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
