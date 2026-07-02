# DEPENDENCIES.md — Open Source Inventory

This file tracks all third-party open source software installed or used on DeepThought.
Updated as new libraries are added.

---

## System (apt / Ubuntu)

| Package | Version | Purpose | License |
|---|---|---|---|
| openjdk-17-jre | 17.0.18 | Java runtime — required to run IB Gateway | GPL v2 w/ Classpath Exception |
| python3-pip | (system) | Python package installer | MIT |
| python3-venv | (system) | Python virtual environments | PSF |

---

## Python — IBKR Trading (`~/ibkr/venv`)

| Package | Version | Purpose | License |
|---|---|---|---|
| ib-insync | 0.9.86 | Python API for Interactive Brokers TWS/Gateway | BSD 2-Clause |
| numpy | 2.4.4 | Numerical computing (ib_insync dependency) | BSD 3-Clause |
| eventkit | 1.0.3 | Event-driven utilities (ib_insync dependency) | BSD 2-Clause |
| nest-asyncio | 1.6.0 | Nested asyncio event loops (ib_insync dependency) | BSD 2-Clause |

---

## Node.js — OpenClaw Workspace (`~/.openclaw/workspace`)

| Package | Version | Purpose | License |
|---|---|---|---|
| nodemailer | 8.0.4 | Sending email via Gmail SMTP | MIT |

## Node.js — Scripts (`~/.openclaw/workspace/scripts`)

Used for browser automation scripts (Google Flights, LegisInfo, etc.)

| Package | Purpose | License |
|---|---|---|
| playwright | Browser automation framework | Apache 2.0 |
| playwright-core | Core Playwright engine | Apache 2.0 |
| playwright-extra | Playwright plugin framework | MIT |
| playwright-extra-plugin-stealth | Evades bot detection in browsers | MIT |
| puppeteer-extra-plugin-stealth | Stealth plugin (puppeteer compat layer) | MIT |
| puppeteer-extra-plugin | Plugin base class | MIT |
| puppeteer-extra-plugin-user-data-dir | User data dir management | MIT |
| puppeteer-extra-plugin-user-preferences | Browser preference management | MIT |
| fs-extra | Extended file system utilities | MIT |
| merge-deep / deepmerge | Deep object merging | MIT |
| glob | File pattern matching | ISC |
| debug | Debug logging utility | MIT |
| ms | Millisecond time parsing | MIT |

> Note: Playwright was invoked via `npx playwright` (temporary download) for the Google Flights and LegisInfo scripts. A full install also exists in `scripts/node_modules`.

---

## Third-Party Software (not open source)

| Software | Version | Purpose |
|---|---|---|
| IB Gateway | 1037 | Interactive Brokers trading gateway — closed source, free to use with IBKR account |

---

## AI & Platform APIs (via OpenClaw)

| Service | Used for | Who calls it | Cost |
|---|---|---|---|
| Anthropic Claude (claude-sonnet-4-6) | Main AI assistant (Rei) | OpenClaw core | Per token — your Anthropic credits |
| Google Gemini + Search grounding | `web_search` tool — research, web queries | OpenClaw web_search tool | Configured in OpenClaw |
| Telegram Bot API | Messaging channel — sending/receiving messages | OpenClaw messaging layer | Free (bot API) |

---

## Data Sources & External APIs

| Source | Used for | Status | Cost | Notes |
|---|---|---|---|---|
| IBKR historical data API | FX pair historical prices | ✅ Active | Free with IBKR account | Via ib_insync, no separate key needed |
| Yahoo Finance (unofficial) | FX historical data (early exploration) | ⛔ Replaced | Free | Unofficial API, no key, rate-limited. Replaced by IBKR direct. |

---

## Discussed / Considered But Not Used

| Tool / Service | What it does | Why considered | Decision |
|---|---|---|---|
| Playwright | Browser automation library (Python/Node) | Used for Google Flights and LegisInfo scraping | Active — installed in scripts/node_modules |
| IBC (IbcAlpha/IBC) | Automates IB Gateway headless login | Needed for auto-start on reboot | Deferred — using manual start + alert for now |
| Xvfb | Virtual display for headless GUI apps | Required by IBC for headless IB Gateway | Deferred — same as above |
| IBKR Client Portal API | REST-based IBKR API | Alternative to IB Gateway | Rejected — requires manual re-auth every 24h, not suitable for unattended automation |
| Brave Search API | Web search | Built into OpenClaw for general research | Available but no API key configured yet |

---

*Last updated: 2026-04-08*
