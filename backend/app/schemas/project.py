from datetime import datetime
from pydantic import BaseModel
from app.models.project import ProjectStatusEnum

class ProjectBase(BaseModel):
    title: str
    description: str | None = None
    repository_url: str | None = None
    demo_url: str | None = None

class ProjectCreate(ProjectBase):
    team_id: int
    event_id: int

class ProjectUpdate(ProjectBase):
    title: str | None = None

class ProjectResponse(ProjectBase):
    id: int
    team_id: int
    event_id: int
    status: ProjectStatusEnum
    submitted_timestamp: datetime | None = None

    class Config:
        from_attributes = True

