import subprocess
import smtplib
import re
import time
import datetime
import socket
from email.mime.text import MIMEText
from config import known_devices, known_mac_addresses, sender, password, recipient, interface, network_range, scan_interval

daily_seen_devices = []
currently_alerted_macs = set()

def send_sms(message):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)

        msg = MIMEText(message)
        msg["From"] = sender
        msg["To"] = recipient

        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
        print("✅ Alert sent!")
    except Exception as e:
        print("❌ Failed to send message:", str(e))


def log_unknown_device(ip, mac, vendor, hostname):
    with open("device_log.txt", "a") as log:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] IP: {ip}, MAC: {mac}, Vendor: {vendor}, Hostname: {hostname}\n")


def scan_network():
    result = subprocess.check_output(
        ["nmap", "-sn", "-e", interface, network_range],
        universal_newlines=True
    )

    active_devices = []
    current_ip = None

    for line in result.splitlines():
        if "Nmap scan report for" in line:
            current_ip = line.split()[-1]
        elif "MAC Address" in line and current_ip:
            mac_match = re.search(r"MAC Address: ([\w:]+) \((.*?)\)", line)
            if mac_match:
                mac = mac_match.group(1).upper()
                vendor = mac_match.group(2)
                try:
                    hostname = socket.gethostbyaddr(current_ip)[0]
                except Exception:
                    hostname = "unknown"
                active_devices.append({
                    "ip": current_ip,
                    "mac": mac,
                    "vendor": vendor,
                    "hostname": hostname
                })
            current_ip = None
    return active_devices


def send_daily_summary(devices):
    if not devices:
        return
    summary = "📋 Daily Network Summary:\n"
    for dev in devices:
        summary += (
            f"- IP: {dev['ip']}, MAC: {dev['mac']}, "
            f"Vendor: {dev['vendor']}, Hostname: {dev['hostname']}\n"
        )
    send_sms(summary)


def monitor():
    print("🔍 Network monitoring started...")
    last_reset_day = datetime.datetime.now().day

    global daily_seen_devices
    global currently_alerted_macs

    while True:
        current_day = datetime.datetime.now().day
        if current_day != last_reset_day:
            print("🔄 Resetting daily log and sending summary...")
            send_daily_summary(daily_seen_devices)
            daily_seen_devices = []
            currently_alerted_macs = set()
            last_reset_day = current_day

        print("📡 Scanning Network...")
        active_devices = scan_network()
        active_macs = {dev['mac'] for dev in active_devices}

        for dev in active_devices:
            mac = dev["mac"]
            ip = dev["ip"]

            if mac not in known_mac_addresses and ip not in known_devices:
                message = (
                    "🔔 Unknown Device Detected:\n"
                    f"IP: {ip}\nMAC: {mac}\nVendor: {dev['vendor']}\nHostname: {dev['hostname']}"
                )
                send_sms(message)
                log_unknown_device(ip, mac, dev['vendor'], dev['hostname'])
                currently_alerted_macs.add(mac)

            daily_seen_devices.append(dev)

        currently_alerted_macs.intersection_update(active_macs)
        time.sleep(scan_interval)


if __name__ == "__main__":
    monitor()
