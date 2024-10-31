from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId
from datetime import datetime
from app.schemas.UserSchema import UserSchema


def find_user_by_email(db: Database, email: str):
    users_collection = db.get_collection("users")
    return users_collection.find_one({"email": email})

def create_user(db: Database, user_data: dict) -> UserSchema:
    users_collection = db.get_collection("users")
    if find_user_by_email(db, user_data["email"]):
        raise ValueError("User found")
    
    new_user = {
        "email": user_data["email"],
        "given_name": user_data["given_name"],
        "family_name": user_data["family_name"],
        "picture": user_data["picture"],
        "locale": user_data.get("locale", "default_locale"),
        "googleId": user_data["id"],
        "conversations": [],
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    
    result = users_collection.insert_one(new_user)
    
    if result.inserted_id:
        return UserSchema(**new_user)
    else:
        return None

def update_user(db: Database, user_data: dict) -> UserSchema:
    users_collection = db.get_collection("users")
    
    existing_user  = users_collection.find_one({"email": user_data["email"]})
    if not existing_user:
        raise ValueError("User not found")
    
    updated_data = {k: v for k, v in user_data.items() if v is not None}
    
    if updated_data:
        updated_data['updated_at'] = datetime.now()
        
        user_id = existing_user['_id']
        users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_data})

        updated_user = users_collection.find_one({"_id": ObjectId(user_id)})
        updated_user["_id"] = str(updated_user["_id"])

        return UserSchema(**updated_user)

    return None

def delete_user(db: Database, user_id: str) -> bool:
    users_collection = db.get_collection("users")
    
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    
    return result.deleted_count > 0

def read_all_users(db: Database) -> list[UserSchema]:
    users_collection = db.get_collection("users")
    
    users = list(users_collection.find({}))
    
    return [UserSchema(**user) for user in users]
    
    
    