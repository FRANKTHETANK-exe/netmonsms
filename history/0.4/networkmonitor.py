import subprocess
import smtplib
import re
import time
import datetime
import socket
from email.mime.text import MIMEText
import config

def send_sms(message):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(config.sender, config.password)

        msg = MIMEText(message)
        msg["From"] = config.sender
        msg["To"] = config.recipient

        server.sendmail(config.sender, config.recipient, msg.as_string())
        server.quit()
        print("✅ Alert sent!")
    except Exception as e:
        print("❌ Failed to send message:", str(e))

def log_unknown_ip(ip, mac, vendor, hostname):
    with open("device_log.txt", "a") as log:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] IP: {ip}, MAC: {mac}, Vendor: {vendor}, Hostname: {hostname}\n")

def scan_network():
    result = subprocess.check_output(
        ["nmap", "-sn", "-e", config.interface, config.network_range],
        universal_newlines=True
    )

    active_ips = set()
    devices = {}
    current_ip = None

    for line in result.splitlines():
        if "Nmap scan report for" in line:
            current_ip = line.split()[-1]
            active_ips.add(current_ip)
            devices[current_ip] = {"ip": current_ip}
        elif "MAC Address" in line and current_ip:
            mac_info = re.search(r"MAC Address: ([\w:]+) \((.*?)\)", line)
            if mac_info:
                devices[current_ip]["mac"] = mac_info.group(1)
                devices[current_ip]["vendor"] = mac_info.group(2)

    for ip in devices:
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except Exception:
            hostname = "unknown"
        devices[ip]["hostname"] = hostname

    return active_ips, devices

def monitor():
    last_alerted_ips = set()
    last_reset_day = datetime.datetime.now().day

    while True:
        current_day = datetime.datetime.now().day
        if current_day != last_reset_day:
            last_alerted_ips.clear()
            last_reset_day = current_day
            print("🔁 Resetting daily alert list")

        print("📡 Scanning Network...")
        active_ips, devices = scan_network()
        print("📶 Active IPs:", active_ips)

        new_devices = active_ips - config.known_devices - last_alerted_ips

        for ip in new_devices:
            dev = devices.get(ip, {})
            mac = dev.get("mac", "unknown")
            vendor = dev.get("vendor", "unknown")
            hostname = dev.get("hostname", "unknown")

            message = (
                f"NEW DEVICE DETECTED:\n"
                f"IP: {ip}\nMAC: {mac}\nVendor: {vendor}\nHostname: {hostname}"
            )

            send_sms(message)
            log_unknown_ip(ip, mac, vendor, hostname)
            last_alerted_ips.add(ip)

        time.sleep(config.scan_interval)

if __name__ == "__main__":
    monitor()
