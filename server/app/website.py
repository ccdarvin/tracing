from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from typing import List

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
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)



manager = ConnectionManager()


@router.websocket("/websites")
async def website_ws(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({"message": "Client left the chat"})

@router.get('/websites')
async def website(request: Request):
    r = request.app.state.redis
    websites = r.json().mget(r.keys('website*'), path='.')
    for website in websites:
        website['icon'] = f'https://www.google.com/s2/favicons?domain={website["id"]}&sz=64'
    return websites