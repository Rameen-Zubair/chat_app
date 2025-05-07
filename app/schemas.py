from pydantic import BaseModel, EmailStr
from datetime import datetime

# User Registration Schema
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# User Response Schema (Excludes Password)
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

# User Authentication Schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Chat Room Creation Schema
class ChatRoomCreate(BaseModel):
    name: str

# Chat Room Response Schema
class ChatRoomResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True

# Message Creation Schema
class MessageCreate(BaseModel):
    chat_room_id: int
    content: str

# Message Response Schema
class MessageResponse(BaseModel):
    id: int
    chat_room_id: int
    user_id: int
    content: str
    sent_at: datetime

    class Config:
        from_attributes = True
