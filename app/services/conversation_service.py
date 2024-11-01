from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId
from datetime import datetime
from app.schemas.ConversationSchema import ConversationSchema
from app.schemas.MessageSchema import MessageSchema

def add_conversation_to_user(db: Database, email: str, conversationId: ObjectId):
    users_collection = db.get_collection("users")
    
    users_collection.update_one({"email": email}, {"$push": {"conversations": str(conversationId)}})
    
def create_new_conversation(db: Database, email: str, first_message: str, first_response: str, label: str):
    conversations_collection = db.get_collection("conversations")
    
    message_instance = MessageSchema(sender="user", text=first_message)
    response_instance = MessageSchema(sender="model", text=first_response)
    conversatation_instance = ConversationSchema(user_email=email, label=label, messages=[message_instance, response_instance])
    
    result = conversations_collection.insert_one(conversatation_instance.dict())
    add_conversation_to_user(db, email, result.inserted_id)
    
    return str(result.inserted_id)

def add_message_to_conversation(db: Database, conversationId: str, message: str, sender: str):
    conversations_collection = db.get_collection("conversations")
    
    message_instance = MessageSchema(sender=sender, text=message)
    conversations_collection.update_one({"_id": ObjectId(conversationId)}, {"$push": {"messages": message_instance.dict()}})
    
def read_conversation(db: Database, conversationId: str) -> ConversationSchema:
    conversations_collection = db.get_collection("conversations")
    
    conversation = conversations_collection.find_one({"_id": ObjectId(conversationId)})
    
    return ConversationSchema(**conversation)

def read_all_conversationId(db: Database, email: str) -> list[str]:
    users_collection = db.get_collection("users")
    user = users_collection.find_one({"email": email})
    
    return user["conversations"]
    
    
    
