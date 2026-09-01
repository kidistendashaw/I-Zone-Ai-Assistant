from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


# The engine is the actual connection to PostgreSQL.
# It uses the database_url from config.py (which reads from .env)
engine = create_engine(settings.database_url)

# SessionLocal is a factory — it creates database sessions.
# A session is like a conversation with the database:
#   open session → read/write data → close session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    This function is used by every API endpoint that needs the database.
    
    It:
    1. Opens a database session
    2. Gives it to the endpoint (yield)
    3. Closes the session when the endpoint is done (finally)
    
    Usage in an endpoint:
        from app.db.session import get_db
        from fastapi import Depends
        
        @app.get("/users")
        def get_users(db = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
