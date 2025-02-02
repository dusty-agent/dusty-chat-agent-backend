from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user import User
from app.utils.token import create_access_token, verify_token
from app.utils.security import hash_password, verify_password
from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid
import secrets

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# ✅ 체험 계정 생성 (고정된 시크릿 키 사용)
@router.post("/guest")
def create_guest_account(db: Session = Depends(get_db)):
    """ 체험 계정 자동 생성 """
    guest_id = str(uuid.uuid4())[:8]
    guest_email = f"guest_{guest_id}@dustyagent.com"

    guest_user = User(email=guest_email, is_guest=True)
    db.add(guest_user)
    db.commit()
    db.refresh(guest_user)

    token = create_access_token({"sub": guest_user.email})
    return {"token": token, "user_email": guest_user.email}

# ✅ 회원가입 (사용자별 개인 시크릿 키 사용)
@router.post("/signup", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """회원가입 API"""
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")

    hashed_password = hash_password(user_data.password)
    new_secret_key = secrets.token_hex(32)  # 사용자별 개인 시크릿 키 생성
    new_user = User(email=user_data.email, password_hash=hashed_password, secret_key=new_secret_key)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# ✅ 로그인 (사용자별 개인 시크릿 키 사용)
@router.post("/login")
def login_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """로그인 API"""
    user = db.query(User).filter(User.email == user_data.email).first()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 잘못되었습니다.")

    access_token = create_access_token(data={"sub": user.email}, user_id=user.id, db=db)
    return {"access_token": access_token, "token_type": "bearer"}

# ✅ 토큰 생성 (회원 가입자와 체험 계정 구분)
@router.post("/token")
def generate_token(user_id: Optional[str] = None, db: Session = Depends(get_db)):
    """토큰 생성 API"""
    access_token = create_access_token(data={"sub": user_id}, user_id=user_id, db=db)
    if not access_token:
        raise HTTPException(status_code=404, detail="User not found")
    return {"access_token": access_token, "token_type": "bearer"}

# ✅ 토큰 검증 (회원 가입자와 체험 계정 구분)
@router.get("/verify")
def verify(user_token: str, user_id: Optional[str] = None, db: Session = Depends(get_db)):
    """토큰 검증 API"""
    payload = verify_token(user_token, user_id, db)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": "Token is valid", "user": payload}
