from pydantic import BaseModel

class TeamBase(BaseModel):
    name: str
    event_id: int

class TeamCreate(TeamBase):
    pass

class TeamResponse(TeamBase):
    id: int

    class Config:
        from_attributes = True

class TeamMemberCreate(BaseModel):
    user_id: int

