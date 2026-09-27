# Architecture

The DOGFOOD 2026 judging platform backend is built using a clean, modular architecture emphasizing separation of concerns and robust security.

## Core Technologies
- **FastAPI**: Chosen for its high performance, automatic OpenAPI documentation generation, and robust dependency injection system which is crucial for enforcing role-based access control (RBAC).
- **SQLAlchemy & PostgreSQL**: A robust relational database model handles complex entity relationships seamlessly.
- **Alembic**: For database migrations.

## Modularity
The application is structured into the following layers:
1. **API Routing (`app/api/v1`)**: Exposes RESTful endpoints, handles HTTP requests, and enforces authentication/authorization boundaries.
2. **Business Logic & Services (`app/services`)**: Encapsulates complex logic such as cross-judge normalization and scoring calculations, ensuring endpoints remain lightweight.
3. **Data Access & Models (`app/models`)**: Defines the relational schema.
4. **Schemas (`app/schemas`)**: Pydantic models for request validation and response serialization.

## Security & Authorization
The system strictly enforces the "Judge Isolation" requirement via the dependency injection layer. Role-checking dependencies (`require_organizer`, `require_judge`) validate the decoded JWT token and ensure a user cannot access another role's resources. Specifically, judge score visibility is restricted directly at the API layer by comparing the requester's ID against the target `judge_id`.
