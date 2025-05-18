from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, group_id: str, websocket: WebSocket):
        await websocket.accept()
        if group_id not in self.active_connections:
            self.active_connections[group_id] = []
        self.active_connections[group_id].append(websocket)

    def disconnect(self, group_id: str, websocket: WebSocket):
        if group_id in self.active_connections:
            self.active_connections[group_id].remove(websocket)
            if not self.active_connections[group_id]:
                del self.active_connections[group_id]

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_to_group(self, group_id: str, message: str):
        if group_id in self.active_connections:
            for connection in self.active_connections[group_id]:
                await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/chat/{group_id}")
async def websocket_endpoint(websocket: WebSocket, group_id: str):
    await manager.connect(group_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_to_group(group_id, f"Group {group_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(group_id, websocket)
        await manager.send_to_group(group_id, f"User disconnected from group {group_id}")
