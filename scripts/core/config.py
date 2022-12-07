from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    API: str = "https://plankton-app-5rfza.ondigitalocean.app"
    WS: str = "wss://plankton-app-5rfza.ondigitalocean.app"
    
    
    
@lru_cache()
def get_settings():
    return Settings()