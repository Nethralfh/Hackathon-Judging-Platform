import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class EventStatusEnum(str, enum.Enum):
    DRAFT = "draft"
    OPEN = "open"
    SUBMISSIONS_CLOSED = "submissions_closed"
    JUDGING = "judging"
    COMPLETED = "completed"

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    start_time = Column(DateTime)
    submission_deadline = Column(DateTime)
    judging_start = Column(DateTime)
    judging_end = Column(DateTime)
    status = Column(Enum(EventStatusEnum), nullable=False, default=EventStatusEnum.DRAFT)
    
    organizer_id = Column(Integer, ForeignKey("users.id"))
    
    organizer = relationship("User")

