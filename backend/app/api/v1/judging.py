from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import require_organizer, require_judge, get_current_user
from app.models.user import User, RoleEnum
from app.models.project import Project
from app.models.judge_assignment import JudgeAssignment
from app.models.score import Score
from app.models.criterion import Criterion
from app.schemas.judging import JudgeAssignmentCreate, JudgeAssignmentResponse, ScoreCreate, ScoreResponse, CriterionCreate, CriterionResponse

router = APIRouter(prefix="/judging", tags=["Judging"])

# -- Criteria --
@router.post("/criteria", response_model=CriterionResponse, status_code=status.HTTP_201_CREATED)
def create_criterion(criterion_in: CriterionCreate, db: Session = Depends(get_db), current_user: User = Depends(require_organizer)):
    new_criterion = Criterion(**criterion_in.model_dump())
    db.add(new_criterion)
    db.commit()
    db.refresh(new_criterion)
    return new_criterion

# -- Assignments --
@router.post("/assignments", response_model=JudgeAssignmentResponse, status_code=status.HTTP_201_CREATED)
def assign_judge(assignment_in: JudgeAssignmentCreate, db: Session = Depends(get_db), current_user: User = Depends(require_organizer)):
    new_assignment = JudgeAssignment(**assignment_in.model_dump())
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return new_assignment

@router.get("/assignments", response_model=list[JudgeAssignmentResponse])
def get_assignments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role == RoleEnum.ORGANIZER:
        return db.query(JudgeAssignment).all()
    elif current_user.role == RoleEnum.JUDGE:
        return db.query(JudgeAssignment).filter(JudgeAssignment.judge_id == current_user.id).all()
    else:
        raise HTTPException(status_code=403, detail="Not authorized to view assignments")

@router.get("/projects", response_model=list[int])
def get_judges_projects(db: Session = Depends(get_db), current_user: User = Depends(require_judge)):
    assignments = db.query(JudgeAssignment).filter(JudgeAssignment.judge_id == current_user.id).all()
    return [a.project_id for a in assignments]

# -- Scores --
@router.post("/scores", response_model=ScoreResponse, status_code=status.HTTP_201_CREATED)
def submit_score(score_in: ScoreCreate, db: Session = Depends(get_db), current_user: User = Depends(require_judge)):
    # Verify assignment
    assignment = db.query(JudgeAssignment).filter(
        JudgeAssignment.judge_id == current_user.id,
        JudgeAssignment.project_id == score_in.project_id
    ).first()
    if not assignment:
        raise HTTPException(status_code=403, detail="Not assigned to this project")
    
    # Verify criterion max score
    criterion = db.query(Criterion).filter(Criterion.id == score_in.criterion_id).first()
    if not criterion:
        raise HTTPException(status_code=404, detail="Criterion not found")
    if score_in.score > criterion.max_score or score_in.score < 0:
        raise HTTPException(status_code=400, detail="Score out of bounds")

    new_score = Score(
        judge_id=current_user.id,
        project_id=score_in.project_id,
        criterion_id=score_in.criterion_id,
        score=score_in.score
    )
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    return new_score

@router.get("/scores", response_model=list[ScoreResponse])
def get_scores(judge_id: int | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role == RoleEnum.PARTICIPANT:
        raise HTTPException(status_code=403, detail="Participants cannot view scores")
        
    if current_user.role == RoleEnum.JUDGE:
        if judge_id is not None and judge_id != current_user.id:
            raise HTTPException(status_code=403, detail="A judge must not be able to read another judge's scores.")
        # Judges can only see their own scores
        return db.query(Score).filter(Score.judge_id == current_user.id).all()
    
    # Organizer can view all or filter
    query = db.query(Score)
    if judge_id:
        query = query.filter(Score.judge_id == judge_id)
    return query.all()

