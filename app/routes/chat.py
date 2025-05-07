from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import ChatRoom, Message, User
from app.schemas import ChatRoomCreate, ChatRoomResponse, MessageCreate, MessageResponse
from jose import jwt
from app.routes.auth import SECRET_KEY, ALGORITHM, oauth2_scheme, get_current_user  # ✅ Correct imports

router = APIRouter()

# ✅ Database Session Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Create Chat Room (Authenticated Users Only)
@router.post("/chatrooms/", response_model=ChatRoomResponse)
def create_chatroom(chatroom: ChatRoomCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = get_current_user(token, db)  # ✅ Fix dependency issue

    # Check if the chat room name already exists
    existing_room = db.query(ChatRoom).filter(ChatRoom.name == chatroom.name).first()
    if existing_room:
        raise HTTPException(status_code=400, detail="Chat room name already taken")

    # Create the chat room if name is unique
    new_chatroom = ChatRoom(name=chatroom.name)
    db.add(new_chatroom)
    db.commit()
    db.refresh(new_chatroom)
    return new_chatroom

# ✅ Send Message (Authenticated Users Only)
@router.post("/messages/", response_model=MessageResponse)
def send_message(message: MessageCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("sub")  # ✅ Extract user ID instead of email

    print(f"Extracted user ID from JWT: {user_id}")  # ✅ Debugging step

    db_user = db.query(User).filter(User.id == user_id).first()
    
    if not db_user:
        print("User lookup failed!")  # ✅ Debugging step
        raise HTTPException(status_code=401, detail="User not found")

    new_message = Message(chat_room_id=message.chat_room_id, user_id=db_user.id, content=message.content)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

# ✅ Retrieve Messages from a Chat Room (Validated)
@router.get("/chatrooms/{chat_room_id}/messages")
def get_messages(chat_room_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = get_current_user(token, db)  # ✅ Fix dependency issue

    chat_room = db.query(ChatRoom).filter(ChatRoom.id == chat_room_id).first()
    if not chat_room:
        raise HTTPException(status_code=404, detail="Chat room not found")

    messages = db.query(Message).filter(Message.chat_room_id == chat_room_id).all()
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found for this chat room")

    return messages
