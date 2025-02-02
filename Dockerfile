# Python 3.10 이미지 사용
FROM python:3.10

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 앱 소스 복사
COPY . .

# 포트 8080을 외부에 노출
EXPOSE 8080

# uvicorn 실행, 환경 변수 PORT 사용
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]
