# InSite Weather

Proactive, text-based weather alerts that help industrial facilities prevent weather-driven pollution (fugitive dust, stormwater) and keep a record of their compliance efforts.

Users enter their site location, pollution concerns, phone number and email. The system monitors National Weather Service forecasts and observations, texts the user ahead of risky conditions with a recommended action, and logs replies such as `WATERED` or `SWEPT` as compliance records.

## Documentation

- [Product requirements (PRD)](docs/PRD.md)
- [Technical design](docs/TECHNICAL_DESIGN.md)
- [Roadmap](docs/ROADMAP.md)
- [Research: alert thresholds](docs/research/ALERT_THRESHOLDS.md)

## Planned repository layout

```
apps/web/        Next.js website (Vercel), TypeScript
backend/         Python back end deployed to Modal: rules engine, hourly check, web API, Twilio webhooks
supabase/        Database migrations, row-level security policies, seed data
docs/            PRD, technical design, roadmap, architecture decision records
```

## Stack

Next.js (TypeScript) on Vercel for the website; Python on Modal for the back end; Supabase for the database and authentication; Twilio (verified toll-free number) for texts; Resend for email.
