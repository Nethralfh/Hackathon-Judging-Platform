"""
backend/app/web/pages.py

Server-rendered HTML page routes for the DOGFOOD judging platform.
These complement — and never replace — the JSON API routes in app/api/v1/.

Auth is resolved from the Authorization Bearer header (same JWT the API uses).
All data is read via the same SQLAlchemy models the API uses — no logic duplication.
"""

from typing import Optional
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User, RoleEnum
from app.models.project import Project
from app.models.team import Team
from app.models.score import Score
from app.models.judge_assignment import JudgeAssignment

import os

# Templates directory is next to this file's package root (backend/app/templates/)
_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
templates = Jinja2Templates(directory=_TEMPLATES_DIR)

router = APIRouter(tags=["Pages"])


def _get_optional_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    """
    Resolve the current user from the Authorization header — returns None if
    unauthenticated (pages are not hard-blocked at the HTTP layer; the template
    handles role-based UI personalisation, while the API routes enforce access).
    """
    from jose import jwt, JWTError
    from app.core.config import settings

    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        # Also try cookie for browser sessions
        cookie_token = request.cookies.get("access_token")
        if not cookie_token:
            return None
        token = cookie_token
    else:
        token = auth_header.split(" ", 1)[1]

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            return None
        user = db.query(User).filter(User.username == username).first()
        return user
    except JWTError:
        return None


# ---------------------------------------------------------------------------
# GET /  — redirect to gallery
# ---------------------------------------------------------------------------
@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request):
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/projects")


# ---------------------------------------------------------------------------
# GET /projects  — Public gallery (no auth required)
# ---------------------------------------------------------------------------
@router.get("/projects", response_class=HTMLResponse, include_in_schema=False)
async def gallery(request: Request, db: Session = Depends(get_db)):
    current_user = _get_optional_user(request, db)

    projects_orm = db.query(Project).order_by(Project.submitted_timestamp.desc()).all()

    # Build flat dicts for the template (include track name from event criteria lookup)
    projects = []
    tracks_set = set()
    for p in projects_orm:
        team = db.query(Team).filter(Team.id == p.team_id).first()
        # Use event name as track placeholder — adapt as needed
        track_label = f"Event {p.event_id}"
        projects.append({
            "id": p.id,
            "title": p.title,
            "description": p.description or "",
            "track": track_label,
            "repository_url": p.repository_url or "",
        })
        tracks_set.add(track_label)

    tracks = sorted(tracks_set)

    return templates.TemplateResponse(
        request,
        "projects/index.html",
        {
            "title": "Gallery",
            "current_user": _user_ctx(current_user),
            "current_path": "/projects",
            "projects": projects,
            "tracks": tracks,
        },
    )


# ---------------------------------------------------------------------------
# GET /projects/new  — Submission form page
# ---------------------------------------------------------------------------
@router.get("/projects/new", response_class=HTMLResponse, include_in_schema=False)
async def new_project_page(request: Request, db: Session = Depends(get_db)):
    current_user = _get_optional_user(request, db)

    return templates.TemplateResponse(
        request,
        "projects/new.html",
        {
            "title": "Submit Project",
            "current_user": _user_ctx(current_user),
            "current_path": "/projects/new",
        },
    )


# ---------------------------------------------------------------------------
# GET /projects/{project_id}  — Project detail page
# ---------------------------------------------------------------------------
@router.get("/projects/{project_id}", response_class=HTMLResponse, include_in_schema=False)
async def show_project(request: Request, project_id: int, db: Session = Depends(get_db)):
    current_user = _get_optional_user(request, db)

    project_orm = db.query(Project).filter(Project.id == project_id).first()
    if not project_orm:
        raise HTTPException(status_code=404, detail="Project not found")

    team = db.query(Team).filter(Team.id == project_orm.team_id).first()
    track_label = f"Event {project_orm.event_id}"

    project = {
        "id": project_orm.id,
        "title": project_orm.title,
        "description": project_orm.description or "",
        "track": track_label,
        "repository_url": project_orm.repository_url or "",
        "team_name": team.name if team else "Unknown",
        "submitted_at": (
            project_orm.submitted_timestamp.strftime("%a, %d %b %Y %H:%M:%S UTC")
            if project_orm.submitted_timestamp else "—"
        ),
    }

    return templates.TemplateResponse(
        request,
        "projects/show.html",
        {
            "title": project_orm.title,
            "current_user": _user_ctx(current_user),
            "current_path": f"/projects/{project_id}",
            "project": project,
        },
    )


