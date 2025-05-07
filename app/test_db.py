from database import SessionLocal

# Create a session and test connection
try:
    session = SessionLocal()
    print("Database connection successful!")
except Exception as e:
    print("Database connection failed:", e)
finally:
    session.close()
