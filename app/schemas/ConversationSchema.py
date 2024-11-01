from pydantic import BaseModel, EmailStr, Field
from app.schemas.MessageSchema import MessageSchema
from datetime import datetime

class ConversationSchema(BaseModel):
    user_email: EmailStr
    label: str
    messages: list[MessageSchema] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)