#!/usr/bin/env python3
"""Weekly progress photo reminder — Sunday 9am."""
import sys
sys.path.insert(0, '/home/warren/.openclaw/workspace/scripts')
from notify import send

send(
    "📸 Weekly progress photo time!\n\n"
    "Same spot, same lighting, same pose as last week. "
    "The scale doesn't show everything — photos do. Take it before breakfast."
)
