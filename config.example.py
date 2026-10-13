"""Example only: copy to config.py and supply your own local settings.

Do not commit config.py, SMTP credentials, or real network identifiers.
The field names match the original version 0.5 monitor.
"""

# Add trusted addresses from a network you own or are authorized to monitor.
known_devices = set()
# Version 0.5 uppercases scanned MACs; enter trusted MACs in uppercase.
known_mac_addresses = set()

# The monitor uses smtp.gmail.com:587 with STARTTLS, as in the original.
sender = "REPLACE_WITH_SMTP_SENDER"
password = "REPLACE_WITH_SMTP_APP_PASSWORD"
recipient = "REPLACE_WITH_RECIPIENT_ADDRESS"

interface = "REPLACE_WITH_NETWORK_INTERFACE"
network_range = "REPLACE_WITH_AUTHORIZED_CIDR"
scan_interval = 30
