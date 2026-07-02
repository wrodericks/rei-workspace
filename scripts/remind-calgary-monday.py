#!/usr/bin/env python3
"""One-off Calgary Monday reminders — 2026-06-15. Run with argument: 1, 2, 3, or 4."""
import sys
sys.path.insert(0, '/home/warren/.openclaw/workspace/scripts')
from notify import send

reminders = {
    "1": "⏰ Good morning from Calgary! 6am MT — time to wake up, shower, and get your speaking notes together. Manulife call at 9:30am, session at 10:30am. You've got this.",
    "2": "📝 8:30am MT — back in the room now. Kimon time. Speaking notes need to be solid before 10:15am when you head to the conference.",
    "3": "📞 9:25am MT — Manulife call in 5 minutes. Wrap up with Kimon.",
    "4": "🏃 10:05am MT — Manulife call should be wrapping up. Time to grab your notes and head out — you need to arrive at conference by 10:15 for your 10:30 session.",
}

key = sys.argv[1] if len(sys.argv) > 1 else None
if key in reminders:
    send(reminders[key])
else:
    print(f"Usage: remind-calgary-monday.py [1|2|3|4]")
