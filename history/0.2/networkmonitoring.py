import subprocess
import time
import smtplib
from email.mime.text import MIMEText

# known devices
known_devices = set()

# Email Settings
sender = 'REPLACE_WITH_SMTP_SENDER'
password = 'REPLACE_WITH_SMTP_APP_PASSWORD'
recipient = 'REPLACE_WITH_RECIPIENT_ADDRESS'

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
		print("Alert sent!")
	except Exception as e:
		print("failed to send message", str(e))
	
def scan_network():
	print("Scannig Network...")
	result = subprocess.check_output(["nmap", "-sn", "-e", "wlan0", 'REPLACE_WITH_AUTHORIZED_CIDR'], universal_newlines=True)
	active_ips = set()
	
	for line in result.splitlines():
		if "Nmap scan report for" in line:
			ip = line.split()[-1]
			if ip.startswith('REPLACE_WITH_AUTHORIZED_IP_PREFIX'):
				active_ips.add(ip)
	
	return active_ips
	
def monitor():
	last_alerted_ips =set()
	while True:
		print("SCANNING NETWORK STANDBY...")
		active_ips = scan_network()
		print("Active IPs:", active_ips)
		
		new_devices = active_ips - known_devices - last_alerted_ips
	
		if new_devices:
			for ip in new_devices:
				send_sms(f"!!! UNKNOWN DEVICE DETECTED ON NETWORK: {ip}")
				last_alerted_ips.add(ip)
		else:
			print("No new devices.")
	
	# SCAN WAIT TIME
	time.sleep(60)
	
if __name__=="__main__":
	monitor()
		
