from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import require_organizer, get_current_user
from app.models.event import Event, EventStatusEnum
from app.schemas.event import EventCreate, EventResponse
from app.models.user import User

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event_in: EventCreate, db: Session = Depends(get_db), current_user: User = Depends(require_organizer)):
    new_event = Event(
        name=event_in.name,
        description=event_in.description,
        start_time=event_in.start_time,
        submission_deadline=event_in.submission_deadline,
        judging_start=event_in.judging_start,
        judging_end=event_in.judging_end,
        organizer_id=current_user.id
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.get("", response_model=list[EventResponse])
def get_events(db: Session = Depends(get_db)):
    return db.query(Event).all()

@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

