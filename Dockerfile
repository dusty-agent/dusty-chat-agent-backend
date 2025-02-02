# Python 3.9 이미지 사용 (필요에 따라 버전을 조정)
FROM python:3.10

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 앱 소스 복사
COPY . .

# uvicorn 실행 (host=0.0.0.0으로 설정하여 외부 접근 가능하게 함)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
