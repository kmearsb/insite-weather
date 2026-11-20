# InSite Weather: Product Requirements

**Status:** Draft v0.2 · **Updated:** 2026-11-15 · **Technical design:** [TECHNICAL_DESIGN.md](./TECHNICAL_DESIGN.md) · **Roadmap:** [ROADMAP.md](./ROADMAP.md)

† = assumption not in the original brief; needs confirmation.

## 1. Summary

InSite Weather texts industrial site operators **before** weather turns into a pollution problem. A user enters a site address, pollution concerns (dust, stormwater), phone and email. The system watches National Weather Service (NWS) forecasts and texts a recommended action ahead of risky conditions. The user replies `WATERED` or `SWEPT`, which stops further alerts for that event and creates a timestamped compliance record.

## 2. Problem

- Permits require facilities to prevent weather-driven pollution: dust from dry, gusty conditions; sediment and debris in stormwater during heavy rain.
- Nobody on site watches the forecast with pollution in mind, so the response is reactive: complaints, track-out onto roads, dirty runoff, and DEP/EPA citations.
- Usually one person runs the whole site. They want to be proactive but can't watch the sky all day.
- No simple tool turns a forecast into a site-specific "do this by then" text and records the response.

## 3. Users

**Primary user: the site operator** (e.g., quarry operations manager). Sees permit conditions as a drag on efficiency but badly wants to avoid citations. Has low web skills and texts all day. Knows the site completely.

Design principles:
- **SMS first.** Every core action works by text alone; the web app is for setup and records.
- **Plain language.** "Dry, gusty winds Thu 10am–6pm", not meteorology.
- **Few alerts.** One event per weather system, no nagging.
- **Forgiving replies.** `watered`, `Watered!` and `WATERED 2 trucks` all work.

## 4. Goals and metrics†

| Metric | Target |
|---|---|
| Sign-ups that finish onboarding | ≥ 80% |
| Action alerts answered before the event | ≥ 60% |
| Observed qualifying conditions that were alerted (recall) | ≥ 90% |
| SMS delivery success | ≥ 99% |
| Forecast pull → alert sent | ≤ 15 min |
| Sites retained at 90 days | ≥ 70% |
| **Guardrails:** monthly STOP rate < 5%; ≤ 3 alert texts per site per week on average | |

## 5. Scope

**MVP (must have)**
1. Web sign-up and log-in, with map confirmation of the site location and phone verification.
2. Scheduled NWS forecast and observation ingestion, plus a check of whether each alerted condition actually occurred (see §6.5 for what is kept).
3. SMS alerts on the 72 h / 24 h cadence, including the weekend rule.
4. Two-way SMS: replies stop alerts for the event and create compliance records.
5. STOP/HELP handling and SMS consent capture.

**Should have:** downloadable records (PDF/CSV) via log-in; adjustable sensitivity (high only vs. moderate + high); email copies of alerts; site operating days†; weather map.

**Later:** payments and subscriptions; **on-site weather station calibration** (learn how site conditions differ from the area forecast because of terrain, waterbodies and so on, then adjust alerts per site); multiple sites and recipients; more concerns.

**Out of scope:** permit interpretation, sampling or inspection tracking, non-US sites, native apps.

## 6. Requirements

### 6.1 Onboarding

1. Enter address (with autocomplete) → choose concerns → enter mobile number and email, and tick the SMS consent box → **Create account**.
2. Confirm the site on a map; drag the pin if needed. The confirmed point is what gets monitored.
3. Enter the 6-digit code texted to the phone.
4. Create a username and password ("used to access your compliance records").
5. Welcome text and email are sent, and monitoring starts. No alerts are sent before the phone is verified.

The whole flow should take under 3 minutes on a phone.†

### 6.2 Concerns and draft triggers†

Thresholds are starting points for subject-matter review, not final values.

| Concern | Action / reply | Moderate | High |
|---|---|---|---|
| **Dust** | Water roads and stockpiles / `WATERED` | Wind ≥ 15 mph or gusts ≥ 25 mph, RH ≤ 45%, < 0.10 in rain in prior 48 h | Wind ≥ 20 mph or gusts ≥ 30 mph, RH ≤ 35%, < 0.10 in rain in prior 48 h |
| **Stormwater** | Sweep, clean up, check BMPs / `SWEPT` | ≥ 0.10 in in 24 h, PoP ≥ 50% | ≥ 0.50 in in 24 h or ≥ 0.25 in in 6 h, PoP ≥ 60% |
| **Track-out** (open question) | Sweep exits / `SWEPT` | ≥ 0.10 in during operating hours | — |

