from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.message import Message, DeletedMessage, MessageHistory
from app.dependencies.auth_dependencies import get_db, get_current_user  # ✅ 사용자 인증 함수 추가
from pydantic import BaseModel
from datetime import datetime
from app.services.openai_service import chat_with_gpt

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

class MessageCreate(BaseModel):
    content: str  # ✅ `role` 필드 제거 (자동 처리)

class MessageResponse(BaseModel):
    id: int
    user_id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True  # ✅ Pydantic v2 변경 사항 적용

# ✅ 로그인한 사용자 기반으로 채팅 내역 가져오기
@router.get("/", response_model=List[MessageResponse])
def get_messages(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)  # ✅ 로그인한 사용자 정보 가져오기
):
    return (
        db.query(Message)
        .filter(Message.user_id == current_user["id"])  # ✅ 사용자 ID 필터링
        .offset(skip)
        .limit(limit)
        .all()
    )

# ✅ 로그인한 사용자와 GPT 간 대화 저장
@router.post("/", response_model=MessageResponse)
async def chat_gpt(
    request: MessageCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    if not request.content:
        raise HTTPException(status_code=400, detail="메시지를 입력하세요.")

    gpt_response = chat_with_gpt(request.content)

    # ✅ 사용자의 메시지 저장
    user_message = Message(user_id=current_user["id"], role="user", content=request.content)
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    # ✅ GPT 응답 저장
    gpt_message = Message(user_id=current_user["id"], role="assistant", content=gpt_response)
    db.add(gpt_message)
    db.commit()
    db.refresh(gpt_message)

    return gpt_message

@router.get("/deleted", response_model=List[dict])
def get_deleted_messages(db: Session = Depends(get_db)):
    """🗑 삭제된 메시지 조회 API"""
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