#!/usr/bin/env python3
"""
Fitbit sync via Google Health API.
Fetches steps, calories burned (TDEE), resting heart rate, sleep, weight, exercise, and heart rate zones.
"""

import json
import os
import re
import sys
import urllib.request
import urllib.parse
import urllib.error
from datetime import date, datetime, timedelta, timezone

TOKEN_FILE = os.path.expanduser("~/.openclaw/workspace/credentials/google-health-token.json")
_OAUTH_FILE = os.path.expanduser("~/.openclaw/workspace/credentials/google-oauth.json")
with open(_OAUTH_FILE) as _f:
    _oauth = json.load(_f)
CLIENT_ID = _oauth["client_id"]
CLIENT_SECRET = _oauth["client_secret"]
HEALTH_DIR = os.path.expanduser("~/.openclaw/workspace/health")
HEALTH_BASE = "https://health.googleapis.com/v4/users/me"


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


def health_get(access_token, path):
    url = f"{HEALTH_BASE}/{path}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {access_token}")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": f"{e.code}: {e.read().decode()[:200]}"}


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
        return {"error": f"{e.code}: {e.read().decode()[:200]}"}


def get_steps(access_token, today):
    d = date.fromisoformat(today)
    r = health_get(access_token, f"dataTypes/steps/dataPoints?pageSize=1000&filter=steps.interval.civil_start_time>=\"{today}T00:00:00\"")
    if "error" in r:
        print(f"  Steps error: {r['error'][:80]}")
        return 0
    total = 0
    for pt in r.get("dataPoints", []):
        total += int(pt.get("steps", {}).get("count", 0) or 0)
    return total


def get_calories_burned(access_token, today):
    """Total daily calories burned (TDEE) via dailyRollUp."""
    d = date.fromisoformat(today)
    body = {
        "range": {
            "start": {"date": {"year": d.year, "month": d.month, "day": d.day}, "time": {"hours": 0}},
            "end": {"date": {"year": d.year, "month": d.month, "day": d.day}, "time": {"hours": 23, "minutes": 59}}
        },
        "pageSize": 3
    }
    r = health_post(access_token, "dataTypes/total-calories/dataPoints:dailyRollUp", body)
    if "error" in r:
        print(f"  Calories error: {r['error'][:80]}")
        return None
    pts = r.get("rollupDataPoints", [])
    if pts:
        return round(pts[0].get("totalCalories", {}).get("kcalSum", 0))
    return None


def get_resting_hr(access_token, today):
    """Resting heart rate for today."""
    d = date.fromisoformat(today)
    r = health_get(access_token, "dataTypes/daily-resting-heart-rate/dataPoints?pageSize=10")
    if "error" in r:
        print(f"  Resting HR error: {r['error'][:80]}")
        return None
    for pt in r.get("dataPoints", []):
        rhr = pt.get("dailyRestingHeartRate", {})
        pt_date = rhr.get("date", {})
        if pt_date.get("year") == d.year and pt_date.get("month") == d.month and pt_date.get("day") == d.day:
            bpm = rhr.get("beatsPerMinute")
            return int(bpm) if bpm else None
    # Fall back to most recent
    pts = r.get("dataPoints", [])
    if pts:
        bpm = pts[0].get("dailyRestingHeartRate", {}).get("beatsPerMinute")
        return int(bpm) if bpm else None
    return None


def get_sleep(access_token, today):
    """Sleep session ending this morning."""
    r = health_get(access_token, "dataTypes/sleep/dataPoints?pageSize=1")
    if "error" in r:
        print(f"  Sleep error: {r['error'][:80]}")
        return None
    pts = r.get("dataPoints", [])
    if not pts:
        return None

    sl = pts[0].get("sleep", {})
    summary = sl.get("summary", {})
    asleep = int(summary.get("minutesAsleep", 0))
    awake = int(summary.get("minutesAwake", 0))

    stage_mins = {}
    for stage in summary.get("stagesSummary", []):
        stage_mins[stage["type"]] = int(stage.get("minutes", 0))

    try:
        end_utc = datetime.fromisoformat(sl["interval"]["endTime"].replace("Z", "+00:00"))
        end_local = end_utc.astimezone()
        start_utc = datetime.fromisoformat(sl["interval"]["startTime"].replace("Z", "+00:00"))
        start_local = start_utc.astimezone()
    except Exception:
        return None

    return {
        "asleep_mins": asleep,
        "awake_mins": awake,
        "deep_mins": stage_mins.get("DEEP", 0),
        "rem_mins": stage_mins.get("REM", 0),
        "light_mins": stage_mins.get("LIGHT", 0),
        "start": start_local.strftime("%I:%M %p"),
        "end": end_local.strftime("%I:%M %p"),
    }


