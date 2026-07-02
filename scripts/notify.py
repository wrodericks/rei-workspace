#!/usr/bin/env python3
"""
Shared Telegram notification utility.
Reads bot token from OpenClaw config and sends a message to Warren.

Usage:
    from notify import send
    send("Your message here")

Or as a CLI:
    python3 notify.py "Your message here"
"""

import json
import sys
import urllib.request
import urllib.parse

OPENCLAW_CONFIG = "/home/warren/.openclaw/openclaw.json"
CHAT_ID = "8733377781"


def get_bot_token():
    with open(OPENCLAW_CONFIG) as f:
        config = json.load(f)
    return config["channels"]["telegram"]["botToken"]


def send(message: str, parse_mode: str = None) -> bool:
    """Send a Telegram message to Warren. Returns True on success."""
    token = get_bot_token()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode

    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            return result.get("ok", False)
    except Exception as e:
        print(f"Telegram send failed: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 notify.py 'Your message'")
        sys.exit(1)
    msg = " ".join(sys.argv[1:])
    ok = send(msg)
    sys.exit(0 if ok else 1)
