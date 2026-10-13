# Version history and source notes

Version numbers come from the supplied folder names. They are not independently verified release tags.

| Version | What is in the source | Review notes |
| --- | --- | --- |
| [0.1](history/0.1/network_alert.py) | One SMTP email-to-SMS message, using Gmail and a carrier gateway. | The example call is at module scope: importing the original would send a message. Private sender, password, and destination literals were replaced with placeholders. |
| [0.2](history/0.2/networkmonitoring.py) | Nmap scanning, a trusted IP set, and an in-memory list of addresses already alerted. | The `time.sleep(60)` call is outside the infinite loop, so scans are not delayed by it. Network range and IP-prefix filtering are hardcoded in the original; both are placeholders here, and the trusted-device set is empty. SMTP/contact literals are also placeholders. |
| [0.3](history/0.3/networkmonitoring.py) | Separate configuration, local device logging, reverse DNS, MAC/vendor parsing, and a daily reset of alert history. | `send_sms` accepts one argument but the monitor calls it with two. The MAC-line condition checks `Mac Address` while the regex expects `MAC Address`. Both defects remain visible. An unused MIME multipart import is also present. |
| [0.4](history/0.4/networkmonitor.py) | The same IP-based monitoring design with a one-argument message call and a matching uppercase MAC-line condition. | Compared with 0.3, the two defects above are corrected and formatting/messages are revised. The supplied loose `networkmonitor.py` is byte-for-byte identical to this version and is included only once. |
| [0.5](networkmonitor.py) | Trusted MAC addresses alongside IPs, a MAC-oriented device list, a daily summary, and tracking of currently observed MACs. | The tracking set does not gate alerts, so unknown devices trigger messages every scan. The summary collects observations rather than unique devices. Trusted MAC entries must match the parser's uppercase representation; the original config mixed letter case. |

The loose `network_alert.py` is a near duplicate of 0.1. Once private configuration is normalized, its only AST-level difference is the message text `New device connected!` instead of `New device connected`; whitespace and indentation also differ. The 0.1 copy is retained, and this text difference is recorded here instead of adding another copy of the same logic.

The three original private configuration files were not copied. The public template preserves their configuration interface and the latest field set, including the MAC allowlist introduced in 0.5. The template can also provide the fields used by 0.3 and 0.4 if copied into the corresponding historical directory, but those files are retained for inspection, not as recommended entry points. Versions 0.1 and 0.2 do not load `config.py`.

Three device logs and three compiled configuration caches were excluded because they are generated files containing or potentially containing private settings and device information. Originals remain in their source folder. No source behavior was changed except replacement/removal of private literal configuration in 0.1 and 0.2.
