# InSite Weather: Roadmap

See [PRD.md](./PRD.md) for requirements and [TECHNICAL_DESIGN.md](./TECHNICAL_DESIGN.md) for the build design. Durations are estimates for a small team and will change as the open questions in PRD §10.3 are resolved.

## Phase 0: Foundations (1–2 weeks)

- [ ] Repo scaffold: `apps/web` (pnpm, TypeScript), `backend` (uv, ruff, mypy, pytest), `supabase` (CLI migrations); CI on GitHub Actions
- [ ] Supabase dev and prod projects (database + Auth), with row-level security on from the first migration
- [ ] Modal dev and prod environments, with secrets
- [ ] Vercel project for `apps/web`
- [ ] Buy the Twilio toll-free number and **submit toll-free verification on day one** (texts can't be sent until it's approved; Twilio reviews within about 3 business days)
- [ ] Record the v0.2 architecture decisions (Supabase, Modal, hourly check) as ADRs

## Phase 1: Weather data and rules engine (3–4 weeks)

- [ ] `insite/weather`: NWS client (point lookup, conditional gridpoint fetch, station readings), unit conversion, interval-to-hourly expansion
- [ ] Confirm how far back NWS station readings are available (design needs about 3 days)
- [ ] `insite/core`: data-driven rules, likelihood tiers, window merging, event reconciliation
- [ ] `hourly_check` and `check_grid_cell` on Modal (evaluate and record events, no sending yet)
- [ ] Post-event verification (observed / not observed / indeterminate)
- [ ] Backtesting CLI against NOAA historical data for pilot locations

## Phase 2: Messaging (2–3 weeks)

- [ ] `insite/messaging`: Twilio and Resend adapters, templates, segment-length tests
- [ ] Alert planning and exactly-once sending inside the hourly check, with delivery receipts
- [ ] Inbound SMS webhook: keyword parsing, event matching, confirmations
- [ ] STOP / START / HELP handling and consent records
- [ ] Email fallback and transactional email
- [ ] `daily_maintenance`: accuracy roll-up, purge, nightly compliance export
- [ ] External heartbeat monitor and `system_health` checks

## Phase 3: Web app (3–4 weeks)

- [ ] Onboarding: address, concerns, contact details and consent, map confirmation, phone verification, password
- [ ] Dashboard with 5-day risk outlook
- [ ] Records page with PDF and CSV export
- [ ] Settings: concerns, sensitivity, operating days/hours, pause alerts
- [ ] Weather map overlays
- [ ] Modal web API: onboarding, outlook, records, settings
- [ ] Internal admin view

## Phase 4: Pilot (6–8 weeks)

- [ ] Onboard 3–10 facilities
- [ ] Track PRD §4.3 metrics weekly
- [ ] Tune thresholds and message copy

## Phase 5: Launch (2–3 weeks)

- [ ] Stripe subscriptions and trials
- [ ] Public sign-up, help center, terms, privacy policy, SMS terms
- [ ] Launch checklist (PRD §9.4)

## Later

- **On-site weather station calibration:** ingest data from an installed on-site station, compare it with area forecasts and nearest-station observations over time, learn site-specific biases (terrain, waterbodies, etc.), and apply them to produce a site-adjusted forecast that reduces both missed events and false alarms. Statistical modeling likely runs as Python on Modal.
- Multiple sites per account; multiple alert recipients per site
- Consultant / multi-site dashboard
- Additional concerns: freeze/thaw, extreme heat, flooding
- Secondary forecast sources (e.g., HRRR, GFS, ECMWF)
