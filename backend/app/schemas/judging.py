from pydantic import BaseModel
from typing import List

class JudgeAssignmentBase(BaseModel):
    judge_id: int
    project_id: int
    event_id: int

class JudgeAssignmentCreate(JudgeAssignmentBase):
    pass

class JudgeAssignmentResponse(JudgeAssignmentBase):
    id: int
    class Config:
        from_attributes = True

class ScoreBase(BaseModel):
    project_id: int
    criterion_id: int
    score: float

class ScoreCreate(ScoreBase):
    pass

class ScoreResponse(ScoreBase):
    id: int
    judge_id: int
    class Config:
        from_attributes = True

class CriterionBase(BaseModel):
    event_id: int
    name: str
    description: str | None = None
    weight: float
    max_score: float

class CriterionCreate(CriterionBase):
    pass

class CriterionResponse(CriterionBase):
    id: int
    class Config:
        from_attributes = True

