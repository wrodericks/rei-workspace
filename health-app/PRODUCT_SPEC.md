# Health Coach App — Product Spec
*Last updated: 2026-04-19*

---

## Vision

A conversational AI health coach that helps 50+ professionals lose weight, reclaim their energy, and perform at their best — built for how their body actually works after 50.

**Not** a passive data tracker. An active planning partner.

---

## Founding Philosophy

This project has three goals, in order of priority:

1. **Build something that works exceptionally well for Warren** — he is the primary user and the prototype. If it works for him, it works for many. Solve the problem deeply and authentically before generalizing.
2. **Learn the process** — understand how commercial applications are built end-to-end, including all the steps involved in going from idea to shipped product.
3. **Experience AI-assisted development** — use Claude Code and AI tooling as the primary development engine. Document what works and what doesn't.

**On commercial potential:** If the product is genuinely effective, monetization is a solvable problem later. It is never the hard part. The hard part is building something people actually want to use every day. Money follows value — don't optimize for it prematurely.

**On scope:** Don't rush toward enterprise readiness, pricing tiers, or scale. Build for one user first. Get it right. Then extrapolate.

---

## Target Market

- **Primary:** 50+ professionals (40+ also resonant)
- Time-poor, stressed, real metabolic challenges
- Not being served well by apps designed for 25-year-olds chasing abs
- **Prototype user:** Warren (this system is the beta)

---

## Goals / Objectives (user-selectable at onboarding)

1. **Weight loss** — calorie deficit, macro tracking, trend analysis
2. **Energy maximization** — sleep quality, HRV, blood sugar stability, readiness scores
3. Both simultaneously (common for target market)

---

## Go-to-Market

- **V1: B2C** — beta via personal network, low friction, can be imperfect
- **Later: B2B / Enterprise** — employer wellness, individual vs. enterprise pricing tiers
- Design for enterprise from day one (data model, auth, admin layer) without building it yet

---

## Core Features — V1

### 1. Nutrition Plan
- AI-generates initial macro/micro targets based on user goal at onboarding
- User can override any target manually
- Tracks: calories, protein, carbs, fat, fibre, caffeine (for energy goal)
- Schema ready for future expansion: sodium, purines, GI, iron, B12, magnesium, vitamin D
- **Scope:** Weight management tool only. Not medical advice. Standard disclaimer throughout.

### 2. Food Logging
Frictionless multi-modal logging:
- 📸 **Photo** — AI vision estimates dish + portion size (primary modality)
- 🎤 **Voice** — quick verbal logging, corrections ("that's two pieces not one")
- 📦 **Barcode scan** — packaged food, exact data, fastest for known items
- ⭐ **Favourites / meal templates** — one tap for repeat meals
- 🍽️ **Restaurant integration** — pull menu nutrition data by restaurant name (V1 or V2)

Photo + voice are complementary: photo handles *how much*, voice handles *what* and corrections.

