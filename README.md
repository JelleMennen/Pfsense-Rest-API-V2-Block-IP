# pfSense REST API V2 — Automated IP Blocking

A Python script that automates firewall rule creation on pfSense using the REST API V2. Designed as a response action module for SIEM and IDS pipelines.

📄 **Full writeup:** [Automating IP Blocking in pfSense with the REST API V2](https://medium.com/@jellemennen) *(Medium)*

---

## What It Does

Sends a single API call to your pfSense firewall to create a block rule for a given IP address. The rule is applied immediately — no manual "Apply Changes" needed.

```bash
python pfsense_block.py 192.168.2.100
# → Block rule created and applied on pfSense
```

## Requirements

- pfSense with [pfSense-pkg-RESTAPI](https://github.com/pfrest/pfSense-pkg-RESTAPI) (V2) installed
- Python 3.x
- `requests` library (`pip install requests`)

## Setup

1. Install the REST API V2 package on pfSense (System → Package Manager)
2. Create an API key (System → REST API → Settings)
3. Clone this repo and update `pfsense_block.py` with your pfSense IP and API key:

```python
PFSENSE_URL = "https://<your-pfsense-ip>/api/v2/firewall/rule"
API_KEY     = "<your-api-key>"
```

4. Run:

```bash
python pfsense_block.py <ip-to-block>
```

## Security Notes

- `verify=False` is used because this targets a homelab with a self-signed certificate. For production, use `verify="/path/to/ca.pem"` with a proper certificate chain.
- Use a dedicated pfSense user with **only** firewall rule privileges for the API key. V2 supports granular per-endpoint permissions — don't use your admin account.
- Never commit your actual API key. Use environment variables or a config file excluded via `.gitignore`.

## How It Fits Together

This script is the **response action** component of a custom SIEM system I'm building:

```
IDS → Python SIEM → AI Analysis (Ollama) → pfsense_block_ip()
```

When the SIEM detects a high-risk threat, this script blocks the source IP at the firewall automatically.