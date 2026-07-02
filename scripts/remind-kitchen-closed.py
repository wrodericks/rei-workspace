#!/usr/bin/env python3
"""Kitchen closed reminder — 8pm daily."""
import sys
sys.path.insert(0, '/home/warren/.openclaw/workspace/scripts')
from notify import send

send(
    "🍽️ Kitchen is closed for the night, Warren.\n\n"
    "You've done the work today — don't undo it in the next two hours. "
    "Water, tea, sparkling water are all yours. Food isn't. 💪"
)
