import json
from typing import Annotated
from fastapi import APIRouter, Depends, Request, Response, WebSocket, WebSocketDisconnect

from app.dependencies import get_current_email, get_curent_email_onetimetoken
from app.utils.token_utils import create_onetimetoken
from app.utils.aiutils import crate_new_chat_session

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        
    async def connect(self, websocket: WebSocket, email: str):
        await websocket.accept()
        self.active_connections[email] = websocket
        print(f"{email} connected.")
        
    def disconnect(self, email: str):
        if email in self.active_connections:
            del self.active_connections[email]
            print(f"{email} disconnected.")

    async def send_personal_message(self, message: str, email: str):
        websocket = self.active_connections.get(email)
        if websocket:
            payload = json.dumps({ "type": "message", "message": message})
            await websocket.send_text(payload)
        
    async def broadcast(self, message: str):
        for email, connection in self.active_connections.items():
            await connection.send_text(message)
            
manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, email: Annotated[str, Depends(get_curent_email_onetimetoken)]):
    await manager.connect(websocket, email)
    try:
        chat_session = crate_new_chat_session()
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data["type"] == "new_chat" and message_data["message"] == 0:    
                if not chat_session.history == []:
                    chat_session = crate_new_chat_session()
            elif message_data["type"] == "message":
                response = chat_session.send_message(message_data["message"])
                await manager.send_personal_message(response.text, email)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{email} left the chat")
        
@router.get("/token")
async def get_token_ws(email: Annotated[str, Depends(get_current_email)]):
    onetimetoken = create_onetimetoken(email)
    return {"message": "Successfully created token", "onetimetoken": onetimetoken}