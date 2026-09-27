from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.core.database import Base

class Criterion(Base):
    __tablename__ = "criteria"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    weight = Column(Float, nullable=False)
    max_score = Column(Float, nullable=False)

