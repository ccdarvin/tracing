from redis.commands.search.field import TextField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.json.path import Path
from datetime import datetime, timezone
from redis.asyncio import Redis
from redis import ResponseError
from pydantic import BaseModel
from typing import Optional

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


class Game(RedisModel):
    id: Optional[str]
    websiteId: str
    relatedKey: Optional[str]
    related: Optional[bool]
    urlSource: Optional[str]
    sport: Optional[str]
    fullName: Optional[str]
    firstTeam: Optional[str]
    secoundTeam: Optional[str]
    scraping: Optional[bool] = False
    lastScraping: Optional[datetime]
    
    def key(self):
        id = self.id
        id = id.replace('https://', '')
        id = id.replace(self.websiteId, '')
        return f'games:{self.websiteId}:{id}'
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
        
    
    class Meta:
        index_name = 'idxGames'
        prefix = ['games:']
        schema = (
            TagField('$.id', as_name='id'),
            TagField('$.scraping', as_name='scraping'),
            TagField('$.websiteId', as_name='websiteId'),
            TagField('$.related', as_name='related'),
            TextField('$.firstTeam', as_name='firstTeam', weight=1),
            TextField('$.secoundTeam', as_name='secoundTeam', weight=0.5),
            TextField('$.lastScraping', as_name='lastScraping', sortable=True),
        )

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
    

class RelatedGame(RedisModel):
    id: str
    name: str
    count: int
    related: list
    scraping: bool = False
    
    def key(self):
        return f'related:{self.id}'
    
    class Meta:
        index_name = 'idxRelated'
        prefix = ['related:']
        schema = (
            TagField('$.scraping', as_name='scraping'),
            TextField('$.related', as_name='related'),
        )


async def run_index(r: Redis, model: RedisModel):
    try:
        await r.ft(model.Meta.index_name).dropindex()
    except ResponseError:
        print('Index not found')
    else:
        print('Index dropped')
    
    try:
        await r.ft(model.Meta.index_name).create_index(
            model.Meta.schema,
            definition=IndexDefinition(
                prefix=model.Meta.prefix, index_type=IndexType.JSON
            )
        )
    except ResponseError:
        print('Index not created')
    else:
        print('Index created')


async def save(r: Redis, model: RedisModel, expire: int = 0):
    key = model.key()
    if await r.exists(key):
        for field, value in model.dict(exclude_unset=True).items():
            if isinstance(value, datetime):
                value = value.replace(tzinfo=timezone.utc).isoformat()
            await r.json().set(key, f'.{field}', value)
    else:
        await r.json().set(key, Path.root_path(), model.dict())
        
    if expire > 0:
        await r.expire(key, expire)


async def delete(r: Redis, model: RedisModel):
    key = model.key()
    if await r.exists(key):
        await r.json().delete(key)

     
async def exists(r: Redis, model: RedisModel) -> bool:
    return await r.exists(model.key()) == 1

async def reload(r: Redis, model: RedisModel) -> RedisModel | None:
    key = model.key()
    print(key)
    if await r.exists(key):
        data = await r.json().get(key, Path.root_path())
        return model.copy(update=data)
    else:
        return model
