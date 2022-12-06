from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    API: str = "http://localhost:8000"
    
    
    
@lru_cache()
def get_settings():
    return Settings()