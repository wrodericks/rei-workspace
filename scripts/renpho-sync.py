#!/usr/bin/env python3
"""
Renpho sync script — fetches today's weight from Renpho, appends to weight-raw.csv,
regenerates weight-dashboard.png, and updates the daily health log.
Usage: python3 scripts/renpho-sync.py [--date YYYY-MM-DD] [--backfill]
"""

import csv
import json
import os
import re
import subprocess
import sys
import urllib.request
import urllib.parse
import urllib.error
from datetime import date, datetime, timedelta

CREDS_FILE = os.path.expanduser("~/.openclaw/workspace/credentials/renpho.json")
GOOGLE_TOKEN_FILE = os.path.expanduser("~/.openclaw/workspace/credentials/google-health-token.json")
GOOGLE_OAUTH_FILE = os.path.expanduser("~/.openclaw/workspace/credentials/google-oauth.json")
HEALTH_DIR = os.path.expanduser("~/.openclaw/workspace/health")
CSV_PATH = os.path.join(HEALTH_DIR, "weight-raw.csv")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
with open(GOOGLE_OAUTH_FILE) as _f:
    _oauth = json.load(_f)
GOOGLE_CLIENT_ID = _oauth["client_id"]
GOOGLE_CLIENT_SECRET = _oauth["client_secret"]
HEALTH_BASE = "https://health.googleapis.com/v4/users/me"

CSV_FIELDS = ["local_ts", "weight_kg", "bodyfat_pct", "muscle_pct", "bmi", "bmr",
              "body_age", "bone_kg", "water_pct", "protein_pct", "visceral_fat", "source"]

def load_creds():
    with open(CREDS_FILE) as f:
        return json.load(f)

def load_existing_csv():
    """Return set of local_ts strings already in the CSV."""
    existing = set()
    if not os.path.exists(CSV_PATH):
        return existing
    with open(CSV_PATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing.add(row.get("local_ts", ""))
    return existing

def append_to_csv(row_data):
    """Append a row to weight-raw.csv, creating with header if needed."""
    new_file = not os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        if new_file:
            writer.writeheader()
        writer.writerow(row_data)

def measurement_to_row(m):
    return {
        "local_ts": m.get("localCreatedAt", ""),
        "weight_kg": m.get("weight", ""),
        "bodyfat_pct": m.get("bodyfat", ""),
        "muscle_pct": m.get("muscle", ""),
        "bmi": m.get("bmi", ""),
        "bmr": m.get("bmr", ""),
        "body_age": m.get("bodyage", ""),
        "bone_kg": m.get("bone", ""),
        "water_pct": m.get("water", ""),
        "protein_pct": m.get("protein", ""),
        "visceral_fat": m.get("visfat", ""),
        "source": "renpho",
    }

def get_measurements_for_date(measurements, target_date):
    return [m for m in measurements if m.get("localCreatedAt", "").startswith(target_date)]

def update_health_log(log_path, weight_kg, body_fat=None, muscle=None, bmi=None):
    if not os.path.exists(log_path):
        print(f"Log file not found: {log_path}")
        return False
    with open(log_path) as f:
        content = f.read()
    weight_str = f"{weight_kg:.1f} kg"
    if body_fat:
        weight_str += f" (body fat: {body_fat:.1f}%, muscle: {muscle:.1f}%, BMI: {bmi:.1f})"
    new_content = re.sub(r"(- Morning weight:)[^\n]*", f"\\1 {weight_str}", content)
    if new_content == content:
        print("Warning: Could not find 'Morning weight' line to update.")
        return False
    with open(log_path, "w") as f:
        f.write(new_content)
    return True

def push_weight_to_google_health(weight_kg, measurement_date):
    """Push weight reading to Google Health API."""
    try:
        with open(GOOGLE_TOKEN_FILE) as f:
            tokens = json.load(f)
    except FileNotFoundError:
        print("Google Health token not found — skipping weight push")
        return False

    # Refresh access token
    try:
        data = urllib.parse.urlencode({
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "refresh_token": tokens["refresh_token"],
            "grant_type": "refresh_token",
        }).encode()
        req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        with urllib.request.urlopen(req) as resp:
            new_tokens = json.loads(resp.read())
            access_token = new_tokens["access_token"]
            tokens["access_token"] = access_token
            with open(GOOGLE_TOKEN_FILE, "w") as f:
                json.dump(tokens, f, indent=2)
    except Exception as e:
        print(f"Google token refresh failed: {e}")
        return False

    # Build weight payload
    weight_grams = int(round(weight_kg * 1000))
    # 8am EDT = 12:00 UTC
    sample_time_utc = f"{measurement_date}T12:00:00Z"
    body = {
        "weight": {
            "weightGrams": weight_grams,
            "sampleTime": {
                "physicalTime": sample_time_utc,
                "utcOffset": "-14400s"
            },
            "notes": "Synced from Renpho"
        }
    }

    try:
        payload = json.dumps(body).encode()
        # Use the parent-path format per the API spec
        url = f"https://health.googleapis.com/v4/users/me/dataTypes/weight/dataPoints"
        req = urllib.request.Request(url, data=payload, method="POST")
        req.add_header("Authorization", f"Bearer {access_token}")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            print(f"✅ Weight pushed to Google Health: {weight_kg} kg for {measurement_date}")
            return True
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"Google Health weight push failed: {e.code} {err[:300]}")
        return False


