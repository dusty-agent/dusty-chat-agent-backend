from sqlalchemy.orm import Session
from app.models.message import Message, MessageHistory
import datetime

def create_message(db: Session, role: str, content: str):
    """새로운 메시지를 생성하고, 해당 메시지를 메시지 이력에도 추가"""
    message = Message(role=role, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)

    # 메시지 이력 추가
    message_history = MessageHistory(
        message_id=message.id,
        role=role,
        content=content,
        created_at=datetime.datetime.utcnow()
    )
    db.add(message_history)
    db.commit()

    return message

def get_messages(db: Session, skip: int = 0, limit: int = 10):
    """메시지 목록을 가져오는 함수"""
    return db.query(Message).offset(skip).limit(limit).all()

def get_message_history(db: Session, message_id: int, skip: int = 0, limit: int = 10):
    """특정 메시지의 이력을 조회하는 함수"""
    return db.query(MessageHistory).filter(MessageHistory.message_id == message_id).offset(skip).limit(limit).all()
