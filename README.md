# DOGFOOD 2026 - Hackathon Judging Platform Backend

This is the backend implementation for the DOGFOOD 2026 judging platform.
It satisfies Tiers T1 and T2 completely, supporting robust judge isolation and accurate cross-judge score normalization.

## How to run

The primary way to run this backend is via Docker Compose:

```bash
docker compose up -d
```

This starts:
- The backend FastAPI application on port 8080.
- A PostgreSQL database properly seeded and migrated.

For local development without Docker, use virtual environments:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python seed.py
uvicorn app.main:app --port 8080
```

## Honest Limits
- **Roles & Permissions**: Role authorization is strict but static. Users are assigned one role at registration (Participant, Judge, Organizer).
- **Scale**: Normalization occurs in-memory. For extremely large hackathons (10,000+ submissions), this should be transitioned to a background worker to avoid blocking the HTTP request.
- **T3 & T4 features**: As prioritized by the spec ("A clean T2 beats a broken T4"), we have focused purely on achieving a flawless T2 backend. We did not build community voting or webhooks.
