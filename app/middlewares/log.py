# app/middleware.py
import logging
from fastapi import Request
from time import time

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # 콘솔 출력
        logging.FileHandler("logs/server.log")  # 로그 파일 저장
    ]
)

async def log_requests(request: Request, call_next):
    """
    요청/응답 정보를 로깅하는 미들웨어 함수.
    """
    start_time = time()  # 요청 시작 시간 기록
    
    # 요청 정보 로그
    logging.info(f"Incoming request: {request.method} {request.url}")
    
    # 요청 처리
    response = await call_next(request)
    
    # 응답 시간 계산 및 로그 기록
    duration = time() - start_time
    logging.info(f"Completed response: {response.status_code} ({duration:.2f}s)")
    
    return response
