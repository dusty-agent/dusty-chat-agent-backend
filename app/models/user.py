import os
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# 환경 변수 확인
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

Base = declarative_base()

# ✅ 운영 환경에서는 `users`, 개발 환경에서는 `users_dev` 사용
USER_TABLE_NAME = "users" if ENVIRONMENT == "production" else "users_dev"

class User(Base):
    __tablename__ = USER_TABLE_NAME

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=True)  # 게스트는 비밀번호 없음
    is_guest = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    messages = relationship("Message", back_populates="user")  # ✅ 메시지와 관계 설정

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, created_at={self.created_at})>"
