from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from redis.commands.search import aggregation
from redis.commands.search import reducers
from pydantic import ValidationError
from .models import Website, save
from typing import List
import json


router = APIRouter()


async def website_scraping(websocket: WebSocket, scraping: bool):
    try:
        id=websocket.query_params['scraping']
    except KeyError:
        print('No scraping')
    else:
        website = Website(id=id, scraping=scraping)
        await save(websocket.app.state.redis, website)
        await manager.broadcast({'id': id, 'scraping': scraping})
        print(f'Website {id} scraping: {scraping}')

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await website_scraping(websocket, True)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        await website_scraping(websocket, False)

    async def send_personal_message(self, message: str|dict, websocket: WebSocket):
        if isinstance(message, dict):
            await websocket.send_json(message)
        else:
            await websocket.send_text(message)

    async def broadcast(self, message: str|dict):
        for connection in self.active_connections:
            print(connection.client_state)
            if isinstance(message, dict):
                await connection.send_json(message)
            else:
                await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/websites")
async def website_ws(websocket: WebSocket):
    await manager.connect(websocket)
    r = websocket.app.state.redis
    try:
        while True:
            data = await websocket.receive_text()
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                await manager.send_personal_message({'status': 'error', 'message': 'Invalid JSON'}, websocket)
                continue
            
            try:
               model = Website(**data)
            except ValidationError as e:
                await manager.send_personal_message({
                    'status': 'error', 
                    'message': 'Invalid data',
                    'errors': e.errors()
                    }, websocket)
                continue
            else:
                await save(r, model)
                websocket.state.model = model
                await manager.broadcast(model.dict(exclude_unset=True))
            
    except WebSocketDisconnect:
        await manager.disconnect(websocket)


@router.get('/websites')
async def website(request: Request):
    r = request.app.state.redis
    game_count = {}
    for row in (await r.ft('idxGames').aggregate(
        aggregation.AggregateRequest('*').group_by(
            '@websiteId', reducers.count().alias('count')
        )
    )).rows:
        game_count[row[1].decode()] = int(row[3])
    websites = await r.json().mget(await r.keys('website*'), path='.')
    for website in websites:
        website['icon'] = f'https://www.google.com/s2/favicons?domain={website["id"]}&sz=64'
        website['gameCount'] = game_count.get(website['id'], 0)
    return websites