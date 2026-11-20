# InSite Weather: Roadmap

See [PRD.md](./PRD.md) for requirements and [TECHNICAL_DESIGN.md](./TECHNICAL_DESIGN.md) for the build design. Durations are estimates for a small team and will change as the open questions in PRD §10.3 are resolved.

## Phase 0: Foundations (1–2 weeks)

- [ ] Monorepo tooling (pnpm workspaces, Turborepo, TypeScript, lint/format, CI on GitHub Actions)
- [ ] AWS CDK app skeleton with dev and prod stages
- [ ] Vercel project for `apps/web`
- [ ] Supabase project for authentication
- [ ] Buy the Twilio toll-free number and **submit toll-free verification on day one** (texts can't be sent until it's approved; Twilio reviews within about 3 business days)
- [ ] Decide database host (AWS Postgres vs. Supabase Postgres) and record it as an ADR

## Phase 1: Weather data and rules engine (3–4 weeks)

- [ ] `packages/weather`: NWS client (point lookup, gridpoint forecast, station observations), unit conversion, interval-to-hourly expansion
- [ ] Ingestion services with per-grid-cell fan-out, raw payload storage in S3, freshness alarms
- [ ] Observed daily summaries computed from station observations
- [ ] `packages/core`: data-driven rules, likelihood tiers, event grouping and state machine
- [ ] Post-event verification (observed / not observed / indeterminate)
- [ ] Backtesting harness against historical data for pilot locations

## Phase 2: Messaging (2–3 weeks)

- [ ] `packages/messaging`: provider adapters, templates, segment-length tests
- [ ] Outbound queue with idempotent sends and delivery receipts
- [ ] Inbound SMS webhook: keyword parsing, event matching, confirmations
- [ ] STOP / START / HELP handling and consent records
- [ ] Email fallback and transactional email

## Phase 3: Web app (3–4 weeks)

- [ ] Onboarding: address, concerns, contact details and consent, map confirmation, phone verification, password
- [ ] Dashboard with 5-day risk outlook
- [ ] Records page with PDF and CSV export
- [ ] Settings: concerns, sensitivity, operating days/hours, pause alerts
- [ ] Weather map overlays
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
