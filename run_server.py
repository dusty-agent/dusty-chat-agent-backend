import uvicorn
import signal

def shutdown():
    print("서버를 종료합니다...")
    raise SystemExit()

signal.signal(signal.SIGINT, lambda sig, frame: shutdown())
signal.signal(signal.SIGTERM, lambda sig, frame: shutdown())

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


# # 가상환경 활성화
# source venv/bin/activate     # macOS/Linux
# .\venv\Scripts\activate      # Windows
# # 의존성 설치
# pip install fastapi uvicorn
# # 스크립트 실행 (Windows)
# python run_server.py
# # 스크립트 실행 (macOS/Linux)
# python3 run_server.py
# # 터미널 출력 확인 : 스크립트 실행 시 Uvicorn 서버 시작, 다음 출력이 표시
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# # 프로덕션 환경에서?(개발환경)
# reload=False 설정 
# Uvicorn 직접 실행하지 X, Gunicorn 혹은 supervisord 같은 프로세스 관리 도구 사용을 추천!
# vs.reload=True 사용, 코드 변경 시 자동으로 서버 재시작 X
#