<div align="center">

<p align="center">
  <img src="./assets/hero.svg" width="100%" alt="DOGFOOD Hackathon Judging Platform">
</p>

<h3 align="center">
  Judges evaluate projects.<br>
  The system protects the evaluation.
</h3>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.12+-0D0F0E?style=flat-square&labelColor=0D0F0E&color=B6FF3B">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-Backend-0D0F0E?style=flat-square&labelColor=0D0F0E&color=B6FF3B">
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-Database-0D0F0E?style=flat-square&labelColor=0D0F0E&color=B6FF3B">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-Ready-0D0F0E?style=flat-square&labelColor=0D0F0E&color=B6FF3B">
  <img alt="API Docs" src="https://img.shields.io/badge/API_Docs-%2Fdocs-0D0F0E?style=flat-square&labelColor=0D0F0E&color=B6FF3B">
</p>

</div>

---

# DOGFOOD

## Hackathon Judging Platform

Hackathons move fast.

Teams build.  
Judges evaluate.  
Organizers coordinate.  
Results have to be trusted.

**DOGFOOD treats judging as infrastructure — not just a form.**

It creates a controlled evaluation workflow connecting events, teams, projects, judges, scoring and results while keeping protected operations inside the backend.

<p align="center">
  <img src="./assets/problem-solution.svg" width="900" alt="Traditional judging versus DOGFOOD">
</p>

---

# THE IDEA

> **Judges evaluate projects. The system protects the evaluation.**

The judging lifecycle becomes:

```text
┌─────────────┐
│    EVENT    │
└──────┬──────┘
       ↓
┌─────────────┐
│    TEAMS    │
└──────┬──────┘
       ↓
┌─────────────┐
│   PROJECTS  │
└──────┬──────┘
       ↓
┌─────────────┐
│    JUDGE    │
│ ASSIGNMENT  │
└──────┬──────┘
       ↓
┌─────────────┐
│  ISOLATED   │
│  JUDGING    │
└──────┬──────┘
       ↓
┌─────────────┐
│    SCORE    │
│   ENGINE    │
└──────┬──────┘
       ↓
┌─────────────┐
│   RESULTS   │
└─────────────┘
```

---

# THE PROBLEM

Traditional hackathon judging can depend heavily on spreadsheets, shared links and manual coordination.

That creates operational problems around:

- judge assignment
- score visibility
- evaluation consistency
- manual calculations
- result processing
- access control

DOGFOOD moves these operations into a structured backend workflow.

<p align="center">
  <img src="./assets/problem-solution.svg" width="900" alt="From traditional judging to DOGFOOD">
</p>

---

# THE DOGFOOD APPROACH

One controlled path from event to result.

```text
EVENT
  │
  ▼
TEAMS
  │
  ▼
PROJECTS
  │
  ▼
RUBRIC
  │
  ▼
JUDGE ASSIGNMENT
  │
  ▼
EVALUATION
  │
  ▼
SCORE PROCESSING
  │
  ▼
RESULTS
```

### The backend becomes the trust layer.

- Judges access assigned projects through backend authorization.
- Evaluation data follows a structured workflow.
- Protected resources are validated server-side.
- Scoring is handled as application logic rather than spreadsheet arithmetic.
- Results can be generated from processed evaluation data.

---

# JUDGING ISOLATION

## Not hidden. **Enforced.**

A frontend restriction is not a security boundary.

DOGFOOD treats judge isolation as a backend authorization problem.

<p align="center">
  <img src="./assets/judging-isolation.svg" width="900" alt="DOGFOOD judge isolation">
</p>

```text
                     JUDGING ENGINE
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
        ┌─────────┐                 ┌─────────┐
        │ JUDGE A │                 │ JUDGE B │
        └────┬────┘                 └────┬────┘
             │                           │
       ┌─────┼─────┐               ┌─────┼─────┐
       ▼     ▼     ▼               ▼     ▼     ▼
      P01   P04   P07             P02   P05   P08
       │     │     │               │     │     │
       ▼     ▼     ▼               ▼     ▼     ▼
     SCORE SCORE SCORE           SCORE SCORE SCORE
```

A protected request follows:

```text
WHO ARE YOU?
      ↓
WHAT IS YOUR ROLE?
      ↓
WHAT ARE YOU ASSIGNED TO?
      ↓
IS THIS RESOURCE ALLOWED?
      ↓
 ┌───────────────┐
 │               │
 YES             NO
 │               │
 ▼               ▼
ACCESS       403 FORBIDDEN
```

