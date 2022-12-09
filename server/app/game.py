from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from pydantic import ValidationError, HttpUrl
from .models import Game, Bet, save, exists
from typing import List
import json


router = APIRouter()


async def game_scraping(websocket: WebSocket, scraping: bool):
    try:
        id=websocket.query_params['game_id']
        website_id=websocket.path_params['website_id']
    except KeyError as e:
        print('No scraping', e)
    else:
        game = Game(id=id, websiteId=website_id, scraping=scraping)
        if not await exists(websocket.app.state.redis, game):
            deleted = True
            await manager.broadcast({
                'id': game.id,
                'deleted': deleted,
            })
        else:    
            await save(websocket.app.state.redis, game)
            await manager.broadcast(game.json(exclude_unset=True))
            print(f'game {game.key()} scraping: {scraping}')


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await game_scraping(websocket, True)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        await game_scraping(websocket, False)

    async def send_personal_message(self, message: str|dict, websocket: WebSocket):
        if isinstance(message, dict):
            await websocket.send_json(message)
        else:
            await websocket.send_text(message)

    async def broadcast(self, message: str|dict):
        for connection in self.active_connections:
            print(connection.query_params)
            if isinstance(message, dict):
                await connection.send_json(message)
            else:
                await connection.send_text(message)


manager = ConnectionManager()


@router.websocket('/games/{website_id}')
async def website_ws(websocket: WebSocket, website_id: str, game_id: HttpUrl):
    await manager.connect(websocket)
    r = websocket.app.state.redis
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                await manager.send_personal_message({'status': 'error', 'message': 'Invalid JSON'}, websocket)
                continue
            
            try:
                type_data = data['type']
                data = data['data']
            except KeyError:
                await manager.send_personal_message({'status': 'error', 'message': 'Missing type or data'}, websocket)
                continue
            
            if type_data == 'bet':
                try:
                    bet = Bet(**data)
                except ValidationError as e:
                    await manager.send_personal_message({'status': 'error', 'message': 'Invalid data', 'errors': e.errors()}, websocket)
                    continue
                else:
                    await save(r, bet, 60*60*24*15)
                    await manager.broadcast(bet.json(exclude_unset=True))
                    continue
            
            await manager.send_personal_message({'status': 'error', 'message': 'Invalid type'}, websocket)
                    
    except WebSocketDisconnect:
        await manager.disconnect(websocket)


#@router.get('/games/{website_id}')
#async def games(request: Request):
#    r = request.app.state.redis
#    websites = await r.json().mget(await r.keys('website*'), path='.')
#    for website in websites:
#        website['icon'] = f'https://www.google.com/s2/favicons?domain={website["id"]}&sz=64'
#    return websites