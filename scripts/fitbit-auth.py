#!/usr/bin/env python3
"""
Google Fitness API OAuth2 authorization flow.
Starts a local server on port 8765, opens the auth URL, captures the token.
"""

import json
import os
import sys
import urllib.parse
import urllib.request
import http.server
import threading
import webbrowser

_OAUTH_FILE = os.path.expanduser("~/.openclaw/workspace/credentials/google-oauth.json")
with open(_OAUTH_FILE) as _f:
    _oauth = json.load(_f)
CLIENT_ID = _oauth["client_id"]
CLIENT_SECRET = _oauth["client_secret"]
REDIRECT_URI = "http://localhost:8765/callback"
TOKEN_FILE = os.path.expanduser("~/.openclaw/workspace/credentials/google-health-token.json")

# Google Health API scopes (Fitbit native)
SCOPES = [
    "https://www.googleapis.com/auth/googlehealth.sleep.readonly",
    "https://www.googleapis.com/auth/googlehealth.activity_and_fitness.readonly",
    "https://www.googleapis.com/auth/googlehealth.health_metrics_and_measurements.readonly",
    "https://www.googleapis.com/auth/googlehealth.health_metrics_and_measurements.writeonly",
    "https://www.googleapis.com/auth/googlehealth.nutrition.readonly",
]

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"

auth_code = None
server_done = threading.Event()

class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if "code" in params:
            auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"""
                <html><body style="font-family:sans-serif;text-align:center;padding:50px">
                <h2>&#10003; Authorization successful!</h2>
                <p>You can close this tab and go back to the terminal.</p>
                </body></html>
            """)
        else:
            error = params.get("error", ["unknown"])[0]
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"<html><body>Error: {error}</body></html>".encode())

        server_done.set()

    def log_message(self, format, *args):
        pass

def build_auth_url():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent",
    }
    return AUTH_URL + "?" + urllib.parse.urlencode(params)

def exchange_code(code):
    data = urllib.parse.urlencode({
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }).encode()

    req = urllib.request.Request(TOKEN_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def main():
    print("Starting local callback server on port 8765...")

    server = http.server.HTTPServer(("localhost", 8765), CallbackHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    url = build_auth_url()
    print(f"\nOpening browser for authorization...")
    print(f"\nIf it doesn't open automatically, visit:\n{url}\n")
    webbrowser.open(url)

    print("Waiting for authorization...")
    server_done.wait(timeout=120)
    server.shutdown()

    if not auth_code:
        print("ERROR: No authorization code received (timed out or error).")
        sys.exit(1)

    print("Authorization code received. Exchanging for tokens...")
    tokens = exchange_code(auth_code)

    os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f, indent=2)
    os.chmod(TOKEN_FILE, 0o600)

    print(f"\n✅ Tokens saved to {TOKEN_FILE}")
    print(f"   Access token: {tokens.get('access_token', '')[:20]}...")
    print(f"   Refresh token: {'present' if tokens.get('refresh_token') else 'MISSING'}")
    print(f"   Expires in: {tokens.get('expires_in')} seconds")
    print(f"   Scopes: {tokens.get('scope', 'unknown')}")

if __name__ == "__main__":
    main()
