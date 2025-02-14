# backend/logs/log.py
import logging
import os

# 로그 파일 저장 경로 지정: 현재 작업 디렉토리 기준으로 "logs/app.log"
log_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "app.log")
print("Logs directory:", log_dir)

# 로그 설정: 콘솔과 파일에 동시에 기록되도록 설정합니다.
logging.basicConfig(
    filename="backend.logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    encoding="utf-8",
    handlers=[
        logging.StreamHandler(),          # 콘솔 출력
        logging.FileHandler(log_file)       # 파일 출력
    ]
)

# 필요하다면, logger 인스턴스를 가져옵니다.
logger = logging.getLogger(__name__)
logger.info("로그가 파일과 콘솔에 모두 기록됩니다.")