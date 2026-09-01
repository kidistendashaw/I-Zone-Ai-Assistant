from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    This is the parent class for ALL database tables.
    Every model (User, Document, Conversation...) inherits from this.
    SQLAlchemy needs this to know which classes represent database tables.
    """
    pass
