#from redis.commands.search.field import TextField
from redis.commands.json.path import Path
from datetime import datetime, timezone
from pydantic import BaseModel
from  typing import Optional
from redis.asyncio import Redis


class RedisModel(BaseModel):
    
    def key(self):
        return NotImplemented


class Website(RedisModel):
    id: str
    name: Optional[str]
    url: Optional[str]
    scraping: Optional[bool] = False
    lastUpdate: Optional[datetime]
    
    def key(self):
        return f'websites:{self.id}'


class Page(RedisModel):
    id: str
    site: Optional[str]
    sport: Optional[str]
    game: Optional[str]
    firstTeam: Optional[str]
    secoundTeam: Optional[str]
    scraping: bool = False
    
    def key(self):
        return f'pages:{self.site}:{self.id}'
    


async def save(r: Redis, model: RedisModel):
    key = model.key()
    if await r.exists(key):
        for field, value in model.dict(exclude_unset=True).items():
           await r.json().set(key, f'.{field}', value)
    else:
        await r.json().set(key, Path.root_path(), model.dict())


async def delete(r: Redis, model: RedisModel):
    key = model.key()
    if await r.exists(key):
        await r.json().delete(key)
        
async def exists(r: Redis, model: RedisModel):
    return await r.exists(model.key()) == 1