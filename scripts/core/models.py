from redis_om import Field, Migrator, JsonModel
from datetime import datetime, timezone
from  typing import Optional
import redis

redis_conn = redis.Redis(
    host='redis-12622.c277.us-east-1-3.ec2.cloud.redislabs.com',
    port=12622,
    password='TxVYpEfg4DwZSjDxerOiWxNEhgIZouKa'
)


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
