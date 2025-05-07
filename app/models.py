# from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
# from sqlalchemy.orm import relationship
# from app.database import engine, SessionLocal
# from sqlalchemy.orm import declarative_base
# from sqlalchemy.sql import func  # ✅ Import func

# Base = declarative_base()

# # Users Table
# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(50), unique=True, nullable=False)
#     email = Column(String(100), unique=True, nullable=False)
#     password_hash = Column(String(255), nullable=False)
#     created_at = Column(TIMESTAMP, server_default=func.current_timestamp())  # ✅ Fixed timestamp

#     messages = relationship("Message", back_populates="user")

# # Chat Rooms Table
# class ChatRoom(Base):
#     __tablename__ = "chat_rooms"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), unique=True, nullable=False)
#     created_at = Column(TIMESTAMP, server_default=func.current_timestamp())  # ✅ Fixed timestamp

#     messages = relationship("Message", back_populates="chat_room")

# # Messages Table
# class Message(Base):
#     __tablename__ = "messages"

#     id = Column(Integer, primary_key=True, index=True)
#     chat_room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     content = Column(Text, nullable=False)
#     sent_at = Column(TIMESTAMP, server_default=func.current_timestamp())  # ✅ Fixed timestamp

#     user = relationship("User", back_populates="messages")
#     chat_room = relationship("ChatRoom", back_populates="messages")

# # Create Tables
# Base.metadata.create_all(engine)

from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()  

# ✅ Users Table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    messages = relationship("Message", back_populates="user")

# ✅ Chat Rooms Table
class ChatRoom(Base):
    __tablename__ = "chat_rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    messages = relationship("Message", back_populates="chat_room")

# ✅ Messages Table
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    chat_room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    sent_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    user = relationship("User", back_populates="messages")
    chat_room = relationship("ChatRoom", back_populates="messages")
    
