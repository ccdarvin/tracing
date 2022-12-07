from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from pydantic import ValidationError
from .models import Website, save
from typing import List
import json


router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

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
                await manager.broadcast(model.dict(exclude_unset=True))
                await manager.send_personal_message({'status': 'ok'}, websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({'message': 'Client left the chat'})


@router.get('/websites')
async def website(request: Request):
    r = request.app.state.redis
    websites = await r.json().mget(await r.keys('website*'), path='.')
    for website in websites:
        website['icon'] = f'https://www.google.com/s2/favicons?domain={website["id"]}&sz=64'
    return websites