def get_weight(access_token, today):
    """Most recent weight entry."""
    r = health_get(access_token, "dataTypes/weight/dataPoints?pageSize=1")
    if "error" in r:
        return None
    pts = r.get("dataPoints", [])
    if not pts:
        return None
    w = pts[0].get("weight", {})
    grams = w.get("weightGrams")
    if not grams:
        return None
    kg = round(int(grams) / 1000, 1)
    lbs = round(kg * 2.20462, 1)
    cd = w.get("sampleTime", {}).get("civilTime", {}).get("date", {})
    d = f"{cd.get('year','?')}-{cd.get('month',0):02d}-{cd.get('day',0):02d}"
    return {"kg": kg, "lbs": lbs, "date": d}


def get_heart_rate_zones(access_token, today):
    """Daily heart rate zone minutes (rest, fat burn, cardio, peak)."""
    d = date.fromisoformat(today)
    body = {
        "range": {
            "start": {"date": {"year": d.year, "month": d.month, "day": d.day}, "time": {"hours": 0}},
            "end": {"date": {"year": d.year, "month": d.month, "day": d.day}, "time": {"hours": 23, "minutes": 59}}
        },
        "pageSize": 3
    }
    r = health_post(access_token, "dataTypes/heart-rate-summary/dataPoints:dailyRollUp", body)
    if "error" in r:
        # Try alternate endpoint
        r = health_get(access_token, f"dataTypes/heart-rate-summary/dataPoints?pageSize=1")
        if "error" in r:
            return None
        pts = r.get("dataPoints", [])
    else:
        pts = r.get("rollupDataPoints", [])

    if not pts:
        return None

    pt = pts[0]
    # Structure varies — try both rollup and regular formats
    hr = pt.get("heartRateSummary", pt.get("heartRate", {}))
    zones = {}
    for zone in hr.get("heartRateZones", []):
        name = zone.get("name", "").lower().replace(" ", "_")
        zones[name] = int(zone.get("minutes", 0))
    return zones if zones else None


