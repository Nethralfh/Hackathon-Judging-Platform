from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./dogfood.db"
    SECRET_KEY: str = "changethisinproduction"
    
    class Config:
        env_file = ".env"

settings = Settings()

