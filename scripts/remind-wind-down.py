#!/usr/bin/env python3
"""Wind-down reminder — 10:30pm daily."""
import sys
sys.path.insert(0, '/home/warren/.openclaw/workspace/scripts')
from notify import send

send(
    "🌙 Wind-down time, Warren.\n\n"
    "Dim the lights, put the phone down. "
    "Target: asleep by 11:30pm. Your body will thank you tomorrow. 😴"
)