def get_exercise(access_token, today):
    """Exercise sessions for today."""
    r = health_get(access_token, f"dataTypes/exercise/dataPoints?pageSize=25&filter=exercise.interval.civil_start_time>=\"{today}T00:00:00\"")
    if "error" in r:
        return []
    sessions = []
    for pt in r.get("dataPoints", []):
        ex = pt.get("exercise", {})
        try:
            start_utc = datetime.fromisoformat(ex["interval"]["startTime"].replace("Z", "+00:00"))
            end_utc = datetime.fromisoformat(ex["interval"]["endTime"].replace("Z", "+00:00"))
            start_local = start_utc.astimezone()
            dur_min = int((end_utc - start_utc).total_seconds() // 60)
        except Exception:
            continue
        metrics = ex.get("metricsSummary", {})
        sessions.append({
            "type": ex.get("exerciseType", "UNKNOWN"),
            "start": start_local.strftime("%I:%M %p"),
            "duration_mins": dur_min,
            "steps": metrics.get("steps"),
            "calories": metrics.get("calories"),
        })
    return sessions


def update_health_log(today, steps, calories, resting_hr, sleep, weight, exercise, hr_zones=None):
    log_path = os.path.join(HEALTH_DIR, "logs", f"{today}.md")

    if not os.path.exists(log_path):
        print(f"No log file for {today} — skipping update.")
        return

    with open(log_path) as f:
        content = f.read()

    lines = ["\n## Fitbit Sync"]
    lines.append(f"*Last synced: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Steps | {steps:,} |")

    if calories:
        lines.append(f"| Calories burned (TDEE) | {calories:,} kcal |")

    if resting_hr:
        lines.append(f"| Resting heart rate | {resting_hr} bpm |")

    if sleep:
        h = sleep["asleep_mins"] // 60
        m = sleep["asleep_mins"] % 60
        lines.append(f"| Sleep | {h}h {m}m asleep ({sleep['awake_mins']}m awake) · {sleep['start']} → {sleep['end']} |")
        lines.append(f"| Sleep stages | Deep {sleep['deep_mins']}m · REM {sleep['rem_mins']}m · Light {sleep['light_mins']}m |")

    if weight:
        lines.append(f"| Weight | {weight['kg']} kg ({weight['lbs']} lbs) — logged {weight['date']} |")

    if exercise:
        for s in exercise:
            ex_str = f"{s['type'].title()} {s['duration_mins']}m at {s['start']}"
            if s["steps"]:
                ex_str += f" ({s['steps']} steps)"
            if s["calories"]:
                ex_str += f" · {s['calories']} kcal"
            lines.append(f"| Exercise | {ex_str} |")

    if hr_zones:
        zone_parts = []
        for label, key in [("Rest", "out_of_range"), ("Fat Burn", "fat_burn"), ("Cardio", "cardio"), ("Peak", "peak")]:
            if key in hr_zones and hr_zones[key] > 0:
                zone_parts.append(f"{label} {hr_zones[key]}m")
        if zone_parts:
            lines.append(f"| HR Zones | {' · '.join(zone_parts)} |")

    fitbit_section = "\n".join(lines)

    if "## Fitbit Sync" in content:
        content = re.sub(r"\n## Fitbit Sync.*", fitbit_section, content, flags=re.DOTALL)
    else:
        content = content.rstrip() + "\n" + fitbit_section + "\n"

    with open(log_path, "w") as f:
        f.write(content)

    print(f"✅ Updated {log_path}")


def main():
    with open(TOKEN_FILE) as f:
        tokens = json.load(f)

    tokens = refresh_access_token(tokens)
    access_token = tokens["access_token"]

    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        today = sys.argv[1]
    else:
        today = date.today().isoformat()
    print(f"Syncing Fitbit data for {today}...\n")

    steps = get_steps(access_token, today)
    print(f"Steps: {steps:,}")

    calories = get_calories_burned(access_token, today)
    print(f"Calories burned (TDEE): {calories:,} kcal" if calories else "Calories burned: no data")

    resting_hr = get_resting_hr(access_token, today)
    print(f"Resting heart rate: {resting_hr} bpm" if resting_hr else "Resting heart rate: no data")

    sleep = get_sleep(access_token, today)
    if sleep:
        h = sleep["asleep_mins"] // 60
        m = sleep["asleep_mins"] % 60
        print(f"Sleep: {h}h {m}m asleep | Deep: {sleep['deep_mins']}m | REM: {sleep['rem_mins']}m")
    else:
        print("Sleep: no data")

    weight = get_weight(access_token, today)
    if weight:
        print(f"Weight: {weight['kg']} kg ({weight['lbs']} lbs) — logged {weight['date']}")
    else:
        print("Weight: no data")

    exercise = get_exercise(access_token, today)
    if exercise:
        for s in exercise:
            ex_str = f"Exercise: {s['type']} {s['duration_mins']}m at {s['start']}"
            if s["steps"]:
                ex_str += f", {s['steps']} steps"
            if s["calories"]:
                ex_str += f", {s['calories']} kcal"
            print(ex_str)
    else:
        print("Exercise: none today")

    hr_zones = get_heart_rate_zones(access_token, today)
    if hr_zones:
        zone_str = ", ".join(f"{k}: {v}m" for k, v in hr_zones.items() if v > 0)
        print(f"HR Zones: {zone_str}")
    else:
        print("HR Zones: no data")

    update_health_log(today, steps, calories, resting_hr, sleep, weight, exercise, hr_zones)

    if weight and weight["date"] == today:
        weight_log = os.path.join(HEALTH_DIR, "weight.md")
        if os.path.exists(weight_log):
            with open(weight_log) as f:
                wc = f.read()
            if today not in wc:
                with open(weight_log, "a") as f:
                    f.write(f"| {today} | {weight['kg']} | {weight['lbs']} | |\n")
                print(f"✅ Added weight entry to weight.md")
    elif weight:
        print(f"Weight skipped (last entry was {weight['date']}, not today)")

    result = {
        "date": today,
        "steps": steps,
        "calories_burned": calories,
        "resting_hr": resting_hr,
        "sleep": sleep,
        "weight": weight,
    }
    output_path = os.path.join(HEALTH_DIR, "fitbit-latest.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n✅ Saved latest data to {output_path}")


if __name__ == "__main__":
    main()