Sensitivity setting: **Standard** alerts on high only; **Cautious** alerts on moderate and high (default†).

### 6.3 Alert cadence

1. **~72 h out:** heads-up only, no action needed.
2. **Weekend rule:** if the event starts on a Saturday or Sunday (later also non-operating days†), the first message asks for precautionary action before the weekend.
3. **~24 h out**, if still forecast: action alert asking the user to act and reply when done.
4. **Late detection:** if first detected under 24 h out, send the action alert immediately.
5. **Reminder†:** one reminder 6 h before the event if there's no reply.
6. **Cancellation†:** a short "no longer expected" text if the event drops out of the forecast after an alert.
7. **Quiet hours†:** nothing between 8 pm and 6 am site time.
8. Every message names the site, the risk, the time window, the action and deadline, and the reply keyword. Keep it to 2 SMS segments or fewer.

### 6.4 Replies

- The first word is the keyword; anything after it is saved as a note.
- `WATERED` → dust; `SWEPT` → stormwater/track-out; `DONE` → the only open event.
- A valid reply logs the action, stops alerts for that event and sends a confirmation with a record ID.
- If the reply is ambiguous or doesn't match an open event, answer with the open events and valid keywords.
- `STOP` / `START` / `HELP` follow carrier rules. `RECORDS` texts back a secure link.†

### 6.5 Compliance records

- Each entry holds: site, concern, event window, the triggering forecast values and their source time, alerts sent, the reply (keyword, note, time), and the observed outcome (observed / not observed / indeterminate).
- Records are append-only (corrections are new entries), stored in UTC and shown in site time.
- Compliance records exist only for events that triggered an alert. They are kept permanently, including after cancellation.
- Inputs to decisions *not* to alert are temporary. During the pilot all data is kept; after the pilot, raw weather data is kept for 5 days, and alert accuracy is kept only as daily totals.
- Downloads include a disclaimer that the record does not by itself prove permit compliance.

### 6.6 Weather data

Pull for each site, at least hourly, covering at least 5 days ahead: wind speed, gust and direction; precipitation amount and probability; max/min temperature; relative humidity. Pull the same parameters as current observations and as **observed daily summaries** from the nearest NWS station. The data drives alerts, post-event verification and the map. The forecast and observed values behind each alert are copied into its compliance record, so raw data can be deleted on schedule (§6.5).

## 7. Non-functional requirements

- **Reliability:** a missed alert is the worst possible failure. The pipeline must be idempotent, retried and alarmed, and stale data (> 3 h†) pages the team.
- **SMS compliance:** a verified toll-free sending number before launch; consent stored with timestamp and wording version.
- **Security and privacy:** phone and email encrypted at rest; signed webhooks; secrets in a managed store.
- **Usability:** mobile-first; WCAG 2.1 AA; US units; English only.

## 8. Technology

TypeScript monorepo on GitHub. Next.js on Vercel, Supabase Auth, AWS via CDK for the backend and database, Twilio texting from a verified toll-free number, Modal for Python only where needed. Details are in [TECHNICAL_DESIGN.md](./TECHNICAL_DESIGN.md).

## 9. Rollout†

Internal alpha (founder's test sites) → closed pilot with 3–10 facilities from the founder's consulting network, free in exchange for feedback → public launch with per-site subscriptions.

## 10. Risks and open questions

**Top risks:** false alarms cause users to opt out; missed alerts damage trust; toll-free verification is rejected or slow; the nearest station doesn't represent the site. Mitigations are sensitivity tiers, pipeline alarms, submitting toll-free verification on day one, and on-site calibration later.

**Open product questions**
1. Final name and domain (`insiteweather.com`)?
2. Final trigger thresholds per concern and tier?
3. Is track-out its own concern in the MVP?
4. Log in with username, email, or both?
5. Should a `NOTNEEDED` reply count as a compliance entry?
6. One site per account for the MVP?

## 11. Milestones†

| Phase | Outcome | Est. |
|---|---|---|
| 0. Foundations | Repo, CI, infrastructure skeleton; toll-free verification submitted | 1–2 wks |
| 1. Weather + rules | Events generated and checked against historical data | 3–4 wks |
| 2. Messaging | Alert → reply → record works end to end | 2–3 wks |
| 3. Web app | Onboarding, records, settings | 3–4 wks |
| 4. Pilot | Metrics tracked for 6+ weeks | 6–8 wks |
| 5. Launch | Payments, public sign-up | 2–3 wks |
