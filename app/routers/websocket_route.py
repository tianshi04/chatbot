from typing import Annotated
from fastapi import APIRouter, Depends, Request, Response, WebSocket, WebSocketDisconnect

from app.dependencies import get_current_email, get_curent_email_onetimetoken
from app.utils.token_utils import create_onetimetoken

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        
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

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, email: Annotated[str, Depends(get_curent_email_onetimetoken)]):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"{email} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{email} left the chat")
        
@router.get("/token")
async def get_token_ws(email: Annotated[str, Depends(get_current_email)]):
    onetimetoken = create_onetimetoken(email)
    return {"message": "Successfully created token", "onetimetoken": onetimetoken}