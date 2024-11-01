from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class MessageSchema(BaseModel):
    sender: Literal["model", "user"]
    text: str
    timestamp: datetime = Field(default_factory=datetime.now)