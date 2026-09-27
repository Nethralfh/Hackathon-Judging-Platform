from sqlalchemy.orm import Session
from app.models.event import Event
from app.models.project import Project
from app.models.score import Score
from app.models.criterion import Criterion
from app.models.result import Result
from app.services.normalization_service import normalize_scores

def compute_results_for_event(db: Session, event_id: int):
    # Get all projects for event
    projects = db.query(Project).filter(Project.event_id == event_id).all()
    project_ids = [p.id for p in projects]
    
    if not project_ids:
        return
        
    # Get all scores for these projects
    scores = db.query(Score).filter(Score.project_id.in_(project_ids)).all()
    criteria = db.query(Criterion).filter(Criterion.event_id == event_id).all()
    criteria_weights = {c.id: c.weight for c in criteria}
    
    # Normalize
    norm_mapping = normalize_scores(scores)
    
    # Compute per-project scores
    project_weighted = {pid: 0.0 for pid in project_ids}
    project_normalized = {pid: 0.0 for pid in project_ids}
    
    for score in scores:
        w = criteria_weights.get(score.criterion_id, 1.0)
        project_weighted[score.project_id] += score.score * w
        project_normalized[score.project_id] += norm_mapping.get(score.id, score.score) * w
        
    # Create or update results
    for pid in project_ids:
        res = db.query(Result).filter(Result.project_id == pid).first()
        if not res:
            res = Result(project_id=pid, event_id=event_id)
            db.add(res)
        res.weighted_score = project_weighted[pid]
        res.normalized_score = project_normalized[pid]
        
    db.commit()
    
    # Rank them
    results = db.query(Result).filter(Result.event_id == event_id).order_by(Result.normalized_score.desc()).all()
    for i, r in enumerate(results):
        r.rank = i + 1
    db.commit()

