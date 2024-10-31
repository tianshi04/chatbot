from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List
from datetime import datetime

class UserSchema(BaseModel):
    email: EmailStr                         # Địa chỉ email của người dùng
    given_name: str                         # Tên người dùng
    family_name: str                        # Họ người dùng
    picture: HttpUrl                        # URL đến ảnh đại diện
    locale: str                             # Ngôn ngữ của người dùng
    googleId: str                           # ID duy nhất từ Google
    conversations: List[str] = []           # Danh sách ID cuộc trò chuyện
    created_at: datetime                    # Thời gian tạo người dùng
    updated_at: datetime                    # Thời gian cập nhật người dùng
