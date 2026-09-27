from app.models.user import RoleEnum
from app.models.event import EventStatusEnum

def test_auth_register(client):
    response = client.post("/api/v1/auth/register", json={"username": "testorg", "email": "org@test.com", "password": "pass", "role": "organizer"})
    assert response.status_code == 201
    
    response = client.post("/api/v1/auth/login", data={"username": "testorg", "password": "pass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_security_isolation(client, db):
    # Register two judges
    client.post("/api/v1/auth/register", json={"username": "judge1", "email": "j1@test.com", "password": "pass", "role": "judge"})
    client.post("/api/v1/auth/register", json={"username": "judge2", "email": "j2@test.com", "password": "pass", "role": "judge"})
    
    t1 = client.post("/api/v1/auth/login", data={"username": "judge1", "password": "pass"}).json()["access_token"]
    t2 = client.post("/api/v1/auth/login", data={"username": "judge2", "password": "pass"}).json()["access_token"]
    
    # Judge 2 tries to access Judge 1 scores
    me1 = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {t1}"}).json()
    j1_id = me1["id"]
    
    res = client.get(f"/api/v1/judging/scores?judge_id={j1_id}", headers={"Authorization": f"Bearer {t2}"})
    assert res.status_code == 403

def test_events_and_teams(client, db):
    client.post("/api/v1/auth/register", json={"username": "testorg2", "email": "org2@test.com", "password": "pass", "role": "organizer"})
    t_org = client.post("/api/v1/auth/login", data={"username": "testorg2", "password": "pass"}).json()["access_token"]
    
    res = client.post("/api/v1/events", json={"name": "Test Event", "status": "draft"}, headers={"Authorization": f"Bearer {t_org}"})
    assert res.status_code == 201
    evt_id = res.json()["id"]
    
    client.post("/api/v1/auth/register", json={"username": "part1", "email": "p1@test.com", "password": "pass", "role": "participant"})
    t_part = client.post("/api/v1/auth/login", data={"username": "part1", "password": "pass"}).json()["access_token"]
    
    res = client.post("/api/v1/teams", json={"name": "Team A", "event_id": evt_id}, headers={"Authorization": f"Bearer {t_part}"})
    assert res.status_code == 201
    team_id = res.json()["id"]
    
    res = client.post("/api/v1/projects", json={"title": "Proj A", "team_id": team_id, "event_id": evt_id}, headers={"Authorization": f"Bearer {t_part}"})
    assert res.status_code == 201
    proj_id = res.json()["id"]

    client.patch(f"/api/v1/events/{evt_id}", json={"status": "submissions_closed"}, headers={"Authorization": f"Bearer {t_org}"})
    res = client.post(f"/api/v1/projects/{proj_id}/submit", headers={"Authorization": f"Bearer {t_part}"})
    assert res.status_code == 403
