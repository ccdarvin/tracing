from redis.commands.search.field import TextField
from redis.commands.json.path import Path
from datetime import datetime, timezone
from pydantic import BaseModel
from  typing import Optional
import redis


r = redis.Redis(
    host='redis-12622.c277.us-east-1-3.ec2.cloud.redislabs.com',
    port=12622,
    password='TxVYpEfg4DwZSjDxerOiWxNEhgIZouKa'
)


class RedisModel(BaseModel):
    
    def key(self):
        return NotImplemented


class Website(RedisModel):
    id: str
    name: Optional[str]
    url: Optional[str]
    scraping: Optional[bool] = False
    
    def key(self):
        return f'websites:{self.id}'


class Page(RedisModel):
    id: str
    site: Optional[str]
    sport: Optional[str]
    game: Optional[str]
    firstTeam: Optional[str]
    secoundTeam: Optional[str]
    lastUpdate: datetime = datetime.now(timezone.utc)
    scraping: bool = False
    
    def key(self):
        return f'pages:{self.site}:{self.id}'
    


def save(model: RedisModel):
    key = model.key()
    if r.exists(key):
        for field, value in model.dict(exclude_unset=True).items():
            r.json().set(key, f'.{field}', value)
    else:
        r.json().set(key, Path.root_path(), model.dict())


def delete(model: RedisModel):
    key = model.key()
    if r.exists(key):
        r.json().delete(key)
        
def exists(model: RedisModel):
    return r.exists(model.key()) == 1
