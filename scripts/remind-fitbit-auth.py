#!/usr/bin/env python3
"""One-shot Fitbit OAuth renewal reminder via Telegram."""
import requests

TELEGRAM_TOKEN   = '8755549029:AAFRMrSWJIDJmGWFVt8iiEBlGXN4dxfMr6o'
TELEGRAM_CHAT_ID = '8733377781'

msg = (
    "⏰ *Fitbit OAuth reminder*\n"
    "Token expires today (7-day limit on unverified Google apps).\n"
    "Run: `python3 ~/.openclaw/workspace/scripts/fitbit-auth.py`\n"
    "Then paste the URL in your browser and approve. Takes 2 minutes."
)

requests.post(
    f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage',
    json={'chat_id': TELEGRAM_CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'},
    timeout=10
)
print("Reminder sent.")