def regenerate_dashboard():
    dashboard_script = os.path.join(SCRIPT_DIR, "weight-dashboard.py")
    result = subprocess.run([sys.executable, dashboard_script], capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout.strip())
    else:
        print(f"Dashboard error: {result.stderr.strip()}")

def main():
    backfill = "--backfill" in sys.argv
    target_date = date.today().isoformat()
    if "--date" in sys.argv:
        idx = sys.argv.index("--date")
        if idx + 1 < len(sys.argv):
            target_date = sys.argv[idx + 1]

    print(f"Renpho sync for {target_date}{' (backfill mode)' if backfill else ''}")

    try:
        creds = load_creds()
    except FileNotFoundError:
        print(f"Credentials not found at {CREDS_FILE}")
        sys.exit(1)

    try:
        from renpho import RenphoClient, RenphoAPIError
    except ImportError:
        print("renpho-api not installed. Run: pip install renpho-api --break-system-packages")
        sys.exit(1)

    try:
        client = RenphoClient(creds["email"], creds["password"])
        client.login()
        measurements = client.get_all_measurements()
        print(f"Fetched {len(measurements)} total measurements")
    except Exception as e:
        print(f"Renpho API error: {e}")
        sys.exit(1)

    existing_ts = load_existing_csv()

    if backfill:
        # Write all measurements not already in CSV
        new_rows = 0
        for m in sorted(measurements, key=lambda x: x.get("localCreatedAt", "")):
            local_ts = m.get("localCreatedAt", "")
            if local_ts and local_ts not in existing_ts:
                append_to_csv(measurement_to_row(m))
                existing_ts.add(local_ts)
                new_rows += 1
        print(f"Backfill: added {new_rows} new rows to CSV")
        regenerate_dashboard()
        return

    # Normal mode: find today's measurements
    todays = get_measurements_for_date(measurements, target_date)

    if not todays:
        # Fall back to most recent within last 7 days
        recent = [m for m in measurements
                  if m.get("localCreatedAt", "") >= (date.fromisoformat(target_date) - timedelta(days=7)).isoformat()]
        if recent:
            latest = max(recent, key=lambda m: m.get("localCreatedAt", ""))
            print(f"No measurement today — using most recent: {latest.get('localCreatedAt')} ({latest['weight']} kg)")
        else:
            print("No recent measurements found.")
            sys.exit(0)
    else:
        latest = max(todays, key=lambda m: m.get("localCreatedAt", ""))

    weight = latest["weight"]
    body_fat = latest.get("bodyfat")
    muscle = latest.get("muscle")
    bmi = latest.get("bmi")
    local_ts = latest.get("localCreatedAt", "")
    print(f"Weight: {weight} kg | Body fat: {body_fat}% | Muscle: {muscle}% | BMI: {bmi}")

    # Append new rows to CSV (all of today's readings)
    added = 0
    for m in sorted(todays, key=lambda x: x.get("localCreatedAt", "")):
        if m.get("localCreatedAt", "") not in existing_ts:
            append_to_csv(measurement_to_row(m))
            added += 1
    if added:
        print(f"Appended {added} new reading(s) to CSV")
    else:
        print("No new readings to append (already in CSV)")

    # Regenerate dashboard
    regenerate_dashboard()

    # Push weight to Google Health
    push_weight_to_google_health(weight, target_date)

    # Update health log
    log_path = os.path.join(HEALTH_DIR, "logs", f"{target_date}.md")
    if update_health_log(log_path, weight, body_fat, muscle, bmi):
        print(f"✅ Updated health log: {log_path}")

    print(json.dumps({
        "date": target_date,
        "weight_kg": weight,
        "body_fat_pct": body_fat,
        "muscle_pct": muscle,
        "bmi": bmi,
        "source": "renpho"
    }))

if __name__ == "__main__":
    main()
