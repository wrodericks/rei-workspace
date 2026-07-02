#!/usr/bin/env python3
"""
Check if Warren's Samsung TV (192.168.2.20) is on.
Uses port 55000 (Samsung 2013-era control API).
Returns: "on" if TV is on and reachable, "off" otherwise.
"""

import socket
import sys

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

if __name__ == "__main__":
    if is_tv_on():
        print("on")
        sys.exit(0)
    else:
        print("off")
        sys.exit(1)
