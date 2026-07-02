#!/usr/bin/env python3
"""
Daily health metrics collector.
Pulls from: Google Health API (Fitbit), Renpho CSV, daily log markdown.
Writes one row per day to health/metrics.csv.

Usage:
  python3 metrics-collect.py                  # today
  python3 metrics-collect.py 2026-04-13       # specific date
  python3 metrics-collect.py --backfill       # Apr 13 → today
"""

import json
import os
import re
import sys
import csv
import urllib.request
import urllib.parse
import urllib.error
from datetime import date, datetime, timedelta

TOKEN_FILE = os.path.expanduser("~/.openclaw/workspace/credentials/google-health-token.json")
_OAUTH_FILE = os.path.expanduser("~/.openclaw/workspace/credentials/google-oauth.json")
with open(_OAUTH_FILE) as _f:
    _oauth = json.load(_f)
CLIENT_ID = _oauth["client_id"]
CLIENT_SECRET = _oauth["client_secret"]
HEALTH_DIR = os.path.expanduser("~/.openclaw/workspace/health")
HEALTH_BASE = "https://health.googleapis.com/v4/users/me"
METRICS_FILE = os.path.join(HEALTH_DIR, "metrics.csv")
RENPHO_FILE = os.path.join(HEALTH_DIR, "weight-raw.csv")

FIELDNAMES = [
    "date",
    # Renpho body comp
    "weight_kg", "bodyfat_pct", "muscle_pct", "bmi", "bmr", "visceral_fat", "water_pct",
    # Fitbit activity
    "steps", "calories_burned", "resting_hr",
    # Fitbit sleep
    "sleep_mins", "deep_mins", "rem_mins",
    # Nutrition (from daily log)
    "calories_in", "protein_g", "net_deficit",
]


# ── Token ──────────────────────────────────────────────────────────────────

def load_tokens():
    with open(TOKEN_FILE) as f:
        return json.load(f)

def refresh_access_token(tokens):
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


# ── Health API helpers ─────────────────────────────────────────────────────

def health_get(access_token, path):
    url = f"{HEALTH_BASE}/{path}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {access_token}")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": f"{e.code}"}

def health_post(access_token, path, body):
    url = f"{HEALTH_BASE}/{path}"
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {access_token}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": f"{e.code}"}


# ── Fitbit data for a specific date ───────────────────────────────────────

def get_steps_for(access_token, day):
    r = health_get(access_token, f'dataTypes/steps/dataPoints?pageSize=1000&filter=steps.interval.civil_start_time>="{day}T00:00:00"&filter=steps.interval.civil_start_time<"{next_day(day)}T00:00:00"')
    if "error" in r:
        return None
    total = sum(int(pt.get("steps", {}).get("count", 0) or 0) for pt in r.get("dataPoints", []))
    return total or None

def get_calories_for(access_token, day):
    d = date.fromisoformat(day)
    body = {
        "range": {
            "start": {"date": {"year": d.year, "month": d.month, "day": d.day}, "time": {"hours": 0}},
            "end": {"date": {"year": d.year, "month": d.month, "day": d.day}, "time": {"hours": 23, "minutes": 59}}
        },
        "pageSize": 3
    }
    r = health_post(access_token, "dataTypes/total-calories/dataPoints:dailyRollUp", body)
    if "error" in r:
        return None
    pts = r.get("rollupDataPoints", [])
    if pts:
        val = round(pts[0].get("totalCalories", {}).get("kcalSum", 0))
        return val if val > 0 else None
    return None

def get_resting_hr_for(access_token, day):
    d = date.fromisoformat(day)
    r = health_get(access_token, "dataTypes/daily-resting-heart-rate/dataPoints?pageSize=30")
    if "error" in r:
        return None
    for pt in r.get("dataPoints", []):
        rhr = pt.get("dailyRestingHeartRate", {})
        pt_date = rhr.get("date", {})
        if pt_date.get("year") == d.year and pt_date.get("month") == d.month and pt_date.get("day") == d.day:
            bpm = rhr.get("beatsPerMinute")
            return int(bpm) if bpm else None
    return None

def get_sleep_for(access_token, day):
    """Find sleep session ending on this day."""
    r = health_get(access_token, "dataTypes/sleep/dataPoints?pageSize=60")
    if "error" in r:
        return None
    d = date.fromisoformat(day)
    for pt in r.get("dataPoints", []):
        sl = pt.get("sleep", {})
        interval = sl.get("interval", {})
        end_str = interval.get("endTime", "")
        if not end_str:
            continue
        try:
            end_utc = datetime.fromisoformat(end_str.replace("Z", "+00:00"))
            end_local = end_utc - timedelta(hours=4)
            if end_local.date() == d:
                summary = sl.get("summary", {})
                asleep = int(summary.get("minutesAsleep", 0))
                deep = 0
                rem = 0
                for stage in summary.get("stagesSummary", []):
                    if stage["type"] == "DEEP":
                        deep = int(stage.get("minutes", 0))
                    elif stage["type"] == "REM":
                        rem = int(stage.get("minutes", 0))
                return {"sleep_mins": asleep, "deep_mins": deep, "rem_mins": rem}
        except Exception:
            continue
    return None


# ── Renpho data ───────────────────────────────────────────────────────────

def load_renpho():
    """Load renpho CSV, return dict keyed by date string."""
    by_date = {}
    if not os.path.exists(RENPHO_FILE):
        return by_date
    with open(RENPHO_FILE) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                ts = datetime.strptime(row["local_ts"], "%Y-%m-%d %H:%M:%S")
                d = ts.date().isoformat()
                # Keep last reading of the day; skip rows with zero body fat (raw weight only)
                if float(row.get("bodyfat_pct", 0)) > 0:
                    by_date[d] = row
                elif d not in by_date:
                    by_date[d] = row
            except Exception:
                continue
    return by_date


