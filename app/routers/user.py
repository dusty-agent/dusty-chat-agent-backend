from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.auth_dependencies import get_current_user, get_db  # ✅ Import 확인
from app.models.user import User

router = APIRouter()

@router.get("/user")
def get_user():
    """사용자 정보 테스트용 엔드포인트"""
    return {"user": "Test User"}

@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    """현재 로그인된 사용자 정보 반환"""
    return {"username": current_user.username, "email": current_user.email}

@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    """현재 로그인된 사용자 정보 반환"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at
    }