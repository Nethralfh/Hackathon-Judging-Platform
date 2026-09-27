from datetime import datetime
from pydantic import BaseModel
from app.models.event import EventStatusEnum

class EventBase(BaseModel):
    name: str
    description: str | None = None
    start_time: datetime | None = None
    submission_deadline: datetime | None = None
    judging_start: datetime | None = None
    judging_end: datetime | None = None

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    status: EventStatusEnum
    organizer_id: int

    class Config:
        from_attributes = True