**The server decides.**

---

# EVALUATION ENGINE

Every evaluation follows a controlled scoring path.

<p align="center">
  <img src="./assets/scoring-engine.svg" width="900" alt="DOGFOOD scoring engine">
</p>

```text
┌───────────────┐
│   CRITERIA    │
└───────┬───────┘
        ↓
┌───────────────┐
│    WEIGHTS    │
└───────┬───────┘
        ↓
┌───────────────┐
│ INDIVIDUAL    │
│    SCORES     │
└───────┬───────┘
        ↓
┌───────────────┐
│   WEIGHTED    │
│    SCORE      │
└───────┬───────┘
        ↓
┌───────────────┐
│ NORMALIZATION │
└───────┬───────┘
        ↓
┌───────────────┐
│ FINAL SCORE   │
└───────────────┘
```

The objective is simple:

**Every score should have a controlled path.**

---

# SYSTEM ARCHITECTURE

DOGFOOD separates the presentation layer from backend-owned business logic.

<p align="center">
  <img src="./assets/architecture.svg" width="950" alt="DOGFOOD system architecture">
</p>

```text
                         ┌──────────────────┐
                         │     FRONTEND     │
                         └────────┬─────────┘
                                  │
                              REST / HTTP
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │          FASTAPI          │
                    ├───────────────────────────┤
                    │                           │
                    │ Authentication            │
                    │ Authorization             │
                    │ Events                    │
                    │ Teams                     │
                    │ Projects                  │
                    │ Judge Assignment          │
                    │ Evaluation                │
                    │ Score Processing          │
                    │ Results                   │
                    │                           │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   PostgreSQL    │
                         └─────────────────┘
```

### Request lifecycle

```text
REQUEST
   │
   ▼
AUTHENTICATION
   │
   ▼
AUTHORIZATION
   │
   ▼
VALIDATION
   │
   ▼
BUSINESS LOGIC
   │
   ▼
DATABASE
   │
   ▼
RESPONSE
```

---

# SECURITY FLOW

Protected requests pass through identity, role and resource checks before business logic.

<p align="center">
  <img src="./assets/security-flow.svg" width="900" alt="DOGFOOD security flow">
</p>

```text
                 ┌─────────────┐
                 │   REQUEST   │
                 └──────┬──────┘
                        ↓
              ┌──────────────────┐
              │ JWT VERIFICATION │
              └────────┬─────────┘
                       ↓
              ┌──────────────────┐
              │    ROLE CHECK    │
              └────────┬─────────┘
                       ↓
              ┌──────────────────┐
              │ RESOURCE CHECK   │
              └────────┬─────────┘
                       ↓
              ┌──────────────────┐
              │    VALIDATION    │
              └────────┬─────────┘
                       ↓
              ┌──────────────────┐
              │  BUSINESS LOGIC │
              └────────┬─────────┘
                       ↓
              ┌──────────────────┐
              │     DATABASE     │
              └────────┬─────────┘
                       ↓
                   RESPONSE
```

Unauthorized access should terminate at the authorization layer rather than depending on frontend behaviour.

---

# FEATURES

| MODULE | PURPOSE |
|:---|:---|
| 🔑 **Authentication** | JWT-based user authentication |
| 🛡️ **Authorization** | Role and resource-level access checks |
| 🏟️ **Events** | Create and manage hackathon events |
| 👥 **Teams** | Manage participants and teams |
| 📦 **Projects** | Handle project information and submissions |
| ⚖️ **Judge Assignment** | Connect judges with assigned projects |
| 📝 **Judging** | Record structured project evaluations |
| 📊 **Scoring** | Process evaluation scores |
| 📚 **API Documentation** | Interactive OpenAPI documentation |

---

# COMPLETE EVALUATION LIFECYCLE

From submission to result.

<p align="center">
  <img src="./assets/evaluation-flow.svg" width="950" alt="DOGFOOD evaluation lifecycle">
</p>

```text
01  EVENT
     ↓
02  TEAMS
     ↓
03  PROJECTS
     ↓
04  RUBRIC
     ↓
05  JUDGE ASSIGNMENT
     ↓
06  EVALUATION
     ↓
07  SCORE VALIDATION
     ↓
08  NORMALIZATION
     ↓
09  RANKING
     ↓
10  FINAL RESULTS
```

