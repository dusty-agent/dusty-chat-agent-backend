from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user import User
from app.utils.token import create_access_token, verify_token
from app.utils.security import hash_password, verify_password
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
import uuid

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# ✅ 회원가입 요청 모델
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# ✅ 회원 응답 모델 (Pydantic v2 대응: `from_attributes = True`)
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True  # ✅ 최신 Pydantic v2 방식

# ✅ 체험 계정 자동 생성 API
@router.post("/guest")
def create_guest_account(db: Session = Depends(get_db)):
    """ 체험 계정 자동 생성 (기존 게스트 계정이 있으면 재사용) """
    guest_id = str(uuid.uuid4())[:8]
    guest_email = f"guest_{guest_id}@dustyagent.com"

    # ✅ 이미 생성된 게스트 계정이 있는지 확인
    existing_guest = db.query(User).filter(User.email == guest_email, User.is_guest == True).first()
    if existing_guest:
        token = create_access_token({"sub": existing_guest.id})  # ✅ `sub`에 `id` 사용
        return {"token": token, "user_id": existing_guest.id}

    # ✅ 새로운 게스트 계정 생성
    guest_user = User(email=guest_email, is_guest=True)
    db.add(guest_user)
    db.commit()
    db.refresh(guest_user)

    token = create_access_token({"sub": guest_user.id})  # ✅ `sub`에 `id` 사용
    return {"token": token, "user_id": guest_user.id}

# ✅ 회원가입 API
@router.post("/signup", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """회원가입 API"""
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")

    hashed_password = hash_password(user_data.password)
    new_user = User(email=user_data.email, password_hash=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# ✅ 로그인 API
@router.post("/login")
def login_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """로그인 API"""
    user = db.query(User).filter(User.email == user_data.email).first()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 잘못되었습니다.")

    access_token = create_access_token(data={"sub": str(user.id)})  # ✅ `sub`에 `id` 사용
    return {"access_token": access_token, "token_type": "bearer"}

# ✅ 토큰 생성 API (이메일이 아닌 user_id 기반)
@router.post("/token")
def generate_token(user_id: int):
    """토큰 생성 API (user_id 기반)"""
    access_token = create_access_token(data={"sub": str(user_id)})  # ✅ `sub`에 `id` 사용
    return {"access_token": access_token, "token_type": "bearer"}

# ✅ 토큰 검증 API (Authorization 헤더 지원)
@router.get("/verify")
def verify(authorization: str = Header(None)):
    """토큰 검증 API"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = authorization.split(" ")[1]
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"message": "Token is valid", "user": payload}
