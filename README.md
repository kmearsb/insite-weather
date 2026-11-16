# InSite Weather

Proactive, text-based weather alerts that help industrial facilities prevent weather-driven pollution (fugitive dust, stormwater) and keep a record of their compliance efforts.

Users enter their site location, pollution concerns, phone number and email. The system monitors National Weather Service forecasts and observations, texts the user ahead of risky conditions with a recommended action, and logs replies such as `WATERED` or `SWEPT` as compliance records.

## Documentation

- [Product requirements (PRD)](docs/PRD.md)
- [Technical design](docs/TECHNICAL_DESIGN.md)
- [Roadmap](docs/ROADMAP.md)

## Planned repository layout

```
apps/web/        Next.js web app (Vercel)
services/        AWS Lambda handlers (ingest, evaluate, notify, inbound-sms, verify)
packages/core/   Rules engine and event state machine
packages/weather NWS client and weather data utilities
packages/messaging SMS and email adapters and templates
packages/db/     Database schema and migrations
infra/           AWS CDK infrastructure
python/          Modal functions (only where scientific computing requires Python)
docs/            PRD, roadmap, architecture decision records
```

## Stack

TypeScript, Next.js on Vercel, Supabase Auth, AWS (CDK, Lambda, EventBridge, SQS, S3, Postgres), Modal for Python jobs when needed.
