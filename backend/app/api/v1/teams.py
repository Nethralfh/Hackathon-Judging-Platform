from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.team import Team, TeamMember
from app.models.event import Event
from app.models.user import User
from app.schemas.team import TeamCreate, TeamResponse, TeamMemberCreate

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.post("", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(team_in: TeamCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == team_in.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    new_team = Team(name=team_in.name, event_id=team_in.event_id)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    
    # add creator to team
    member = TeamMember(team_id=new_team.id, user_id=current_user.id)
    db.add(member)
    db.commit()
    
    return new_team

@router.post("/{team_id}/members", status_code=status.HTTP_201_CREATED)
def add_member(team_id: int, member_in: TeamMemberCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
        
    existing_member = db.query(TeamMember).filter(TeamMember.team_id == team_id, TeamMember.user_id == member_in.user_id).first()
    if existing_member:
        raise HTTPException(status_code=409, detail="User is already in team")
        
    new_member = TeamMember(team_id=team_id, user_id=member_in.user_id)
    db.add(new_member)
    db.commit()
    return {"status": "ok"}

@router.get("/{team_id}", response_model=TeamResponse)
def get_team(team_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

