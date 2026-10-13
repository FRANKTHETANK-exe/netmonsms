# NetmonSMS

A Python project that uses Nmap host discovery to look for unfamiliar devices on a local network and sends email/SMS-gateway alerts through SMTP.

The top-level `networkmonitor.py` is the latest supplied version, 0.5. It records device details, compares IP and MAC addresses with trusted-device lists, and attempts to send a summary when the calendar day changes. Earlier versions are in `history/`; their changes and defects are described in [HISTORY.md](HISTORY.md).

## Files and configuration

- `networkmonitor.py`: original version 0.5 source, unchanged.
- `config.example.py`: a clean template with the configuration fields the monitor imports. Copy it to `config.py` and replace every `REPLACE_WITH_...` value locally.
- `history/`: earlier source retained to show how the project developed. Versions 0.1 and 0.2 have private literals replaced with placeholders.

Python 3 and an installed `nmap` command are required by the code. The Python imports are all from the standard library. No exact Python or Nmap version requirement was supplied. The original configurations use a 30-second interval; this is retained in the template.

The SMTP host and port are hardcoded as `smtp.gmail.com:587`, with STARTTLS. Configure the sender, credential, recipient address, network interface, authorized scan range, and trusted devices before considering a run. SMS delivery depends on the recipient gateway. SMTP authentication and carrier delivery have not been checked.

## Current limitations

This is a preserved project snapshot, not a validated monitoring service:

- Version 0.5 sends an alert for every unknown device on every scan. It updates `currently_alerted_macs` but never uses that set to suppress repeated alerts.
- Its daily summary appends each observation, so the same device can appear many times.
- Only reports with a matching MAC/vendor line are added to the device list. Other discovered hosts may be omitted.
- The parser takes the last token of each Nmap report as an IP. Hostname-formatted reports can leave parentheses in that token and affect lookups or matching.
- Scan failures are not caught. Failed message delivery is printed, but there is no retry queue.
- Device details, including addresses and hostnames, are written to `device_log.txt` and included in outgoing messages.

Use only a network you own or have permission to monitor. Choose a recipient you control and consider the device information that messages will disclose. Keep `config.py` and generated logs private. The included `.gitignore` excludes them and Python caches.

## Review status

All six included Python files passed static compilation without importing or running them. No network scan, SMTP login, message delivery, or device interaction was performed. The historical bugs were documented rather than silently changed.

No license, upstream reference, or authorship header was present in the supplied folder. No license has been invented for this package; the source provenance beyond those local files is unverified.
