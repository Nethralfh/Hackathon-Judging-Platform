from pydantic import BaseModel
from app.models.user import RoleEnum

class UserBase(BaseModel):
    username: str
    email: str
    role: RoleEnum = RoleEnum.PARTICIPANT

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

