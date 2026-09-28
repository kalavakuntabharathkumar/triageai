# MCP-Powered Support Ticket Triage Agent

Production-style reference project using Python, FastAPI, PostgreSQL, Docker, MCP and pytest.

## Features
- FastAPI ticket intake and triage API
- Seven MCP tools for ticketing, CRM and knowledge-base operations
- Deterministic offline triage engine
- Optional LLM-provider boundary
- PostgreSQL persistence with SQLAlchemy
- Docker Compose
- Pytest tests and demo/seed scripts

The business metrics in the resume description are target/project-story figures. This repository
does not fabricate external production traffic; `scripts/benchmark.py` measures the local build.

## Seven MCP tools
1. get_ticket
2. search_knowledge_base
3. get_customer
4. get_customer_history
5. update_ticket
6. assign_ticket
7. record_triage_decision

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

API: http://localhost:8000/docs

Local Python:
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
pytest -q
python scripts/seed.py
python scripts/demo.py
```

## API
Create: `POST /tickets`
List: `GET /tickets`
Triage: `POST /tickets/{ticket_id}/triage`
Audit: `GET /audits/{ticket_id}`

## Optional LLM
Set `LLM_PROVIDER=openai_compatible`, `LLM_BASE_URL`, `LLM_API_KEY`, and `LLM_MODEL`.
The default `rules` mode is deterministic and requires no external credentials.
