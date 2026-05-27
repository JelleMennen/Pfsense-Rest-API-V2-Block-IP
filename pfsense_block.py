import requests
import urllib3
import json
import logging
import sys

# Disables the errors for the self singed certfications (verify-False) to keep the output clean

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("pfSense")

# Config: Use your own credentials
PFSENSE_URL = "https://YOURURL/api/v2/firewall/rule"
API_KEY = "Your API key"

HEADERS = {
    "X-API-Key":    API_KEY,
    "Content-Type": "application/json",
}

def pfsense_block_ip(ip_address: str) -> bool:

    payload = {
        "type":           "block",
        "interface":      ["lan"],
        "ipprotocol":     "inet",
        "protocol":       None,
        "source":         ip_address,
        "source_port":    None,
        "destination":    "any",
        "destination_port": None,
        "descr":          f"auto-block {ip_address}",
        "disabled":       False,
        "log":            True,
        "floating":       False,
        "quick":          False,
        "statetype":      "keep state",
        "tcp_flags_any":  False,
        "tcp_flags_out_of": None,
        "tcp_flags_set":  None,
        "top":            True,
        "apply":          True,
    }

    print("Payload:", json.dumps(payload, indent=2))

    try: 
        response = requests.post(
        PFSENSE_URL, headers=HEADERS, json=payload,
        timeout=8, verify=False
    )
        response.raise_for_status()
        print(f"Blocked: {ip_address}")
        print(f"Response:", response.json)
        return True
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        if e.response is not None:
            print("Response body:", e.response.text)
        return False
    except Exception as e:
        print(f"Error: {e}")
    return False

if __name__ == "__main__":
    target_ip = sys.argv[1]
    pfsense_block_ip(target_ip)