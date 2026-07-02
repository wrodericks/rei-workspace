#!/usr/bin/env python3
"""
10pm screens-off check.
Pings the Samsung TV — only messages Warren if the TV is actually on.
"""
import socket
import sys
sys.path.insert(0, '/home/warren/.openclaw/workspace/scripts')
from notify import send

TV_IP = "192.168.2.20"
TV_PORT = 55000
TIMEOUT = 3

def is_tv_on():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        result = sock.connect_ex((TV_IP, TV_PORT))
        sock.close()
        return result == 0
    except Exception:
        return False

if is_tv_on():
    send(
        "📵 TV off, Warren. Right now.\n\n"
        "You know the pattern: TV → snacking → 2am → wrecked sleep. "
        "It starts here. Turn it off and do something else — read, guitar, or just go to bed. 🌙"
    )
