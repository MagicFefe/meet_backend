from typing import Any
from starlette.websockets import WebSocket


class WSConnectivityManager:

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket, code: int = 1000, reason: str | None = None):
        if websocket in self.active_connections:
            await websocket.close(code=code, reason=reason)
            self.active_connections.remove(websocket)

    async def remove_connection(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_json_to_websocket(self, message: Any, websocket: WebSocket):
        if websocket in self.active_connections:
            await websocket.send_json(message)

    async def send_json_broadcast(self, message: Any):
        for websocket in self.active_connections:
            await websocket.send_json(message)
