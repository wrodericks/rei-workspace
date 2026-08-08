# Health Tracking — Detail

## Conditions / Flags
- **Gout history** — tracking purines preventively (no recent flare as of Jul 2026). Target <400mg/day.

## Stats & Goals
- 52yo, 178cm, 120kg → goal 90kg (20% body fat)
- Target: 1,900 kcal/day, 140–150g protein (revised 2026-06-30 — fat loss primary, muscle preservation)
- **Skeletal muscle goal:** 48kg by Sep 8, 2026 (baseline: 46.1kg as of Jun 6)
- **Creatine:** 5g daily (started 2026-06-07, Day 3 as of Jun 9 — full saturation ~Jul 7)
- Active program: health/ppl-program.md — 12-week PPL, Jun 6 – Sep 8
- Focus: reducing sugar/refined carbs, eliminating late-night eating
- Dropped vanilla syrup from lattes permanently (confirmed 2026-05-28)

## Setup
- Started: 2026-04-13
- Daily logs: health/logs/
- Weight log: health/weight.md
- Fitbit: connected via Google Fitness API (2026-04-15), token at credentials/google-health-token.json
  - Re-auth every 7 days (unverified app limitation) — reminder set for May 8
  - TODO: migrate to native Fitbit API for permanent tokens
- Smart scale: Renpho R-A033 — activated 2026-04-21
  - TODO: Renpho API client — reverse-engineer auth, wire into daily sync

## Cron Jobs
- 8PM ET daily — kitchen closed check-in
- 10PM ET daily — bedtime nudge
- 10:30PM — wind-down nudge
- 11:15PM — Fitbit sleep check
- 11:45PM — Fitbit sleep check
- Target bedtime: 11–11:30pm

## Energy Management Framework
Goal: consistently high energy for work, gym, and family.

### Key Levers (evidence-based)
- **Sleep** — highest leverage; consistency of wake time matters more than total hours
- **Meal composition** — protein + fat + fibre at meals slows glucose, avoids spikes/crashes
- **Meal timing** — front-load calories earlier; late heavy meals disrupt sleep and next-day energy
- **Hydration** — even mild dehydration tanks energy; unsweetened tea counts
- **Post-meal movement** — 10 min walk after eating flattens glucose spikes significantly
- **Exercise** — increases baseline energy over time; short-term fatigue, long-term gain

### Daily Energy Tracking
Rate energy at three points using: **High / Med / Low / Zero**
- **Morning** — after waking, before caffeine
- **Afternoon** — around 3pm
- **Evening** — around 8pm

Most days will be Med — that's the baseline. Definitions:
- **High** — noticeably energized
- **Med** — normal, functional baseline
- **Low** — tired, dragging, below par
- **Zero** — something went wrong (sick, very hungover, etc.) — rare

Log in daily health file under Energy Log section.

### Rei's Role
- Flag meal compositions likely to cause energy crashes (high carb + low protein/fat/fibre)
- Note sleep duration in daily logs
- Surface patterns over time (e.g. "low afternoon energy correlates with late high-carb dinners")

---

## "Totals" Command
When Warren says **"totals"**, always produce this table format showing the day's running totals vs. targets, with a status emoji:

| | Today | Target | |
|---|---|---|---|
| Calories | X | 1,900 | ✅/⚠️ |
| Protein | Xg | 140–150g | ✅/⚠️ |
| Carbs | Xg | <150g | ✅/⚠️ |
| Fat | Xg | <80g | ✅/⚠️ |
| Fibre | Xg | 25g+ | ✅/⚠️ |
| Sugar | Xg | <40g | ✅/⚠️ |
| Sodium | Xmg | <2,300mg | ✅/⚠️ |
| Purines | Xmg | <400mg | ✅/⚠️ |

Use ✅ when on target, ⚠️ when off (with a brief note). Estimate any missing micros (fibre, sugar, sodium, purines) based on foods logged. This format should be consistent across all sessions.

## Weight Trend
- 120.0 → 118.4 kg over first 3 days (good start as of 2026-04-16)

---

## Weight Regression Analysis (planned)
Goal: identify what actually drives daily weight change. Warren's hypothesis: alcohol is the biggest driver of water retention.

### Variables to test (against Δweight day-over-day)
- Alcohol (Y/N or units)
- Sodium (mg)
- Carbohydrates (g)
- Caloric surplus/deficit
- Exercise (Y/N)
- Prior day weight (autocorrelation)

### Modelling notes
- Use rolling average deficit (3-day and 5-day) rather than single-day — weight responds to cumulative energy balance
- Test rolling sodium and carbs too — water retention can persist 2-3 days
- Run both 3-day and 5-day windows, compare fit
- Simple multiple linear regression to start; check residuals for non-linearity
- Data quality caveat: food logging inconsistent early on and in Japan

### Status
Planned — run after return to Toronto (Aug 15+). Enough data (~100+ weight observations) to get meaningful results.

### Handling Incomplete Data
Five options considered:

1. **Complete cases only** — drop days with missing food data. Clean but loses data; risk of selection bias if missing days correlate with indulgent eating.
2. **Multiple imputation** — fill missing values statistically. More complex, adds noise.
3. **Segment by period** — run regression separately on well-logged periods (Toronto Apr-Jul vs. Japan Jul-Aug). Honest about data quality differences.
4. **Partial variables** — include days for variables we do have, exclude only for missing ones. Most regression frameworks handle this naturally.
5. **Simplify for sparse periods** — Japan: use alcohol Y/N, exercise Y/N, weight only. Drop nutrition variables where logging is patchy.

**Recommended approach: Option 3 + 4**
- Segment by period
- Use available variables per day
- Flag data quality explicitly
- Add a **data quality score** (0/1/2) per day as a control variable or filter

