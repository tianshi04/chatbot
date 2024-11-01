import json
from typing import Annotated
from fastapi import APIRouter, Depends, Request, Response, WebSocket, WebSocketDisconnect

from app.dependencies import get_current_email, get_curent_email_onetimetoken
from app.utils.token_utils import create_onetimetoken
from app.utils.aiutils import crate_new_chat_session, get_topic
from app.database import get_db
from pymongo.database import Database
from app.services.conversation_service import create_new_conversation, add_message_to_conversation, read_conversation, read_all_conversationId, get_conversationIds_by_email, get_historychat_by_conversationId, get_label_by_conversationId

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
    
    async def send_message(self, email: str, typeMessage: str, data: str):
        websocket = self.active_connections.get(email)
        if websocket:
            payload = json.dumps({ "type": typeMessage, "message": data})
            await websocket.send_text(payload)
    async def send_message(self, email: str, typeMessage: str, data: dict):
        websocket = self.active_connections.get(email)
        if websocket:
            payload = json.dumps({ "type": typeMessage, "message": data})
            await websocket.send_text(payload)
    
    async def send_message(self, email: str, typeMessage: str, data: list[dict]):
        websocket = self.active_connections.get(email)
        if websocket:
            payload = json.dumps({ "type": typeMessage, "message": data})
            await websocket.send_text(payload)
        
    async def broadcast(self, message: str):
        for email, connection in self.active_connections.items():
            await connection.send_text(message)
            
manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, email: Annotated[str, Depends(get_curent_email_onetimetoken)], db: Annotated[Database, Depends(get_db)]):
    await manager.connect(websocket, email)
    try:
        chat_session = crate_new_chat_session()
        conversationId = None
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data["type"] == "new_chat" and message_data["message"] == 0:    
                if not chat_session.history == []:
                    chat_session.history = []
                    conversationId = None
            elif message_data["type"] == "message":
                response = chat_session.send_message(message_data["message"])
                await manager.send_personal_message(response.text, email)
                if conversationId is None:
                    this_label = get_topic(str(chat_session.history))
                    conversationId = create_new_conversation(db, email, message_data["message"], response.text, this_label)
                    await manager.send_message(email, "label", {"label": this_label, "conversationId": conversationId})
                else:
                    add_message_to_conversation(db, conversationId, message_data["message"], "user")
                    add_message_to_conversation(db, conversationId, response.text, "model")
            elif message_data["type"] == "load_conversationIds":
                quantity = message_data["quantity"]
                conversationIds = get_conversationIds_by_email(db, email, quantity)
                resultList = [{"conversationId": e, "label": get_label_by_conversationId(db, e)} for e in conversationIds]
                await manager.send_message(email, "conversationIds", resultList)
            elif message_data["type"] == "load_messages":
                conversationId = message_data["conversationId"]
                messages = read_conversation(db, conversationId)
                messageDict = [mes.dict() for mes in messages.messages]
                for message in messageDict:
                    message["timestamp"] = str(message["timestamp"])
                await manager.send_message(email, "conversation_messages", messageDict)
                chat_session.history = get_historychat_by_conversationId(db, conversationId)
                
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{email} left the chat")
        
@router.get("/token")
async def get_token_ws(email: Annotated[str, Depends(get_current_email)]):
    onetimetoken = create_onetimetoken(email)
    return {"message": "Successfully created token", "onetimetoken": onetimetoken}