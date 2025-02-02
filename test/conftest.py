# tests/conftest.py

from sqlalchemy import MetaData
from app.database.database import engine
from app.models.message import Base

def reset_db():
    metadata = MetaData()
    metadata.reflect(bind=engine)
    messages_table = metadata.tables.get("messages")
    if messages_table is not None:
        messages_table.drop(engine)
    Base.metadata.create_all(engine)