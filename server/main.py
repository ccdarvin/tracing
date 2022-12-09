from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.website import router as website_router
from app.game import router as game_router
from fastapi.responses import HTMLResponse
from typing import List
from app.models import Game
import redis.asyncio as redis
from redis import ResponseError
from time import sleep


app = FastAPI()
app.include_router(website_router, tags=['website'])
app.include_router(game_router, tags=['game'])


app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
async def startup():
    app.state.redis = await redis.Redis(
        host='redis-12622.c277.us-east-1-3.ec2.cloud.redislabs.com',
        port=12622,
        password='TxVYpEfg4DwZSjDxerOiWxNEhgIZouKa' 
    )
    try:
        await app.state.redis.ft(Game.Meta.index_name).dropindex()
    except ResponseError:
        print('Index does not exist')
    else:
        print('Index dropped')
    sleep(5)
    try:
        await app.state.redis.ft(Game.Meta.index_name).create_index(
            Game.Meta.schema, 
            definition=IndexDefinition(prefix=Game.Meta.prefix, index_type=IndexType.JSON)
        )
    except ResponseError:
        print('Error creating index')
    else:
        print('Index created')

    
@app.on_event('shutdown')
async def shutdown():
    await app.state.redis.close()  


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://127.0.0.1:8000/websites`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
