from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import require_organizer, get_current_user
from app.models.user import User, RoleEnum
from app.models.result import Result
from app.models.project import Project
from app.models.team import Team
from app.schemas.result import ResultResponse
from app.services.scoring_service import compute_results_for_event
import csv
from io import StringIO

router = APIRouter(prefix="/results", tags=["Results"])

@router.post("/compute/{event_id}", status_code=status.HTTP_200_OK)
def compute_results(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_organizer)):
    compute_results_for_event(db, event_id)
    return {"status": "computed"}

@router.get("", response_model=list[ResultResponse])
def get_results(event_id: int | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role == RoleEnum.PARTICIPANT:
        raise HTTPException(status_code=403, detail="Participants cannot view results")
        
    query = db.query(Result)
    if event_id:
        query = query.filter(Result.event_id == event_id)
    return query.order_by(Result.rank.asc()).all()

@router.get("/export")
def export_results_csv(event_id: int | None = None, db: Session = Depends(get_db), current_user: User = Depends(require_organizer)):
    query = db.query(Result).join(Project).join(Team)
    if event_id:
        query = query.filter(Result.event_id == event_id)
        
    results = query.order_by(Result.rank.asc()).all()
    
    csv_file = StringIO()
    writer = csv.writer(csv_file)
    writer.writerow(["project_id", "project_name", "team_name", "weighted_score", "normalized_score", "rank"])
    
    for r in results:
        writer.writerow([
            r.project.id,
            r.project.title,
            r.project.team.name,
            round(r.weighted_score, 2),
            round(r.normalized_score, 2),
            r.rank
        ])
        
    csv_file.seek(0)
    response = StreamingResponse(iter([csv_file.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=results.csv"
    return response

