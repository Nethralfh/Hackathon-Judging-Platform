<div align="center">

# ⚡ DOGFOOD

### HACKATHON JUDGING PLATFORM

**Where evaluation becomes infrastructure.**

<br>

<img src="https://d112y698adiu2z.cloudfront.net/photos/production/challenge_thumbnails/004/714/391/datas/original.png" width="900" alt="Hackathon">

<br><br>

### `MANAGE` · `EVALUATE` · `ISOLATE` · `SCORE` · `RANK`

<br>

![Python](https://img.shields.io/badge/Python-3.12+-111111?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-111111?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-111111?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-111111?style=for-the-badge&logo=docker&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Tested-111111?style=for-the-badge&logo=pytest&logoColor=white)

</div>

---

## 01 — THE THOUGHT

> **A hackathon is only as fair as the system doing the judging.**

Hackathons move fast.

Teams build.  
Judges evaluate.  
Organizers coordinate.  
Results have to be trusted.

**DOGFOOD treats judging as infrastructure — not just a form.**

It provides a controlled backend for managing hackathons, teams, projects, judges, evaluations and final results while enforcing access at the system level.

---

<div align="center">

<img src="https://rajeevg.com/images/blog/hackathon-voting-app/hackathon-live-desktop-clean.png" width="850" alt="Hackathon Judging">

</div>

---

# 02 — FROM CHAOS → CONTROL

```text
┌──────────────────────────────────────────────────────────┐
│                    TRADITIONAL FLOW                      │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Teams → Submissions → Judges → Spreadsheets → Results  │
│                         │                                │
│                         ├── Manual coordination          │
│                         ├── Score visibility             │
│                         ├── Inconsistent evaluation      │
│                         └── Result processing            │
│                                                          │
└──────────────────────────────────────────────────────────┘


                           ↓


┌──────────────────────────────────────────────────────────┐
│                         DOGFOOD                          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  EVENT → TEAMS → PROJECTS → ASSIGNMENTS → JUDGING       │
│                                             │            │
│                                             ▼            │
│                                      SCORE ENGINE        │
│                                             │            │
│                                             ▼            │
│                                      FINAL RESULTS       │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### The principle is simple.

**Judges evaluate projects.**

**The system protects the evaluation.**

---

# 03 — THE EXPERIENCE

<div align="center">

<img src="https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/003/809/365/datas/original.png" width="900" alt="Hackathon Dashboard">

</div>

<br>

One platform for the complete hackathon evaluation lifecycle.

| Stage | Operation |
|:---:|:---|
| `01` | **CREATE** — Configure the hackathon |
| `02` | **ORGANIZE** — Manage teams and participants |
| `03` | **SUBMIT** — Collect project submissions |
| `04` | **DEFINE** — Configure evaluation rubrics |
| `05` | **ASSIGN** — Allocate projects to judges |
| `06` | **EVALUATE** — Conduct isolated judging |
| `07` | **PROCESS** — Calculate and normalize scores |
| `08` | **PUBLISH** — Generate final results |

---

# 04 — THE CORE

## 🔐 JUDGE ISOLATION

### Not hidden. Enforced.

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
          ┌──────┼──────┐             ┌──────┼──────┐
          ▼      ▼      ▼             ▼      ▼      ▼
         P01    P04    P07           P02    P05    P08
          │      │      │             │      │      │
          ▼      ▼      ▼             ▼      ▼      ▼
        SCORE  SCORE  SCORE         SCORE  SCORE  SCORE
```

A judge's evaluation belongs to that judge.

The authorization layer validates:

```text
WHO ARE YOU?
      ↓
WHAT IS YOUR ROLE?
      ↓
WHAT ARE YOU ASSIGNED TO?
      ↓
ARE YOU ALLOWED TO ACCESS THIS RESOURCE?
      ↓
YES ───────────────→ RESPONSE
NO  ───────────────→ 403 FORBIDDEN
```

This makes authorization part of the **backend architecture**, not merely a frontend restriction.

---

# 05 — SYSTEM ARCHITECTURE

```text
                         ┌───────────────────┐
                         │     FRONTEND      │
                         └─────────┬─────────┘
                                   │
                              REST / HTTP
                                   │
                                   ▼
                  ┌────────────────────────────────┐
                  │            FASTAPI              │
                  ├────────────────────────────────┤
                  │ Authentication                 │
                  │ Authorization                  │
                  │ Event Management               │
                  │ Team Management                │
                  │ Project Submissions            │
                  │ Judge Assignment               │
                  │ Evaluation                      │
                  │ Score Processing                │
                  │ Results                         │
                  └───────────────┬────────────────┘
                                  │
                                  ▼
                       ┌────────────────────┐
                       │      DATABASE      │
                       │     PostgreSQL     │
                       └────────────────────┘
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

# 06 — WHAT'S INSIDE

<table>
<tr>
<td width="50%">

### 🔑 AUTHENTICATION

JWT-based authentication with controlled access to protected resources.

</td>

<td width="50%">

### 🏟️ EVENT MANAGEMENT

Create and manage complete hackathon lifecycles.

</td>
</tr>

<tr>
<td>

### 👥 TEAM MANAGEMENT

Participants, teams and membership workflows.

</td>

<td>

### 📦 PROJECT SUBMISSIONS

Structured project information and submission lifecycle.

</td>
</tr>

<tr>
<td>

### ⚖️ JUDGING ENGINE

Rubric-based evaluation with controlled access.

</td>

<td>

### 🔒 JUDGE ISOLATION

Backend-enforced separation of evaluations.

</td>
</tr>

<tr>
<td>

### 📊 SCORE ENGINE

Weighted scoring and result processing.

</td>

<td>

### 🏆 RESULT ENGINE

Generate validated final rankings.

</td>
</tr>
</table>

---

# 07 — API SURFACE

<div align="center">

### REST API

`/api/v1`

</div>

```text
AUTHENTICATION
│
├── POST   /auth/register
├── POST   /auth/login
└── GET    /auth/me


EVENTS
│
├── POST   /events
├── GET    /events
└── GET    /events/{event_id}


TEAMS
│
├── POST   /teams
├── GET    /teams/{team_id}
└── POST   /teams/{team_id}/members


PROJECTS
│
├── POST   /projects
├── GET    /projects
├── GET    /projects/{project_id}
└── POST   /projects/{project_id}/submit


JUDGING
│
├── POST   /judges/assignments
├── GET    /judges/assignments
└── POST   /judging/scores


RESULTS
│
├── GET    /results
├── GET    /results/{project_id}
└── GET    /results/export
```

---

# 08 — SECURITY MODEL

<div align="center">

<img src="https://i.imgur.com/82fX4GI.png" width="850" alt="Judging Scorecard">

</div>

```text
                     ┌─────────────┐
                     │   REQUEST   │
                     └──────┬──────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │ JWT VERIFICATION │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │   ROLE CHECK     │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ RESOURCE CHECK   │
                  └────────┬─────────┘
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
             AUTHORIZED          DENIED
                 │                   │
                 ▼                   ▼
              RESPONSE          403 / 401
```

### Security philosophy

```text
Frontend protection       → UX
Backend authorization     → SECURITY
Database constraints      → INTEGRITY
Validation                → SAFETY
```

---

# 09 — TECH STACK

<div align="center">

<img src="https://skillicons.dev/icons?i=python,fastapi,postgres,docker,git,github" width="520">

</div>

<br>

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

VERSIONING      Git / GitHub
```

---

# 10 — PROJECT STRUCTURE

```text
Hackathon-Judging-Platform/
│
├── frontend/
│
├── backend/
│   │
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   │
│   ├── tests/
│   │
│   ├── alembic/
│   │
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
│
├── README.md
│
└── .gitignore
```

---

# 11 — QUALITY GATE

DOGFOOD is designed around testable backend behaviour.

```text
✓ Authentication
✓ Authorization
✓ Event Lifecycle
✓ Team Management
✓ Submission Validation
✓ Judge Assignment
✓ Judge Isolation
✓ Weighted Evaluation
✓ Score Processing
✓ Result Generation
✓ Export
```

### Critical scenario

```text
┌──────────────┐
│   JUDGE A    │
└──────┬───────┘
       │
       │ tries to access
       │ Judge B's score
       ▼
┌──────────────────────┐
│   AUTHORIZATION      │
│       LAYER          │
└──────────┬───────────┘
           │
           ▼
      ┌──────────┐
      │   403    │
      │ FORBIDDEN│
      └──────────┘
```

---

# 12 — LIVE API

Once the backend is running:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

<div align="center">

### API FIRST.  
### DOCUMENTED.  
### TESTABLE.

</div>

---

# 13 — QUICK START

### Clone

```bash
git clone https://github.com/Nethralfh/Hackathon-Judging-Platform.git
cd Hackathon-Judging-Platform
```

### Start Backend

```bash
docker compose up --build
```

### Open API

```text
http://localhost:8000
```

### Swagger

```text
http://localhost:8000/docs
```

---

# 14 — ROADMAP

```text
CORE
[x] Authentication
[x] Event Management
[x] Team Management
[x] Project Submission
[x] Judge Assignment
[x] Judging Workflow
[x] Score Processing


NEXT
[ ] Advanced Analytics
[ ] Real-time Dashboard
[ ] Automated Insights
[ ] Advanced Leaderboards
[ ] Audit Timeline
[ ] Extended Reporting
```

---

# 15 — THE BIGGER PICTURE

```text
                         HACKATHON
                              │
                              ▼
                        PARTICIPANTS
                              │
                              ▼
                           PROJECTS
                              │
                              ▼
                            JUDGES
                              │
                              ▼
                         EVALUATION
                              │
                              ▼
                    ┌──────────────────┐
                    │     DOGFOOD      │
                    │                  │
                    │     SECURE       │
                    │    ISOLATED      │
                    │    STRUCTURED    │
                    │    TRACEABLE     │
                    └────────┬─────────┘
                             │
                             ▼
                       FINAL RESULTS
```

---

<div align="center">

# ⚡ BUILD. JUDGE. TRUST.

### DOGFOOD

**Hackathon Judging Platform**

<br>

`SECURE` · `ISOLATED` · `STRUCTURED` · `SCALABLE`

<br>

---

### Built for hackathons.
### Engineered for trusted evaluation.

<br>

⭐ **Star the repository if you find the project interesting.**

</div>
