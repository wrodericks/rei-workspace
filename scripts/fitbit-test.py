#!/usr/bin/env python3
"""Quick test of Google Fitness API - fetch today's steps, sleep, weight, heart rate."""

import json
import os
import urllib.request
import urllib.parse
from datetime import datetime, date

TOKEN_FILE = os.path.expanduser("~/.openclaw/workspace/credentials/google-health-token.json")
_OAUTH_FILE = os.path.expanduser("~/.openclaw/workspace/credentials/google-oauth.json")
with open(_OAUTH_FILE) as _f:
    _oauth = json.load(_f)
CLIENT_ID = _oauth["client_id"]
CLIENT_SECRET = _oauth["client_secret"]

def refresh_token(tokens):
    data = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": tokens["refresh_token"],
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req) as resp:
        new_tokens = json.loads(resp.read())
        tokens["access_token"] = new_tokens["access_token"]
        with open(TOKEN_FILE, "w") as f:
            json.dump(tokens, f, indent=2)
        return tokens

def api_get(url, access_token):
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {access_token}")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def main():
    with open(TOKEN_FILE) as f:
        tokens = json.load(f)

    # Refresh token to be safe
    tokens = refresh_token(tokens)
    access_token = tokens["access_token"]

    today = date.today().strftime("%Y-%m-%d")
    print(f"Fetching Fitbit data for {today}...\n")

    # Steps
    try:
        url = f"https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"
        # Use REST aggregation for steps
        now_ms = int(datetime.now().timestamp() * 1000)
        start_ms = int(datetime.combine(date.today(), datetime.min.time()).timestamp() * 1000)
        
        body = json.dumps({
            "aggregateBy": [{"dataTypeName": "com.google.step_count.delta"}],
            "bucketByTime": {"durationMillis": 86400000},
            "startTimeMillis": start_ms,
            "endTimeMillis": now_ms
        }).encode()
        
        req = urllib.request.Request(url, data=body, method="POST")
        req.add_header("Authorization", f"Bearer {access_token}")
        req.add_header("Content-Type", "application/json")
        
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
        
        steps = 0
        for bucket in data.get("bucket", []):
            for ds in bucket.get("dataset", []):
                for point in ds.get("point", []):
                    for val in point.get("value", []):
                        steps += val.get("intVal", 0)
        print(f"Steps today: {steps:,}")
    except Exception as e:
        print(f"Steps: error — {e}")

    # Heart rate
    try:
        url = f"https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"
        body = json.dumps({
            "aggregateBy": [{"dataTypeName": "com.google.heart_rate.bpm"}],
            "bucketByTime": {"durationMillis": 86400000},
            "startTimeMillis": start_ms,
            "endTimeMillis": now_ms
        }).encode()
        req = urllib.request.Request(url, data=body, method="POST")
        req.add_header("Authorization", f"Bearer {access_token}")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
        
        hr_vals = []
        for bucket in data.get("bucket", []):
            for ds in bucket.get("dataset", []):
                for point in ds.get("point", []):
                    for val in point.get("value", []):
                        if val.get("fpVal"):
                            hr_vals.append(val["fpVal"])
        if hr_vals:
            print(f"Heart rate today: avg {sum(hr_vals)/len(hr_vals):.0f} bpm, min {min(hr_vals):.0f}, max {max(hr_vals):.0f}")
        else:
            print("Heart rate: no data yet today")
    except Exception as e:
        print(f"Heart rate: error — {e}")

    # Weight
    try:
        body = json.dumps({
            "aggregateBy": [{"dataTypeName": "com.google.weight"}],
            "bucketByTime": {"durationMillis": 86400000 * 7},
            "startTimeMillis": start_ms - 86400000 * 7,
            "endTimeMillis": now_ms
        }).encode()
        req = urllib.request.Request("https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate", data=body, method="POST")
        req.add_header("Authorization", f"Bearer {access_token}")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
        
        weights = []
        for bucket in data.get("bucket", []):
            for ds in bucket.get("dataset", []):
                for point in ds.get("point", []):
                    for val in point.get("value", []):
                        if val.get("fpVal"):
                            weights.append(val["fpVal"])
        if weights:
            print(f"Weight (last 7 days): latest {weights[-1]:.1f} kg")
        else:
            print("Weight: no data in last 7 days")
    except Exception as e:
        print(f"Weight: error — {e}")

    print("\n✅ API connection working!")

if __name__ == "__main__":
    main()
