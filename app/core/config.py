import os
from dotenv import load_dotenv
from urllib.parse import unquote  # URL 디코딩

# ✅ 환경 선택 (기본값: development)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# ✅ 적절한 .env 파일 로드
env_file = f".env.{ENVIRONMENT}"
if os.path.exists(env_file):
    load_dotenv(env_file)
else:
    raise FileNotFoundError(f"🚨 환경 파일 {env_file}이 존재하지 않습니다! 환경 설정을 확인하세요.")

class Config:
    ENV = ENVIRONMENT  # 현재 환경
    
    # DATABASE_URL을 디코딩하여 로드
    if ENV == "production":
        DATABASE_URL = unquote(os.getenv("DATABASE_URL_PROD"))
    else:
        DATABASE_URL = unquote(os.getenv("DATABASE_URL_DEV"))

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    API_BASE_URL = os.getenv("API_BASE_URL")
    DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

    # ✅ 필수 환경 변수 검증
    if not DATABASE_URL:
        missing_var = "DATABASE_URL_PROD" if ENV == "production" else "DATABASE_URL_DEV"
        raise ValueError(f"🚨 {missing_var} 환경 변수가 설정되지 않았습니다! .env.{ENVIRONMENT} 파일을 확인하세요.")

    if not OPENAI_API_KEY:
        raise ValueError("🚨 OPENAI_API_KEY 환경 변수가 설정되지 않았습니다! .env 파일을 확인하세요.")

config = Config()