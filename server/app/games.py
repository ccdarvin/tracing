from .conn import redis_conn
from redis_om import Field, JsonModel
from  typing import Optional
from datetime import datetime, timezone


class Game(JsonModel):
    url: Optional[str] = Field(index=True, primary_key=True)
    site: Optional[str] = Field(index=True)
    sport: Optional[str] = Field(index=True)
    game: Optional[str] = Field(index=True, full_text_search=True, default='')
    firstTeam: Optional[str] = Field(index=True, full_text_search=True, default='')
    secoundTeam: Optional[str] = Field(index=True, full_text_search=True, default='')
    lastUpdate: datetime = Field(default=datetime.now(timezone.utc))
    
    class Meta:
        database = redis_conn
        global_key_prefix = 'tracker'
        model_key_prefix = 'games'