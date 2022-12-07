from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    API: str
    WS: str
    
    class Config:
        env_file = '.env.local'
    
    
    
@lru_cache()
def get_settings():
    return Settings()