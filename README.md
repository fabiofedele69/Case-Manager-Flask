# Case-Manager-Flask

# 🏦 Banking Case Manager Application

Flask-based microservice system for monitoring trades and generating alerts.

## Features
- Trade ingestion API
- Simple alerting rule engine
- PostgreSQL persistence
- Containerized with Docker
- Helm chart for AKS deployment
- Reproducible DevPod environment

## Quick Start (Local Dev)
```bash
# 1. Start DevPod environment
devpod up

# 2. Run locally with Docker Compose
cd infra
docker-compose up --build

# 3. Test endpoint
curl -X POST http://localhost:8080/trades \
  -H "Content-Type: application/json" \
  -d '{"trade_id": "T1", "instrument": "AAPL", "amount": 150000, "currency": "USD"}'
