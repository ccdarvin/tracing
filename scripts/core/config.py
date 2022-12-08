from pydantic import BaseSettings

class Settings(BaseSettings):
    API: str
    WS: str
    
    class Config:
        env_file = '.env.local'
    
    

def get_settings():
    return Settings()