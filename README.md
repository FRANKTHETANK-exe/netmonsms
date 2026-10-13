# NetmonSMS

NetmonSMS checks a local network for unfamiliar devices and emails an alert with their IP address, MAC address, vendor, and hostname. It uses Nmap for discovery and Gmail SMTP for delivery. Version 0.5 also writes a device log and sends a daily summary while the monitor is running.

## Requirements

- Python 3. All Python dependencies are in the standard library.
- [Nmap](https://nmap.org/download.html), available as `nmap` on your `PATH`.
- A Gmail account that supports app passwords.
- Access to a local network you own or have permission to monitor.

Install Nmap using its [installation guide](https://nmap.org/book/install.html). On a Mac with Homebrew, the [Nmap formula](https://formulae.brew.sh/formula/nmap) provides:

```sh
brew install nmap
```

Check that both commands are available:

```sh
python3 --version
nmap --version
```

## Setup

From the project directory, create your local configuration:

```sh
cp config.example.py config.py
```

Edit `config.py` and replace every `REPLACE_WITH_...` value:

| Setting | Value |
| --- | --- |
| `sender` | Your full Gmail address. |
| `password` | A Google app password for this monitor. |
| `recipient` | The email address that should receive alerts. |
| `interface` | The network interface connected to your LAN. |
| `network_range` | Your LAN's CIDR range. |
| `known_devices` | A Python set of trusted IP address strings; `set()` leaves it empty. |
| `known_mac_addresses` | A Python set of trusted MAC address strings, using uppercase letters and colons. |
| `scan_interval` | Seconds to wait after each scan; the default is `30`. |

A device is trusted if either its IP or its MAC address matches a trusted entry. Empty allowlists make every detected device unknown.

To create the app password, enable 2-Step Verification, then open your Google Account's [App passwords](https://myaccount.google.com/apppasswords) page and create one for NetmonSMS. Put that password in `config.py`. Google restricts app passwords for some accounts, including some organization accounts and accounts with Advanced Protection; see [Google's app-password help](https://support.google.com/accounts/answer/185833?hl=en).

The script connects to `smtp.gmail.com` on port `587` with STARTTLS, matching [Google's SMTP settings](https://knowledge.workspace.google.com/admin/gmail/send-email-from-a-printer-scanner-or-app). It does not implement OAuth.

Start with a regular email inbox as the recipient. SMS requires a working email-to-text gateway: [AT&T ended that service in June 2025](https://www.att.com/support/article/wireless/KM1061254/), and [Verizon is shutting it down by March 31, 2027](https://www.verizon.com/support/vtext-vzwpix-shutdown/). The early examples use `tmomail.net`; [T-Mobile still describes tmomail delivery](https://www.t-mobile.com/support/plans-features/help-with-scams-spam-and-fraud), but delivery with this project is unverified.

## Run

Stay in the project directory so the log is written there:

```sh
python3 networkmonitor.py
```

Press `Ctrl+C` to stop. Nmap uses different discovery methods depending on privileges; local Ethernet MAC discovery may require elevated privileges. See [Nmap's host-discovery documentation](https://nmap.org/book/man-host-discovery.html). On Unix, when those privileges are needed:

```sh
sudo python3 networkmonitor.py
```

The terminal shows scan activity and whether SMTP submission succeeded. Unknown devices are appended to `device_log.txt` with a timestamp and the same details sent in the alert. After a change of calendar day, the next loop sends the collected observations as a summary and clears that list. Stopping the process does not send a final summary.

`Alert sent!` means SMTP submission succeeded; it does not confirm inbox or phone delivery. Alerts include network identifiers, so use a recipient you control. Keep `config.py` and `device_log.txt` private; both are in `.gitignore`.

## Known limitations

- Unknown devices trigger another alert on every scan. The MAC tracking set does not currently suppress repeat alerts.
- Daily summaries contain repeated observations of the same device.
- Discovery only records Nmap output with a matching MAC/vendor line. Hosts without that line are skipped, and hostname-formatted IPs can be parsed incorrectly.
- A failed scan stops the process. Failed emails are printed to the terminal but are not queued for retry.

## Earlier versions

Versions 0.1–0.4 are in [`history/`](history/): an SMTP test, IP-based monitoring, device logging, then alert-call and MAC-parser fixes. Use the top-level script for version 0.5. The early files contain unfinished behavior: 0.1 sends on import, 0.2 has no delay inside its scan loop, and 0.3 has a broken alert call.
