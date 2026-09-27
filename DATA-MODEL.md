# Data Model

The database is built on PostgreSQL, utilizing standard relational patterns.

## Core Entities

- **User**: Represents all individuals in the system. Distinguished by a `role` enum (Organizer, Judge, Participant).
- **Event**: The hackathon instance. Contains configurable metadata and submission deadlines.
- **Team & TeamMember**: Participants form teams, which are linked to the Event.
- **Project**: Represents a team's submission. Includes links to the repository, demo, and tracks its submission status (`DRAFT`, `SUBMITTED`, `LOCKED`).
- **Criterion**: The judging rubrics defined by the organizer. Each criterion has a weight and a max score.
- **JudgeAssignment**: Maps a Judge to a Project.
- **Score**: A single evaluation given by a Judge to a Project on a specific Criterion.
- **Result**: The aggregated, normalized, and ranked output for a Project.

## Export Path
The export path (`/api/v1/results/export`) directly joins `Result`, `Project`, and `Team` tables to output a flattened CSV, prioritizing the normalized scores and final ranking.

## Schema Details
The schema relies heavily on Foreign Keys with cascading where appropriate to ensure data integrity.
For example, a `Score` cannot exist without a valid `Judge`, `Project`, and `Criterion`.
