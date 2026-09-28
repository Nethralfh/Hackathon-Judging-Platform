<p align="center">
  <img src="./assets/hero.svg" width="100%" alt="DOGFOOD Hackathon Judging Platform" />
</p>

<h3 align="center">Judges evaluate projects.<br/>The system protects the evaluation.</h3>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.12+-0D0F0E?style=flat-square&labelColor=0D0F0E&color=B6FF3B" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-backend-0D0F0E?style=flat-square&labelColor=0D0F0E&color=B6FF3B" />
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-database-0D0F0E?style=flat-square&labelColor=0D0F0E&color=B6FF3B" />
  <img alt="API docs" src="https://img.shields.io/badge/API_docs-%2Fdocs-0D0F0E?style=flat-square&labelColor=0D0F0E&color=B6FF3B" />
</p>

---

## The problem

Hackathon judging usually runs on spreadsheets, shared links and trust.
Scores are visible to the wrong people. Totals are added by hand. Nobody can say how a ranking was produced.

<p align="center">
  <img src="./assets/problem-solution.svg" width="900" alt="Traditional judging versus DOGFOOD" />
</p>

## The DOGFOOD approach

One path from event to result. Every step is checked by the backend.

- Judges see only the projects assigned to them.
- Scores are stored against a rubric, not typed into a sheet.
- Results come from processed scores, not manual totals.

> **The backend is the trust layer.**

---

## Judging isolation

Not hidden. **Enforced.**

Every evaluation request is checked against the judge's identity and assignment on the server. If a judge is not assigned to a project, the request ends in `403 Forbidden`. The interface is never the security boundary.

<p align="center">
  <img src="./assets/judging-isolation.svg" width="900" alt="Judge A and Judge B are isolated by backend access control" />
</p>

## Evaluation engine

Every score has a controlled path: criteria, weights, weighted score, normalization, final score.

<p align="center">
  <img src="./assets/scoring-engine.svg" width="900" alt="Scoring engine: weighted score, normalization, final score" />
</p>

## Architecture

Separate frontend. Backend-owned logic.

<p align="center">
  <img src="./assets/architecture.svg" width="950" alt="DOGFOOD system architecture" />
</p>

## Security

Requests pass identity, role and resource checks before any business logic runs.

<p align="center">
  <img src="./assets/security-flow.svg" width="900" alt="Backend request security flow" />
</p>

---

## Features

| Module | What it does |
| --- | --- |
| Authentication | JWT-based login and identity |
| Authorization | Role and resource checks on every protected route |
| Events | Create and manage hackathon events |
| Teams | Register and manage teams |
| Projects | Submit and manage projects |
| Judging | Assign judges and record evaluations |
| Scoring | Structured criteria and score processing |
| API docs | Interactive OpenAPI documentation |

> Status reflects the current backend. Result ranking, export and further modules are tracked in the [roadmap](#roadmap).

## Lifecycle

From submission to ranking.

<p align="center">
  <img src="./assets/evaluation-flow.svg" width="950" alt="Ten-stage judging lifecycle" />
</p>

## Results

Scores in. Ranking out. No manual totals.

<p align="center">
  <img src="./assets/results-engine.svg" width="900" alt="Result engine: aggregation, normalization, ranking" />
</p>

---

## API

The backend serves interactive documentation.

```
http://localhost:8000/docs
```

Endpoints are grouped by resource: authentication, events, teams, projects, judging and scoring. The `/docs` page is the source of truth for routes and schemas.

## Tech stack

<p align="center">
  <img src="./assets/tech-stack.svg" width="700" alt="Python, FastAPI, PostgreSQL, SQLAlchemy, Pydantic, JWT, Alembic, Pytest, Docker, GitHub" />
</p>

## Project structure

```
.
├── assets/        README visuals
├── backend/       FastAPI application
└── frontend/      Client application
```

Adjust this tree to match the repository as it grows.

## Quick start

```bash
git clone https://github.com/Nethralfh/Hackathon-Judging-Platform.git
cd Hackathon-Judging-Platform/backend

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```

Open <http://localhost:8000/docs>.

Requires Python 3.12+ and a running PostgreSQL instance. Set your database URL and JWT secret in a local `.env` file, never in the repository.

## Roadmap

- [x] Authentication
- [x] Events, teams and projects
- [x] Judge assignment and scoring
- [x] Interactive API documentation
- [ ] Result aggregation, normalization and ranking
- [ ] Result export
- [ ] Alembic migrations
- [ ] Automated test coverage with Pytest
- [ ] Docker setup
- [ ] Frontend integration

## Vision

A judging system that a team can defend.
When someone asks how a ranking was produced, the answer is in the data, not in a spreadsheet.

---

<p align="center">
  <img src="./assets/footer.svg" width="700" alt="DOGFOOD. Build. Judge. Trust." />
</p>
