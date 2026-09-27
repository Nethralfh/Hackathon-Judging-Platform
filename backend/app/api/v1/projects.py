from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.project import Project, ProjectStatusEnum
from app.models.event import Event, EventStatusEnum
from app.models.team import Team, TeamMember
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter(prefix="", tags=["Projects"])

@router.get("/public/projects", response_model=list[ProjectResponse])
def get_public_projects(db: Session = Depends(get_db)):
    return db.query(Project).filter(Project.status != ProjectStatusEnum.DRAFT).all()

@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project_in: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == project_in.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.status == EventStatusEnum.SUBMISSIONS_CLOSED:
        raise HTTPException(status_code=403, detail="Submissions are closed for this event")
    if event.submission_deadline and datetime.now(timezone.utc).replace(tzinfo=None) > event.submission_deadline:
        raise HTTPException(status_code=403, detail="Submission deadline has passed")
        
    team = db.query(Team).filter(Team.id == project_in.team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    new_project = Project(
        title=project_in.title,
        description=project_in.description,
        repository_url=project_in.repository_url,
        demo_url=project_in.demo_url,
        team_id=project_in.team_id,
        event_id=project_in.event_id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.patch("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_in: ProjectUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    event = db.query(Event).filter(Event.id == project.event_id).first()
    if event.status == EventStatusEnum.SUBMISSIONS_CLOSED or (event.submission_deadline and datetime.now(timezone.utc).replace(tzinfo=None) > event.submission_deadline):
        raise HTTPException(status_code=403, detail="Cannot update project after submission deadline")

    for var, value in vars(project_in).items():
        if value is not None:
            setattr(project, var, value)
            
    db.commit()
    db.refresh(project)
    return project

@router.post("/projects/{project_id}/submit", response_model=ProjectResponse)
def submit_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    event = db.query(Event).filter(Event.id == project.event_id).first()
    if event.status == EventStatusEnum.SUBMISSIONS_CLOSED or (event.submission_deadline and datetime.now(timezone.utc).replace(tzinfo=None) > event.submission_deadline):
        raise HTTPException(status_code=403, detail="Cannot submit project after submission deadline")

    project.status = ProjectStatusEnum.SUBMITTED
    project.submitted_timestamp = datetime.now(timezone.utc).replace(tzinfo=None)
    db.commit()
    db.refresh(project)
    return project

@router.get("/projects", response_model=list[ProjectResponse])
def get_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Project).all()

@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

