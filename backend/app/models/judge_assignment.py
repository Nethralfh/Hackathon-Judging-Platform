from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class JudgeAssignment(Base):
    __tablename__ = "judge_assignments"

    id = Column(Integer, primary_key=True, index=True)
    judge_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    
    judge = relationship("User")
    project = relationship("Project")
    event = relationship("Event")

