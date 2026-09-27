from pydantic import BaseModel

class ResultResponse(BaseModel):
    id: int
    project_id: int
    event_id: int
    weighted_score: float
    normalized_score: float
    rank: int | None = None
    
    class Config:
        from_attributes = True

