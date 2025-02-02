import os
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# ✅ 운영 환경에서는 `messages_history`, 개발 환경에서는 `messages_history_dev`
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
MESSAGE_TABLE_NAME = "messages_history" if ENVIRONMENT == "production" else "messages_history_dev"

class Message(Base):
    __tablename__ = MESSAGE_TABLE_NAME

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # ✅ User 테이블과 연결
    message = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="messages")  # ✅ User와 관계 설정

    def __repr__(self):
        return f"<Message(id={self.id}, user_id={self.user_id}, message={self.message}, created_at={self.created_at})>"
    
class DeletedMessage(Base):
    __tablename__ = "deleted_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String, nullable=False)
    deleted_at = Column(DateTime, default=datetime.utcnow)

class MessageHistory(Base):
    __tablename__ = "messages_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)