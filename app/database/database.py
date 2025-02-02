# database/database.py - DB 연결 설정
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import config  # ✅ 환경 변수 가져오기
from urllib.parse import unquote

# ✅ 엔진 생성 (DEBUG_MODE에 따라 SQL 실행 로그 활성화)
engine = create_engine(config.DATABASE_URL, echo=config.DEBUG_MODE)

# ✅ 세션 생성기
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ 베이스 클래스 정의
Base = declarative_base()

# ✅ 데이터베이스 세션 의존성 (FastAPI에서 사용)
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ 테이블 자동 생성 (운영 환경에서는 실행 X)
if config.ENV == "development":
    Base.metadata.create_all(bind=engine)
