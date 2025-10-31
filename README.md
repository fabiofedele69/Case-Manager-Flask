# Banking Case Manager Application

A microservices-based Flask application for monitoring trades and managing alerts.

## Microservices
- **Trade Ingest** — Receives trades, performs validation, triggers alerts.
- **Case Manager** — Stores and tracks alert cases.
- **Postgres** — Shared persistence layer.

## Run Locally
```bash
cd infra
docker-compose up --build
