# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# # MySQL Connection URL (Updated with Password)
# DATABASE_URL = "mysql+pymysql://root:password@localhost/chat_app"


# # Create Engine
# engine = create_engine(DATABASE_URL, echo=True)

# # Session Local to interact with the database
# SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# def save_message(message):
#     # ✅ Ensure this function exists in `database.py`
#     print(f"Saving message: {message}")  # Debugging
#     # Add actual database storage logic here

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from app.models import Message

# ✅ Database Connection
DATABASE_URL = "mysql+pymysql://root:password@localhost/chat_app"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# ✅ Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Retrieve messages from a specific chat room
def get_messages(chat_room_id: int):
    from app.models import Message  # ✅ Import inside function to avoid circular dependency
    db = SessionLocal()
    messages = db.query(Message).filter(Message.chat_room_id == chat_room_id).order_by(Message.sent_at.asc()).all()
    db.close()
    return messages

# ✅ Store chat messages in database
def save_message(chat_room_id: int, user_id: int, content: str):
    from app.models import Message  # ✅ Import inside function to avoid circular dependency
    db = SessionLocal()
    new_message = Message(chat_room_id=chat_room_id, user_id=user_id, content=content)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    db.close()
    print(f"✅ Message saved: {new_message.content}")

