# app/middlewares/log.py
import logging
from fastapi import Request
from time import time

# 기본 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/server.log", mode="a"),
    ],
)

# 공통 로거 생성
def get_logger(name: str):
    """
    이름을 기준으로 로거를 반환합니다.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:  # 핸들러 중복 방지
        handler = logging.FileHandler(f"logs/{name}.log", mode="a")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

async def log_requests(request: Request, call_next):
    """
    요청 및 응답을 로깅하는 미들웨어.
    """
    start_time = time()
    logger = get_logger("RequestLogger")
    logger.info(f"Incoming request: {request.method} {request.url}")

    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"Request failed: {request.method} {request.url} - {e}")
        raise

    duration = time() - start_time
    logger.info(f"Completed response: {response.status_code} ({duration:.2f}s)")
    return response