from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.auth_dependencies import get_db
from app.models.message import MessageHistory, DeletedMessage
from typing import List

router = APIRouter(prefix="/chat", tags=["Chat History"])

# ✅ 채팅기록 조회 (삭제되지 않은 메시지만)
@router.get("/history", response_model=List[dict])
def get_chat_history(db: Session = Depends(get_db)):
    """🚀 삭제되지 않은 메시지(채팅 기록) 조회"""
    chat_history = db.query(MessageHistory).filter(MessageHistory.event_type != "delete").all()
    
    return [
        {
            "id": msg.id,
            "message_id": msg.message_id,
            "role": msg.role,
            "content": msg.content,
            "created_at": msg.created_at
        }
        for msg in chat_history
    ]

# ✅ 삭제된 메시지 조회 API (휴지통)
@router.get("/deleted", response_model=List[dict])
def get_deleted_messages(db: Session = Depends(get_db)):
    deleted_messages = db.query(DeletedMessage).all()
    return [
        {
            "id": msg.id,
            "message_id": msg.message_id,
            "role": msg.role,
            "content": msg.content,
            "deleted_at": msg.deleted_at
        }
        for msg in deleted_messages
    ]
