import logging
from sqlalchemy import MetaData, text
from app.database.database import engine, Base, SessionLocal
from sqlalchemy.orm import Session
from app.models.message import Message, MessageHistory
import datetime

logger = logging.getLogger(__name__)

def init_db():
    """데이터베이스 초기화 및 테이블 재생성"""
    logger.info("Initializing database...")
    
    metadata = MetaData()  # ✅ 올바른 MetaData 객체 생성
    metadata.reflect(bind=engine)  # 기존 테이블 정보 로드
    
    # 기존 테이블 삭제 (필요한 경우)
    messages_table = metadata.tables.get("messages")
    if messages_table is not None:
        logger.info("🗑 기존 'messages' 테이블 삭제")
        with engine.connect() as connection:
            with connection.begin():  # ✅ 트랜잭션 처리
                connection.execute(text('DROP TABLE IF EXISTS messages CASCADE'))

    # 테이블 생성
    Base.metadata.create_all(bind=engine)  # ✅ Base.metadata 사용
    logger.info("✅ 데이터베이스 초기화 완료!")
    
def create_message(db: Session, role: str, content: str):  # ✅ SessionLocal → Session 변경
    """메시지 저장 및 메시지 이력 기록"""
    
    message = Message(role=role, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)

    # 메시지 이력 기록
    message_history = MessageHistory(
        message_id=message.id,
        role=role,
        content=content,
        created_at=datetime.datetime.utcnow()
    )
    db.add(message_history)
    db.commit()

    return message