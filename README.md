<div align="center">

# HACKJUDGE

### A judging infrastructure built for hackathons.

**SUBMISSIONS · ASSIGNMENTS · EVALUATIONS · NORMALIZATION · RESULTS**

<br>

Built for **DOGFOOD 2026**

</div>

---

## Overview

HackJudge is an end-to-end platform for running the operational and
judging layer of a hackathon.

It connects participants, organizers, and judges through a single
workflow — from project submission to final ranking.

Designed around **judging integrity, controlled access, transparent
scoring, and local-first operation.**

---

## The Workflow

**01 — Submit**  
Teams submit projects within a controlled event window.

**02 — Assign**  
Organizers distribute submissions across judges.

**03 — Evaluate**  
Judges score projects against weighted criteria.

**04 — Normalize**  
Evaluations are processed across judges before ranking.

**05 — Rank**  
Final scores and results are generated from the judging data.

---

## Judging Integrity

### Private by default.

A judge can access their assigned evaluations and own scores.

They cannot access another judge's scores —  
**not through the interface, and not through the API.**

Authorization is enforced at the backend boundary.

---

## Designed for the Real World

| | |
|---|---|
| **Local-first** | Runs without cloud infrastructure |
| **Role-isolated** | Participant, Judge & Organizer boundaries |
| **Weighted scoring** | Criteria-driven evaluation |
| **Normalization** | Cross-judge score processing |
| **Exportable** | Structured judging and result data |
| **Containerized** | Reproducible local deployment |

---

## Architecture

```text
                         HACKJUDGE
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
     PARTICIPANT         ORGANIZER            JUDGE
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                      SUBMISSIONS
                             │
                       ASSIGNMENT
                             │
                       EVALUATION
                             │
                      NORMALIZATION
                             │
                        RANKINGS
                             │
                         RESULTS
