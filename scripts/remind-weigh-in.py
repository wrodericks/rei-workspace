#!/usr/bin/env python3
"""Morning weigh-in reminder — 9am daily."""
import sys
sys.path.insert(0, '/home/warren/.openclaw/workspace/scripts')
from notify import send

send(
    "⚖️ Morning weigh-in time!\n\n"
    "Step on the scale before eating or drinking anything. "
    "Same time, same conditions = accurate trend data. Log it when you're done."
)
