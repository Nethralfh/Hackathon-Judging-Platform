import enum
from sqlalchemy import Column, Integer, String, Enum
from app.core.database import Base

class RoleEnum(str, enum.Enum):
    ORGANIZER = "organizer"
    JUDGE = "judge"
    PARTICIPANT = "participant"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.PARTICIPANT)