**Food database requirements:**
- Strong Japanese food coverage (target market travels; Warren's use case)
- Major Western cuisines standard

### 3. Daily Dashboard
The motivational engine. Front and centre:
- Calories consumed vs. budget (remaining for the day)
- Macros breakdown
- Calories burned (from wearable)
- **Calorie deficit for the day** (burned − consumed)
- Weight today vs. trend
- Time-stamped food log

Views: daily, weekly, monthly trend

### 4. Wearable Integration
- **Fitbit** (primary — Warren's device)
- **Apple Watch, Garmin** (also supported)
- Via Apple Health / Google Fit as catch-all
- Data pulled: calories burned, steps, active minutes, sleep duration, sleep stages, HRV, resting heart rate, skin temperature
- **Smart scale integration:** Withings, Garmin, Renpho, and any that sync via Apple Health / Google Fit
- Inactivity nudges: handled by wearable itself — app does NOT duplicate this

### 5. Calorie Deficit Tracking
- Formula: Deficit = Calories burned (wearable) − Calories consumed (food log)
- Displayed daily on dashboard
- Tracked over time — deficit vs. actual weight loss correlation view
- Noise caveat surfaced to user (water weight, sodium, sleep create day-to-day noise; weekly trends are more meaningful)

### 6. Proactive AI Coaching
- **Morning check-in** — brief daily conversation: what's your day like, any eating challenges ahead? AI plans around reality, not an ideal day
- **Meal-time prompts** — before each meal, surfaces where user stands and what to prioritize ("you're 40g short on protein, lunch is your chance")
- **Real-time course correction** — after each meal logged, AI suggests next meal based on gaps ("breakfast was high sodium, low fibre — a salad with chicken for lunch balances that")
- **End-of-day summary** — how did today go, what patterns are emerging, what should tomorrow look like
- Calendar context: captured via morning check-in conversation (manual, not automatic feed), not a formal calendar integration in V1

### 7. Sleep Tracking
- Sleep data from wearable (duration + stages)
- Sleep quality flagged on dashboard
- Wind-down nudges (evening) and sleep-past-target check-ins via push notification
- Bedtime target user-configurable
- Morning readiness context surfaced based on last night's sleep

### 8. Water Tracking
Treated with the same rigour as food — target, logging, dashboard, nudges.

- **Target:** AI-suggested based on body weight (~35ml/kg/day) at onboarding; user-overridable
- **Logging:** Quick-tap options (glass, bottle, custom amount) — minimal friction
- **Dashboard:** Daily progress toward target, displayed alongside food and deficit
- **Proactive nudges:** If falling behind mid-day, AI prompts to drink. Cadence adapts — more frequent if consistently behind, quieter if consistently on track
- **Trend tracking:** Daily water consumption logged over time
- **Correlation data:** Water intake included as a variable in long-term weight loss correlation analysis (V2/V3 ML layer)

*Note for 50+ users: thirst mechanism weakens with age — passive "drink when thirsty" is not reliable. Active tracking and nudges are especially important for this demographic.*

### 9. Reporting & Trends
- Daily / weekly / monthly breakdowns
- Deficit vs. weight loss correlation over time
- Consistency / streak metrics
- Cause-and-effect data view: "on weeks where I averaged 500 cal deficit, I lost X kg"

### 10. Energy Goal Features (if user selects energy objective)
- Daily energy self-rating (1-5) in morning check-in
- Caffeine logged and tracked (cutoff time flagged)
- Blood sugar stability framing in meal suggestions (low GI, pair carbs with protein/fat)
- Dashboard reframed around energy language, not just weight
- HRV + sleep quality as primary readiness proxies

---

## Data Schema — Collect Now, Use Later

Build schema to accommodate these from day one even if not surfaced in V1:

- HRV (heart rate variability)
- Sleep stages (deep, REM, light %)
- Resting heart rate trend
- Skin temperature
- Stress level (1-5 self-reported)
- Alcohol consumption
- Caffeine intake + timing
- Meal timing (not just what, but when)
- Travel / location context
- Weekend vs. weekday flag
- Social eating context (alone vs. with others)

**Design principle:** Collect schema-ready; surface collection gradually via opt-in as user settles in. Don't overwhelm on day one.

---

## ML / Personalization Layer — V2/V3

Needs ~90 days of consistent data before meaningful patterns emerge. Build data collection right from day one.

Potential insights:
- "Your weight loss correlates more with sleep quality than calorie deficit"
- "High sodium days create 3-4 days of water retention noise"
- "Your best weeks follow days where protein exceeded 140g"
- Crash pattern detection: "you crash at 3pm after less than 6.5h sleep"
- Daily readiness score synthesized from HRV + sleep + resting HR
- Energy forecast based on last night's data

---

## Technical Architecture

### Frontend
- Mobile-native app (React Native or Flutter)
- iOS + Android
- Local-first: data lives on device, syncs to cloud
- Works offline; queues logs and syncs on reconnect
- **Works anywhere** — same experience in Toronto or Tokyo

### Backend
- Lightweight (Supabase + simple API layer is sufficient for beta)
- Handles: AI calls, auth, data sync, wearable OAuth
- **Enterprise-ready data model from day one:**
  - Users belong to accounts, accounts can belong to orgs
  - Data isolation between orgs
  - Auth layer supports SSO/SAML later (use Auth0, Clerk, or Supabase Auth)
  - Admin/aggregate reporting concept in schema (not built in V1)

### AI Layer
- Cloud LLM (OpenAI / Anthropic) — cannot run on-device at quality required
- Vision model for photo food analysis
- Whisper or equivalent for voice transcription

---

## Explicitly Out of Scope — V1

- Medical condition tracking / advice (legal/regulatory risk)
- Workout logging / exercise planning (wearable handles activity)
- Inactivity nudges (wearable handles this)
- Formal calendar integration (manual via morning check-in)
- Voice interface as primary interaction mode (V2)
- Japanese health culture brand development (later version)
- ML personalization (needs data first — V2/V3)
- Restaurant integration (V1 or V2 — TBD)
- B2B / enterprise features (architecture ready, not built)

---

## Tech Stack — Decided 2026-04-19

| Layer | Choice | Why |
|-------|--------|-----|
| Mobile | Expo (React Native) | Solo-friendly, one codebase for iOS + Android, AI tools know it extremely well |
| Backend | Supabase | All-in-one (DB, auth, storage, edge functions), enterprise-ready, generous free tier |
| AI | OpenAI (GPT-4o + Vision + Whisper) | Text, vision, and voice under one integration; most mature tooling |
| Notifications | Expo Push | Built in, trivial to set up |
| Hosting | Supabase + Railway | Minimal infrastructure to manage |

**Development approach:** Solo founder (Warren) + Claude Code (via Rei) for code generation. No co-founder in V1.

---

## Open Questions

1. Pricing model for B2C ($15-30/month range typical for health apps)
2. App store strategy — TestFlight beta first?

---

## Next Steps

1. Warren continues as prototype user — build his system well first
2. Revisit tech stack decision (need to pick before building)
3. Co-founder question — decide before or after prototype?
4. Voice interface for Warren personally: test Telegram voice messages with Whisper transcription
