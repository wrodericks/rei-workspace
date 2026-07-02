# Health Tracking — Detail

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

## Weight Trend
- 120.0 → 118.4 kg over first 3 days (good start as of 2026-04-16)
