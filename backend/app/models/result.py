from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    weighted_score = Column(Float, nullable=False, default=0.0)
    normalized_score = Column(Float, nullable=False, default=0.0)
    rank = Column(Integer, nullable=True)

    project = relationship("Project")
    event = relationship("Event")

