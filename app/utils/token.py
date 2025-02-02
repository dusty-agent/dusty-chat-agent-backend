from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.models.user import User
import os
from dotenv import load_dotenv
import secrets

# 환경 변수 로드
load_dotenv()
DEFAULT_SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")  # 체험 계정용 고정 키
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1시간

# 사용자별 시크릿 키 가져오기 (회원가입한 사용자)
def get_user_secret_key(user_id: str, db: Session) -> Optional[str]:
    user = db.query(User).filter(User.id == user_id).first()
    return user.secret_key if user else None

# JWT 토큰 생성 (체험 계정 또는 회원 계정 구분)
def create_access_token(data: dict, user_id: Optional[str] = None, db: Optional[Session] = None, expires_delta: Optional[timedelta] = None):
    if user_id and db:
        # 회원가입한 사용자는 DB에서 개인 시크릿 키를 가져옴
        secret_key = get_user_secret_key(user_id, db)
        if not secret_key:
            return None
    else:
        # 체험 계정(Guest User)은 고정된 시크릿 키 사용
        secret_key = DEFAULT_SECRET_KEY

    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)

# JWT 토큰 검증 (체험 계정 또는 회원 계정 구분)
def verify_token(token: str, user_id: Optional[str] = None, db: Optional[Session] = None):
    if user_id and db:
        secret_key = get_user_secret_key(user_id, db)
    else:
        secret_key = DEFAULT_SECRET_KEY  # 체험 계정

    if not secret_key:
        return None

    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
