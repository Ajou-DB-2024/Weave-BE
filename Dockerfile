# 베이스 이미지 선택
FROM python:3.10-slim

# 작업 디렉터리 설정
WORKDIR /app

# 필요한 파일 복사
COPY ./app /app/app
COPY ./data /app/data
COPY requirements.txt /app

# 의존성 설치
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# FastAPI 앱 실행
CMD ["python", "-m", "app.main"]
