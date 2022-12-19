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


class Game(RedisModel):
    id: str
    websiteId: str
    relatedKey: Optional[str]
    hasRelated: bool = False
    urlSource: Optional[str]
    sport: Optional[str]
    fullName: Optional[str]
    firstTeam: Optional[str]
    secondTeam: Optional[str]
    scraping: bool = False
    lastUpdate: Optional[datetime]
    
    def key(self):
        id = self.id
        id = id.replace('https://', '')
        id = id.replace(self.websiteId, '')
        return f'games:{self.websiteId}:{id}'


class RelatedGame(RedisModel):
    id: str
    name: str
    count: int
    related: list
    scraping: bool = False
    
    def key(self):
        return f'related:{self.id}'
    

class Bet(RedisModel):
    id: str
    websiteId: str
    gameId: str
    period: str
    group: Optional[str]
    name: Optional[str]
    bet: Optional[float]
    
    def __init__(self, **data):
        data["id"] = f'{data["period"]}_{data["group"]}_{data["name"]}'
        super().__init__(**data)
    
    def key(self):
        game_id = self.gameId.replace('https://', '').replace(self.websiteId, '')
        return f'bets:{self.websiteId}:{game_id}:{self.id}'


def save(model: RedisModel, expire: int = 0):
    key = model.key()
    if r.exists(key):
        for field, value in model.dict(exclude_unset=True).items():
            r.json().set(key, f'.{field}', value)
    else:
        r.json().set(key, Path.root_path(), model.dict())
    # update lastUpdate 
    r.json().set(key, f'.lastUpdate', datetime.now(timezone.utc).isoformat())
    if expire > 0:
        r.expire(key, expire)


def delete(model: RedisModel):
    key = model.key()
    if r.exists(key):
        r.json().delete(key)
        
def exists(model: RedisModel):
    return r.exists(model.key()) == 1
