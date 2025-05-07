# from fastapi import FastAPI, WebSocket
# from app.routes import auth, chat  # ✅ Ensure both imports exist
# from fastapi.middleware.cors import CORSMiddleware
# from typing import List
# from app.database import save_message


# app = FastAPI()

# # ✅ Enable CORS for frontend access
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ✅ Include authentication & chat routes
# app.include_router(auth.router)
# app.include_router(chat.router)  

# @app.get("/")
# def home():
#     return {"message": "Welcome to the Chat Application!"}

# # ------------------------------------
# # 🔥 WebSocket Implementation
# # ------------------------------------
           

# @app.websocket("/ws/{room_id}")
# async def websocket_endpoint(websocket: WebSocket, room_id: int):
#     await websocket.accept()
    
#     if room_id not in active_connections:
#         active_connections[room_id] = []
#     active_connections[room_id].append(websocket)

#     try:
#         while True:
#             message = await websocket.receive_text()

#             save_message(room_id, user_id=2, content=message)  # ✅ Store in DB

#             for connection in active_connections[room_id]:  # ✅ Only broadcast in this room
#                 await connection.send_text(message)
#     except:
#         active_connections[room_id].remove(websocket)

####################################NEW CODEEEEEEEEEEEEEEEEEEEEEEEEEEE##########################################

###### TESTINGGG ###########3

# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def home():
#     return {"message": "FastAPI is working!"}

################################

from fastapi import FastAPI, WebSocket
from app.database import save_message, get_messages
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import User
from app.routes.auth import verify_password, create_access_token  # ✅ Correct folder path
from pydantic import BaseModel
from app.routes.auth import router as auth_router  # ✅ Import router properly
from app.routes.chat import router as chat_router 
from fastapi.staticfiles import StaticFiles




app = FastAPI()
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
app.include_router(auth_router)
app.include_router(chat_router)

active_connections = {}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ Allow frontend requests
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Define Login Request Model
class LoginRequest(BaseModel):
    email: str
    password: str

# ✅ Fix the Login Route
@app.post("/api/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.id)
    return {"access_token": token}


# ✅ WebSocket for specific rooms
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int):
    await websocket.accept()
    
    if room_id not in active_connections:
        active_connections[room_id] = []
    active_connections[room_id].append(websocket)

    try:
        while True:
            message = await websocket.receive_text()

            save_message(chat_room_id=room_id, user_id=2, content=message)  # ✅ Store in DB

            for connection in active_connections[room_id]:  # ✅ Broadcast only within this room
                await connection.send_text(message)
    except:
        active_connections[room_id].remove(websocket)

# ✅ API Route to Get Messages for a Specific Room
@app.get("/chatrooms/{room_id}/messages")
def get_chatroom_messages(room_id: int):
    messages = get_messages(room_id)
    return [{"user_id": msg.user_id, "content": msg.content, "sent_at": msg.sent_at} for msg in messages]
