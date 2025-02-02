from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.user import User  # User 모델 확인
import os

from app.utils.token import verify_token

# OAuth2 토큰 방식 사용
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    """데이터베이스 세션 생성"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    """현재 로그인된 사용자 가져오기 (토큰 검증)"""
    user = db.query(User).filter(User.token == token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="인증되지 않은 사용자입니다.")
    return payload["sub"]