# ---------------------------------------------------------------------------
# GET /judge/dashboard  — Judge scoring queue
# ---------------------------------------------------------------------------
@router.get("/judge/dashboard", response_class=HTMLResponse, include_in_schema=False)
async def judge_dashboard(request: Request, db: Session = Depends(get_db)):
    current_user = _get_optional_user(request, db)

    # If not a judge, render empty queue (auth enforcement lives in the API)
    if not current_user or current_user.role != RoleEnum.JUDGE:
        return templates.TemplateResponse(
            request,
            "judge/dashboard.html",
            {
                "title": "Scoring Queue",
                "current_user": _user_ctx(current_user),
                "current_path": "/judge/dashboard",
                "assignments": [],
            },
        )

    # Fetch this judge's assigned projects
    judge_assignments = (
        db.query(JudgeAssignment)
        .filter(JudgeAssignment.judge_id == current_user.id)
        .all()
    )

    # Fetch existing scores this judge has submitted, keyed by project_id
    existing_scores_by_project: dict = {}
    score_rows = (
        db.query(Score)
        .filter(Score.judge_id == current_user.id)
        .all()
    )
    for s in score_rows:
        existing_scores_by_project[s.project_id] = s

    assignments = []
    for ja in judge_assignments:
        project_orm = db.query(Project).filter(Project.id == ja.project_id).first()
        if not project_orm:
            continue

        track_label = f"Event {project_orm.event_id}"
        project_dict = {
            "id": project_orm.id,
            "title": project_orm.title,
            "description": project_orm.description or "",
            "track": track_label,
            "repository_url": project_orm.repository_url or "",
        }

        raw_score = existing_scores_by_project.get(project_orm.id)
        existing_score = None
        if raw_score:
            # The score table stores a single float; map it to the criteria dict
            # the frontend expects (functionality/creativity/impact are EJS-era keys)
            existing_score = {
                "criteria": {
                    "functionality": raw_score.score,
                    "creativity": None,
                    "impact": None,
                },
                "comment": "",
            }

        assignments.append({
            "project": project_dict,
            "existing_score": existing_score,
        })

    return templates.TemplateResponse(
        request,
        "judge/dashboard.html",
        {
            "title": "Scoring Queue",
            "current_user": _user_ctx(current_user),
            "current_path": "/judge/dashboard",
            "assignments": assignments,
        },
    )


# ---------------------------------------------------------------------------
# GET /organizer/dashboard  — Organizer progress view
# ---------------------------------------------------------------------------
@router.get("/organizer/dashboard", response_class=HTMLResponse, include_in_schema=False)
async def organizer_dashboard(request: Request, db: Session = Depends(get_db)):
    current_user = _get_optional_user(request, db)

    # Gather stats from real DB data
    all_projects = db.query(Project).order_by(Project.title).all()
    all_scores = db.query(Score).all()

    # Per-project score grouping
    scores_by_project: dict = {}
    for s in all_scores:
        scores_by_project.setdefault(s.project_id, []).append(s)

    project_rows = []
    for p in all_projects:
        team = db.query(Team).filter(Team.id == p.team_id).first()
        scores = scores_by_project.get(p.id, [])
        score_values = [s.score for s in scores]
        avg = sum(score_values) / len(score_values) if score_values else None
        project_rows.append({
            "id": p.id,
            "title": p.title,
            "track": f"Event {p.event_id}",
            "score_count": len(scores),
            "avg_score": avg,
        })

    total_projects = len(all_projects)
    scored_projects = sum(1 for r in project_rows if r["score_count"] > 0)
    total_scores = len(all_scores)

    # Per-judge completion
    judges = db.query(User).filter(User.role == RoleEnum.JUDGE).all()
    scores_by_judge: dict = {}
    for s in all_scores:
        scores_by_judge[s.judge_id] = scores_by_judge.get(s.judge_id, 0) + 1

    judge_rows = []
    for j in judges:
        assignments = (
            db.query(JudgeAssignment)
            .filter(JudgeAssignment.judge_id == j.id)
            .all()
        )
        tracks = list({f"Event {a.event_id}" for a in assignments})
        judge_rows.append({
            "id": j.id,
            "name": j.username,
            "tracks": tracks,
            "review_count": scores_by_judge.get(j.id, 0),
        })

    judge_rows.sort(key=lambda j: j["review_count"], reverse=True)

    return templates.TemplateResponse(
        request,
        "organizer/dashboard.html",
        {
            "title": "Organizer Dashboard",
            "current_user": _user_ctx(current_user),
            "current_path": "/organizer/dashboard",
            "stats": {
                "total_projects": total_projects,
                "scored_projects": scored_projects,
                "total_scores": total_scores,
            },
            "project_rows": project_rows,
            "judge_rows": judge_rows,
        },
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _user_ctx(user: Optional[User]) -> Optional[dict]:
    """Convert ORM user to a plain dict safe for template rendering."""
    if user is None:
        return None
    return {"role": user.role.value, "username": user.username, "id": user.id}
