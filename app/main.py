import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat, health, user, gpt_model
from app.database.init_db import init_db
from app.routers import auth, history

# 로깅 설정
logger = logging.getLogger(__name__)

# FastAPI 앱 초기화
app = FastAPI(title="DustyChatAgent API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(gpt_model.router, prefix="/api")

@app.get("/")  
def root():
    return {"message": "FastAPI is running!"}

@app.on_event("startup")
async def startup_event():
    from app.database.init_db import init_db
    init_db()