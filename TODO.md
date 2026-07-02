# TODO.md — Warren's To-Do List

Last updated: 2026-04-24

---

## 🧠 Leadership & New Role
- [ ] **Transformation leadership session** — once job is confirmed, dedicated thinking session on competencies, stakeholder mapping, first 90 days. Lean on Rei throughout. See details/leadership-transformation.md

## 🧠 AI / Context & Architecture
- [ ] **Diagnose memory search issue** — run `openclaw status` and investigate why memory_search returned no results on 2026-06-06 session start. Possible indexing issue. Warren to paste output when available.
- [ ] **Clean up TODO.md vs MEMORY.md overlap** — remove project descriptions from TODO.md (just action items + links to details/), remove action items from MEMORY.md (pure context only)


- [x] **Context segmentation framework** — done 2026-05-03. Trimmed all major files, moved details to details/ folder, pointers in MEMORY.md. 66% reduction in auto-loaded context.
- [x] **Education session: Rei's context files** — done 2026-05-03. Covered context files, tokens, heartbeats, crons, Gateway daemon.
- [ ] **Code inventory** — maintain a living document (`CODE_INVENTORY.md`) summarizing every script/file Rei has built, its purpose, inputs/outputs, and status
- [ ] **Code walkthrough session** — go through all code files Rei has built together, review what they do

## ✈️ Japan Prep (depart July 2)

- [ ] **OpenClaw travel setup** — install OpenClaw on travel laptop, port workspace/context/credentials/scripts
- [ ] **IB Gateway auto-start fix** — must work before Japan (reboot resilience)
- [ ] **Full reboot test** — verify everything comes back up automatically after reboot
- [ ] **Cron jobs on travel laptop** — replicate FX monitor, health cron jobs
- [ ] **Test end-to-end from laptop** — Telegram → Rei → IBKR, health logging, etc.
- [ ] Deadline: late June

## 🧹 Cleanup
- [ ] **Workspace code review + cleanup** — review scripts/ contents before archiving/deleting. Candidates: bill-c15/ica/legisinfo research files, flight search JS scripts, one-off tools. Then delete scripts/node_modules (18MB). Do after git is set up so everything is tracked first.

## 🔧 Tech / Infrastructure

- [x] **Fitbit OAuth re-auth** — done 2026-05-02. Re-auth reminder set for May 23. Tokens expire every 7 days (unverified app limitation).
- [x] **Renpho API client** — done 2026-05-16. Package installed, sync working, 9pm cron active.
- [ ] **Renpho → Google Health weight push** — auto-push weight from Renpho sync to Google Health API nightly. Write endpoint partially built in renpho-sync.py but Google's API returns inconsistent errors (new API, thin docs). Revisit after May 19 Fitbit → Google Health migration settles. Also check if Renpho's native Fitbit integration starts working on its own.
- [ ] **Proactive activity check-in crons** — scheduled crons that pull Fitbit data mid-day and evening to give proactive nudges: e.g. steps warning at 6pm if under target, calorie deficit check, sleep summary in the morning. On-demand pull already works; this adds proactive alerts.
- [ ] **IBKR compliance approval** — email compliance to get permission to open live account. Deadline: before June BOJ meeting. Warren said he'd do this Tuesday May 19. ⚠️ *Cron check 7pm May 19: no confirmation received — follow up with Warren.*
- [ ] **IBKR live account funding** — deposit $5,000 CAD, convert to JPY manually once live account open. Target: before June BOJ hike.
- [ ] **IBKR live switch** — when ready, flip port 4002 → 7497 in monitor.py and trade.py
- [x] **IB Gateway auto-start** — done 2026-05-18. IBC installed, systemd user service auto-restarts Gateway and handles login. No manual intervention needed.


## 🏥 Health Data

- [ ] **Health data consolidation** — unify all health data into a single local store: Fitbit (TDEE, steps, sleep, HR), Renpho (weight, body comp), and food logs (calories, macros, nutrition). Fix sync gaps and failures. Goal: one complete daily record per day, structured for analytics. Once we have enough data (~4-6 weeks), start doing trend analysis, correlation work (sleep vs. weight, calories vs. deficit, etc.).
- [ ] **Fitbit sync crons** — restore daily Fitbit pulls: morning (~8am) for yesterday's sleep + final TDEE, evening (~9pm) for today's running burn total. Old 7am cron was dropped at some point.
- [ ] **Telegram → script hooks** — build `message:received` hooks that pattern-match specific Telegram commands (e.g. `/fitbit-sync`, `/renpho-sync`) and execute scripts directly without going through the LLM. Zero token cost, reliable triggers. Build alongside health data consolidation.

## 📱 Health App

- [ ] **Install Windsurf** — free IDE with agentic coding, for tinkering with the health app locally
- [ ] **First Claude Code session** — scaffold Expo app + Supabase schema (accounts created: Expo + Supabase ✅)

## 💰 FX / IBKR

- [ ] **Monitor CADJPY exit signal** — target ~p75 (~107–108 range). Paper trade active as of 2026-04-24.

---

## ✅ Done
- [x] Email setup (rei.deepthought@gmail.com) — 2026-04-05
- [x] IBKR paper trading pipeline — monitor.py, trade.py, signal flow — 2026-04-08
- [x] FX dashboard + email — 2026-04-09
- [x] Health tracking system — daily logs, weight log — 2026-04-13
- [x] Fitbit/Google Fitness API connected — 2026-04-15
- [x] Renpho R-A033 scale activated — 2026-04-21
- [x] Full health app product spec — 2026-04-19
- [x] Expo + Supabase accounts created — 2026-04-19