# ── Parse daily log markdown ───────────────────────────────────────────────

def parse_daily_log(day):
    log_path = os.path.join(HEALTH_DIR, "logs", f"{day}.md")
    if not os.path.exists(log_path):
        return {}

    with open(log_path) as f:
        content = f.read()

    result = {}

    # Calories in + protein — parse **TOTAL** row from food table
    # Format: | **TOTAL** | | 2,029 | 151g | ...
    total_match = re.search(r'\|\s*\*\*TOTAL\*\*\s*\|[^|]*\|\s*\*?\*?~?([\d,]+)\*?\*?\s*\|\s*\*?\*?~?(\d+)g?\*?\*?\s*\|', content, re.IGNORECASE)
    if total_match:
        result["calories_in"] = int(total_match.group(1).replace(",", ""))
        result["protein_g"] = int(total_match.group(2))

    # Calories burned — various formats in logs
    burn_patterns = [
        r'Calories burned.*?(\d[\d,]+)\s*kcal',
        r'TDEE.*?(\d[\d,]+)',
        r'calories.*?burned.*?(\d[\d,]+)',
        r'\*\*TDEE\*\*.*?(\d[\d,]+)',
        r'Total burn.*?(\d[\d,]+)',
        r'\| Calories burned \(TDEE\) \| ([\d,]+) kcal \|',
    ]
    for pattern in burn_patterns:
        m = re.search(pattern, content, re.IGNORECASE)
        if m:
            val = int(m.group(1).replace(",", ""))
            if val > 1000:  # sanity check
                result["calories_burned_log"] = val
                break

    # Net deficit — various formats
    deficit_patterns = [
        r'[Dd]eficit.*?(\d[\d,]+)\s*kcal',
        r'[Nn]et deficit.*?(\d[\d,]+)',
        r'[Dd]eficit[:\s]+\*?\*?~?(\d[\d,]+)',
    ]
    for pattern in deficit_patterns:
        m = re.search(pattern, content, re.IGNORECASE)
        if m:
            val = int(m.group(1).replace(",", ""))
            if 0 < val < 5000:
                result["net_deficit"] = val
                break

    return result


# ── Build one row ──────────────────────────────────────────────────────────

def next_day(day):
    return (date.fromisoformat(day) + timedelta(days=1)).isoformat()

def collect_day(access_token, day, renpho_by_date):
    print(f"  Collecting {day}...")
    row = {"date": day}

    # Renpho
    renpho = renpho_by_date.get(day, {})
    if renpho:
        row["weight_kg"] = renpho.get("weight_kg", "")
        row["bodyfat_pct"] = renpho.get("bodyfat_pct", "")
        row["muscle_pct"] = renpho.get("muscle_pct", "")
        row["bmi"] = renpho.get("bmi", "")
        row["bmr"] = renpho.get("bmr", "")
        row["visceral_fat"] = renpho.get("visceral_fat", "")
        row["water_pct"] = renpho.get("water_pct", "")

    # Fitbit via API
    steps = get_steps_for(access_token, day)
    if steps:
        row["steps"] = steps

    calories = get_calories_for(access_token, day)
    if calories:
        row["calories_burned"] = calories

    rhr = get_resting_hr_for(access_token, day)
    if rhr:
        row["resting_hr"] = rhr

    sleep = get_sleep_for(access_token, day)
    if sleep:
        row["sleep_mins"] = sleep["sleep_mins"]
        row["deep_mins"] = sleep["deep_mins"]
        row["rem_mins"] = sleep["rem_mins"]

    # Daily log (calories in, protein, deficit)
    log_data = parse_daily_log(day)
    if "calories_in" in log_data:
        row["calories_in"] = log_data["calories_in"]
    if "protein_g" in log_data:
        row["protein_g"] = log_data["protein_g"]
    if "net_deficit" in log_data:
        row["net_deficit"] = log_data["net_deficit"]
    # Use log calories_burned if API didn't return one
    if "calories_burned" not in row and "calories_burned_log" in log_data:
        row["calories_burned"] = log_data["calories_burned_log"]
    # Compute deficit if we have both
    if "net_deficit" not in row and "calories_burned" in row and "calories_in" in row:
        row["net_deficit"] = int(row["calories_burned"]) - int(row["calories_in"])

    return row


# ── CSV I/O ────────────────────────────────────────────────────────────────

def load_existing():
    if not os.path.exists(METRICS_FILE):
        return {}
    rows = {}
    with open(METRICS_FILE) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows[row["date"]] = row
    return rows

def save_all(rows_by_date):
    dates = sorted(rows_by_date.keys())
    with open(METRICS_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        for d in dates:
            writer.writerow(rows_by_date[d])
    print(f"✅ Saved {len(dates)} rows to {METRICS_FILE}")


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    tokens = load_tokens()
    tokens = refresh_access_token(tokens)
    access_token = tokens["access_token"]

    renpho_by_date = load_renpho()
    existing = load_existing()

    if "--backfill" in sys.argv:
        start = date(2026, 4, 13)
        end = date.today()
        days = []
        d = start
        while d <= end:
            days.append(d.isoformat())
            d += timedelta(days=1)
        print(f"Backfilling {len(days)} days ({days[0]} → {days[-1]})...")
    elif len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        days = [sys.argv[1]]
    else:
        days = [date.today().isoformat()]

    for day in days:
        row = collect_day(access_token, day, renpho_by_date)
        existing[day] = row

    save_all(existing)

if __name__ == "__main__":
    main()
