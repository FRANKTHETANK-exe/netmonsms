"""Copy to config.py and fill in your settings. Keep config.py private."""

# Add trusted addresses from a network you own or are authorized to monitor.
known_devices = set()
# Enter trusted MAC addresses in uppercase, separated by colons.
known_mac_addresses = set()

# Gmail SMTP credentials and alert recipient.
sender = "REPLACE_WITH_SMTP_SENDER"
password = "REPLACE_WITH_SMTP_APP_PASSWORD"
recipient = "REPLACE_WITH_RECIPIENT_ADDRESS"

interface = "REPLACE_WITH_NETWORK_INTERFACE"
network_range = "REPLACE_WITH_AUTHORIZED_CIDR"
scan_interval = 30
