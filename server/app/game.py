from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from .models import Game, Bet, RelatedGame, save, exists, reload
from pydantic import ValidationError, HttpUrl
from redis.commands.search.query import Query
from datetime import datetime, timezone
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
        game = Game(id=id, websiteId=website_id)
        lastScraping = lastScraping=datetime.now(timezone.utc)
        if game := await reload(websocket.app.state.redis, game):
            print(game.relatedKey, scraping, lastScraping)
            await websocket.app.state.redis.json().set(game.relatedKey, '.scraping', scraping)
            await websocket.app.state.redis.json().set(game.relatedKey, '.lastScraping', game.lastScraping)
        if not await exists(websocket.app.state.redis, game):
            deleted = True
            await manager.broadcast({
                'id': game.id,
                'deleted': deleted,
            })
        else:
            game.scraping = scraping
            game.lastScraping = lastScraping
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
            if isinstance(message, dict):
                await connection.send_json(message)
            else:
                await connection.send_text(message)


manager = ConnectionManager()


@router.websocket('/games/{website_id}')
async def game_ws(websocket: WebSocket, website_id: str|None, game_id: HttpUrl|None):
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
                    await save(r, bet, 60*60)
                    await manager.broadcast(bet.json(exclude_unset=True))
                    continue
            
            await manager.send_personal_message({'status': 'error', 'message': 'Invalid type'}, websocket)
                    
    except (WebSocketDisconnect,):
        await manager.disconnect(websocket)


@router.get('/games')
async def game_list(request: Request, q: str=None):
    r = request.app.state.redis
    q_any = q.replace('*', '').replace('vs', '')
    q_any = '*'.join(q_any.split())
    print(f'{q}|{q_any}*')
    query = Query(f'{q}|{q_any}*').with_scores().paging(0, 30).language('spanish')
    result = await r.ft('idxGames').search(query)
    games = []
    for doc in result.docs:
        games.append({
            **json.loads(doc.json),
            'key': doc.id,
            'searchScore': doc.score
        })
    return games


@router.post('/games/related')
async def game_related(
    request: Request, related: RelatedGame
):
    r = request.app.state.redis
    await save(r, related)
    for key in related.related:
        await r.json().set(key, '.related', True)
        await r.json().set(key, '.scraping', False)
    return related


@router.get('/games/related')
async def game_related_list(
    request: Request
):
    r = request.app.state.redis
    docs = await r.json().mget(await r.keys('related:*'), '.')
    return docs


@router.get('/games/bets')
async def game_bets(
    request: Request
):
    r = request.app.state.redis
    try:
        bets = await r.json().mget(await r.keys(f'bets:*'), '.')
    except Exception as e:
        return []
    return bets

    