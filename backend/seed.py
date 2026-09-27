import json
import os
import sys
from datetime import datetime, timezone
import dateutil.parser

# Add current dir to sys path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.user import User, RoleEnum
from app.models.event import Event, EventStatusEnum
from app.models.team import Team, TeamMember
from app.models.project import Project, ProjectStatusEnum
from app.models.criterion import Criterion
from app.models.judge_assignment import JudgeAssignment
from app.models.score import Score
from app.core.security import get_password_hash, create_access_token

def clear_db(db: Session):
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()

def seed():
    # Setup tables if they dont exist (useful for sqlite)
    Base.metadata.drop_all(bind=engine); Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    with open("fixtures.json", "r") as f:
        data = json.load(f)

    # 1. Organizer
    org = User(username="organizer", email="org@example.com", hashed_password=get_password_hash("test"), role=RoleEnum.ORGANIZER)
    db.add(org)
    db.commit()
    db.refresh(org); print("Org done")

    # 2. Event
    evt = data["event"]
    close_time = dateutil.parser.isoparse(evt["submissions_close"]).replace(tzinfo=None)
    
    event = Event(
        name=evt["name"],
        submission_deadline=close_time,
        status=EventStatusEnum.SUBMISSIONS_CLOSED, # Start closed for the checker
        organizer_id=org.id
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    # 3. Criteria (tracks map to criteria for simplicity)
    criteria_map = {}
    for track in data["tracks"]:
        c = Criterion(event_id=event.id, name=track["name"], weight=1.0, max_score=10.0)
        db.add(c)
        db.commit()
        db.refresh(c)
        criteria_map[track["id"]] = c

    # 4. Judges
    judge_map = {}
    for j in data["judges"]:
        user = User(username=j["id"], email=j["email"], hashed_password=get_password_hash("test"), role=RoleEnum.JUDGE)
        db.add(user)
        db.commit()
        db.refresh(user)
        judge_map[j["id"]] = user

    # 5. Teams & Participants
    team_map = {}
    participant_user = None
    for t in data["teams"]:
        team = Team(name=t["name"], event_id=event.id)
        db.add(team)
        db.commit()
        db.refresh(team)
        team_map[t["id"]] = team
        for member_email in t["members"]:
            member = db.query(User).filter(User.email == member_email).first()
            if not member:
                member = User(username=member_email.split("@")[0] + str(team.id), email=member_email, hashed_password=get_password_hash("test"), role=RoleEnum.PARTICIPANT)
                db.add(member)
                db.commit()
                db.refresh(member)
                if not participant_user:
                    participant_user = member
            tm = TeamMember(team_id=team.id, user_id=member.id)
            db.add(tm)
            db.commit()

    # 6. Projects
    project_map = {}
    for p in data["projects"]:
        sub_time = dateutil.parser.isoparse(p["submitted_at"]).replace(tzinfo=None) if "submitted_at" in p else None
        proj = Project(
            title=p["title"],
            description=p.get("summary", ""),
            repository_url=p.get("repo_url", ""),
            team_id=team_map[p["team"]].id,
            event_id=event.id,
            status=ProjectStatusEnum.SUBMITTED,
            submitted_timestamp=sub_time
        )
        db.add(proj)
        db.commit()
        db.refresh(proj)
        project_map[p["id"]] = proj

    # 7. Assignments & Scores
    for s in data["scores"]:
        j_id = judge_map[s["judge"]].id
        p_id = project_map[s["project"]].id
        
        # Ensure assigned
        assign = db.query(JudgeAssignment).filter(JudgeAssignment.judge_id == j_id, JudgeAssignment.project_id == p_id).first()
        if not assign:
            assign = JudgeAssignment(judge_id=j_id, project_id=p_id, event_id=event.id)
            db.add(assign)
            db.commit()
            
        for crit_name, score_val in s["criteria"].items():
            # In a real app criteria might match by name, but we can just use the first criterion
            crit_id = list(criteria_map.values())[0].id 
            score = Score(judge_id=j_id, project_id=p_id, criterion_id=crit_id, score=score_val)
            db.add(score)
            db.commit()

    # 8. Generate TOML
    org_token = create_access_token(subject=org.username)
    judge_a_token = create_access_token(subject=data["judges"][0]["id"])
    judge_b_token = create_access_token(subject=data["judges"][1]["id"])
    participant_token = create_access_token(subject=participant_user.username)
    
    judge_a_user = db.query(User).filter(User.username == data["judges"][0]["id"]).first()

    toml = f"""[portal]
base_url = "http://localhost:8080"

[tiers]
claimed = ["T1", "T2"]
pitch = "Clean architecture."

[auth]
organizer   = "Authorization: Bearer {org_token}"
judge_a     = "Authorization: Bearer {judge_a_token}"
judge_b     = "Authorization: Bearer {judge_b_token}"
participant = "Authorization: Bearer {participant_token}"

[routes]
gallery      = "/api/v1/public/projects"
submit       = "/api/v1/projects"
judge_scores = "/api/v1/judging/scores"
peer_scores  = "/api/v1/judging/scores?judge_id={judge_a_user.id}"
csv_export   = "/api/v1/results/export"
"""
    with open("../.dogfood.toml", "w") as toml_file:
        toml_file.write(toml)
    print("Seed complete. .dogfood.toml generated.")

if __name__ == "__main__":
    seed()

