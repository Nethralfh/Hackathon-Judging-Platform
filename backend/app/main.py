from fastapi import FastAPI
from app.api.v1 import auth, events, teams, projects, judging, results

app = FastAPI(title="DOGFOOD 2026", openapi_url="/api/v1/openapi.json", docs_url="/api/v1/docs")

app.include_router(auth.router, prefix="/api/v1")
app.include_router(events.router, prefix="/api/v1")
app.include_router(teams.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(judging.router, prefix="/api/v1")
app.include_router(results.router, prefix="/api/v1")

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}

