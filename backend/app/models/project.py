import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class ProjectStatusEnum(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    LOCKED = "locked"

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    repository_url = Column(String)
    demo_url = Column(String)
    
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    
    status = Column(Enum(ProjectStatusEnum), nullable=False, default=ProjectStatusEnum.DRAFT)
    submitted_timestamp = Column(DateTime)
    
    team = relationship("Team")
    event = relationship("Event")