---

# RESULTS ENGINE

Scores enter the processing layer.

```text
PROJECT SCORES
      │
      ▼
SCORE AGGREGATION
      │
      ▼
NORMALIZATION
      │
      ▼
RANKING
      │
      ▼
FINAL RESULTS
```

<p align="center">
  <img src="./assets/results-engine.svg" width="900" alt="DOGFOOD result processing engine">
</p>

The result pipeline is designed to make score processing structured and traceable.

---

# API

DOGFOOD exposes an interactive backend API.

### Base URL

```text
http://localhost:8000
```

### Interactive documentation

```text
http://localhost:8000/docs
```

The `/docs` interface provides the available API operations, request schemas and response structures.

### API areas

```text
AUTHENTICATION
│
├── Register
├── Login
└── Current User


EVENTS
│
├── Create Event
├── List Events
└── Event Details


TEAMS
│
├── Create Team
├── Team Details
└── Team Members


PROJECTS
│
├── Create Project
├── Project Details
└── Project Submission


JUDGING
│
├── Judge Assignment
├── Assigned Projects
└── Evaluation / Scores


RESULTS
│
└── Processed Results
```

---

# TECH STACK

<p align="center">
  <img src="./assets/tech-stack.svg" width="700" alt="DOGFOOD technology stack">
</p>

```text
LANGUAGE        Python 3.12+
BACKEND         FastAPI
DATABASE        PostgreSQL
ORM             SQLAlchemy
VALIDATION      Pydantic
AUTHENTICATION  JWT
MIGRATIONS      Alembic
TESTING         Pytest
CONTAINER       Docker
VERSION CONTROL Git / GitHub
```

---

# PROJECT STRUCTURE

```text
Hackathon-Judging-Platform/
│
├── README.md
│
├── assets/
│   ├── hero.svg
│   ├── problem-solution.svg
│   ├── judging-isolation.svg
│   ├── scoring-engine.svg
│   ├── architecture.svg
│   ├── security-flow.svg
│   ├── evaluation-flow.svg
│   ├── results-engine.svg
│   ├── tech-stack.svg
│   └── footer.svg
│
├── backend/
│   ├── app/
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
│
└── frontend/
```

---

# QUICK START

## Clone

```bash
git clone https://github.com/Nethralfh/Hackathon-Judging-Platform.git
cd Hackathon-Judging-Platform
```

## Backend

```bash
cd backend
```

## Create virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

## Open API

```text
http://localhost:8000
```

## Open Swagger

```text
http://localhost:8000/docs
```

---

# DOCKER

If Docker is configured for the project:

```bash
docker compose up --build
```

The backend will then run through the configured Docker service.

---

# ROADMAP

### CORE

- [x] Authentication
- [x] Event management
- [x] Team management
- [x] Project management
- [x] Judge assignment
- [x] Judging workflow
- [x] Interactive API documentation

### NEXT

- [ ] Advanced result aggregation
- [ ] Score normalization
- [ ] Ranking engine
- [ ] Result export
- [ ] Alembic migration workflow
- [ ] Expanded automated tests
- [ ] Dockerized deployment
- [ ] Frontend integration
- [ ] Advanced analytics
- [ ] Audit timeline

---

# WHY DOGFOOD?

A judging platform should not simply collect numbers.

It should preserve the path behind those numbers.

```text
WHO
 │
 ▼
JUDGED WHAT
 │
 ▼
UNDER WHICH CRITERIA
 │
 ▼
WITH WHICH SCORE
 │
 ▼
PROCESSED HOW
 │
 ▼
RESULTED IN WHAT
```

That is the idea behind DOGFOOD.

**Make the evaluation structured.**

**Make access controlled.**

**Make the result traceable.**

---

# VISION

<p align="center">
  <img src="./assets/footer.svg" width="700" alt="DOGFOOD Build Judge Trust">
</p>

<div align="center">

# ⚡ DOGFOOD

### BUILD. JUDGE. TRUST.

**Hackathon Judging Platform**

<br>

`SECURE` · `ISOLATED` · `STRUCTURED` · `TRACEABLE`

<br><br>

**Judges evaluate projects.**

**The system protects the evaluation.**

<br>

---

### Built for hackathons.
### Engineered for trusted evaluation.

<br>

⭐ **Star the repository if you find the project interesting.**

</div>
