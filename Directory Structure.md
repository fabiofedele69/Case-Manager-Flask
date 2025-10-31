banking-case-manager/
├─ .devcontainer/
│  └─ devcontainer.json
├─ charts/
│  ├─ trade-ingest/
│  │  ├─ Chart.yaml
│  │  ├─ values.yaml
│  │  └─ templates/
│  │     ├─ deployment.yaml
│  │     └─ service.yaml
│  └─ case-manager/
│     ├─ Chart.yaml
│     ├─ values.yaml
│     └─ templates/
│        ├─ deployment.yaml
│        └─ service.yaml
├─ .github/
│  └─ workflows/
│     └─ ci.yml
├─ infra/
│  └─ docker-compose.yml
├─ trade-ingest/
│  ├─ app.py
│  ├─ Dockerfile
│  └─ requirements.txt
├─ case-manager/
│  ├─ app.py
│  ├─ models.py
│  ├─ Dockerfile
│  └─ requirements.txt
└─ README.md
