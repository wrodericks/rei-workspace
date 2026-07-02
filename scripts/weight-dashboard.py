#!/usr/bin/env python3
"""
Weight dashboard generator.
Reads health/weight-raw.csv and outputs health/weight-dashboard.png.
No AI involvement — pure data viz.
Usage: python3 scripts/weight-dashboard.py
"""

import csv
import os
from datetime import datetime, timedelta

HEALTH_DIR = os.path.expanduser("~/.openclaw/workspace/health")
CSV_PATH = os.path.join(HEALTH_DIR, "weight-raw.csv")
PNG_PATH = os.path.join(HEALTH_DIR, "weight-dashboard.png")

GOAL_WEIGHT = 81.0
START_WEIGHT = 119.2  # first reading Apr 14, 2026

def load_data():
    rows = []
    if not os.path.exists(CSV_PATH):
        return rows
    with open(CSV_PATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row["local_ts"] = datetime.strptime(row["local_ts"], "%Y-%m-%d %H:%M:%S")
                row["weight_kg"] = float(row["weight_kg"])
                row["bodyfat_pct"] = float(row["bodyfat_pct"]) if row.get("bodyfat_pct") else None
                row["muscle_pct"] = float(row["muscle_pct"]) if row.get("muscle_pct") else None
                row["bmi"] = float(row["bmi"]) if row.get("bmi") else None
                rows.append(row)
            except (ValueError, KeyError):
                continue
    return sorted(rows, key=lambda r: r["local_ts"])

def daily_latest(rows):
    """One reading per day — latest of the day."""
    by_date = {}
    for r in rows:
        d = r["local_ts"].date()
        by_date[d] = r
    return sorted(by_date.values(), key=lambda r: r["local_ts"])

def moving_avg(values, window=7):
    result = []
    for i in range(len(values)):
        start = max(0, i - window + 1)
        result.append(sum(values[start:i+1]) / (i - start + 1))
    return result

def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.gridspec import GridSpec

    rows = load_data()
    if not rows:
        print("No data in weight-raw.csv")
        return

    daily = daily_latest(rows)
    dates = [r["local_ts"] for r in daily]
    weights = [r["weight_kg"] for r in daily]
    bodyfats = [r["bodyfat_pct"] for r in daily if r["bodyfat_pct"] is not None and r["bodyfat_pct"] > 1.0]
    bf_dates = [r["local_ts"] for r in daily if r["bodyfat_pct"] is not None and r["bodyfat_pct"] > 1.0]
    mavg = moving_avg(weights)

    current = weights[-1]
    lost = START_WEIGHT - current
    remaining = current - GOAL_WEIGHT
    pct_done = (lost / (START_WEIGHT - GOAL_WEIGHT)) * 100

    # Trend projection (last 14 days)
    if len(daily) >= 7:
        recent = daily[-14:]
        r_dates = [(r["local_ts"] - recent[0]["local_ts"]).days for r in recent]
        r_weights = [r["weight_kg"] for r in recent]
        if len(set(r_dates)) > 1:
            import statistics
            n = len(r_dates)
            mx = sum(r_dates) / n
            my = sum(r_weights) / n
            slope = sum((x - mx) * (y - my) for x, y in zip(r_dates, r_weights)) / sum((x - mx)**2 for x in r_dates)
            intercept = my - slope * mx
            if slope < 0:
                days_to_goal = (GOAL_WEIGHT - intercept) / slope
                goal_date = recent[0]["local_ts"] + timedelta(days=days_to_goal)
            else:
                goal_date = None
        else:
            slope = 0
            goal_date = None
    else:
        slope = 0
        goal_date = None

    # --- Plot ---
    fig = plt.figure(figsize=(12, 8), facecolor="#1a1a2e")
    gs = GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.3)

    ax1 = fig.add_subplot(gs[0, :])   # weight over time (full width)
    ax2 = fig.add_subplot(gs[1, 0])   # body fat
    ax3 = fig.add_subplot(gs[1, 1])   # progress bar

    text_color = "#e0e0e0"
    grid_color = "#2a2a4a"
    accent = "#4fc3f7"
    green = "#81c784"
    orange = "#ffb74d"

    # --- Weight chart ---
    ax1.set_facecolor("#0d0d1a")
    ax1.plot(dates, weights, color=accent, linewidth=1.5, alpha=0.6, label="Daily weight")
    ax1.plot(dates, mavg, color=orange, linewidth=2.5, label="7-day avg")
    ax1.axhline(GOAL_WEIGHT, color=green, linewidth=1, linestyle="--", alpha=0.7, label=f"Goal {GOAL_WEIGHT} kg")
    ax1.set_title("Weight Over Time", color=text_color, fontsize=13, pad=10)
    ax1.set_ylabel("kg", color=text_color)
    ax1.tick_params(colors=text_color)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax1.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=30, ha="right")
    ax1.yaxis.set_tick_params(labelcolor=text_color)
    ax1.spines[:].set_color(grid_color)
    ax1.grid(True, color=grid_color, alpha=0.5)
    ax1.legend(facecolor="#1a1a2e", labelcolor=text_color, fontsize=9)

    # Annotate latest
    ax1.annotate(f"{current:.1f} kg", xy=(dates[-1], current),
                 xytext=(-60, 12), textcoords="offset points",
                 color=accent, fontsize=10, fontweight="bold",
                 arrowprops=dict(arrowstyle="->", color=accent, lw=1))

    # --- Body fat chart ---
    ax2.set_facecolor("#0d0d1a")
    if bf_dates:
        ax2.plot(bf_dates, bodyfats, color="#f48fb1", linewidth=2)
        ax2.set_title("Body Fat %", color=text_color, fontsize=11, pad=8)
        ax2.set_ylabel("%", color=text_color)
        ax2.tick_params(colors=text_color)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        ax2.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=30, ha="right")
        ax2.spines[:].set_color(grid_color)
        ax2.grid(True, color=grid_color, alpha=0.5)
        if bodyfats:
            ax2.annotate(f"{bodyfats[-1]:.1f}%", xy=(bf_dates[-1], bodyfats[-1]),
                         xytext=(-50, 10), textcoords="offset points",
                         color="#f48fb1", fontsize=10, fontweight="bold",
                         arrowprops=dict(arrowstyle="->", color="#f48fb1", lw=1))
    else:
        ax2.text(0.5, 0.5, "No body fat data", ha="center", va="center",
                 color=text_color, transform=ax2.transAxes)

    # --- Stats panel ---
    ax3.set_facecolor("#0d0d1a")
    ax3.axis("off")

    stats = [
        ("Current", f"{current:.1f} kg"),
        ("Lost", f"{lost:.1f} kg"),
        ("Remaining", f"{remaining:.1f} kg"),
        ("Progress", f"{pct_done:.1f}%"),
    ]
    if goal_date:
        stats.append(("Goal date (est.)", goal_date.strftime("%b %d, %Y")))
        weekly_rate = slope * 7
        stats.append(("Rate", f"{weekly_rate:.2f} kg/wk"))

    y = 0.92
    ax3.text(0.5, 1.0, "Stats", ha="center", va="top", color=text_color,
             fontsize=12, fontweight="bold", transform=ax3.transAxes)
    for label, value in stats:
        ax3.text(0.05, y, label, color="#aaaaaa", fontsize=10, transform=ax3.transAxes)
        ax3.text(0.95, y, value, color=accent, fontsize=10, fontweight="bold",
                 ha="right", transform=ax3.transAxes)
        y -= 0.14

    # Progress bar
    bar_y = y - 0.05
    ax3.add_patch(plt.Rectangle((0.05, bar_y - 0.04), 0.9, 0.06,
                                  facecolor=grid_color, transform=ax3.transAxes))
    ax3.add_patch(plt.Rectangle((0.05, bar_y - 0.04), 0.9 * (pct_done / 100), 0.06,
                                  facecolor=green, transform=ax3.transAxes))
    ax3.text(0.5, bar_y - 0.12, f"{pct_done:.1f}% to goal",
             ha="center", color=green, fontsize=9, transform=ax3.transAxes)

    fig.suptitle(
        f"Warren's Weight Dashboard  •  {datetime.now().strftime('%b %d, %Y')}",
        color=text_color, fontsize=14, fontweight="bold", y=0.98
    )

    plt.savefig(PNG_PATH, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"✅ Dashboard saved to {PNG_PATH}")

if __name__ == "__main__":
    main()
