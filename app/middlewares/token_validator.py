from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from app.middlewares.log import get_logger
from app.common.utils.jwt_decode import decode_jwt_token

class JWTAuthMiddleware(BaseHTTPMiddleware):
    """
    JWT 인증 미들웨어
    """
    async def dispatch(self, request: Request, call_next):
        logger = get_logger("JWTAuthMiddleware")

        # Swagger UI 및 OpenAPI 문서 요청, TestAPI 요청은 예외 처리
        excluded_paths = ["/docs", "/openapi.json", "/api/v0/test", "/api/v0/login"]
        if any(request.url.path.startswith(path) for path in excluded_paths):
            logger.info(f"Skipping JWT validation for path: {request.url.path}")
            return await call_next(request)

        # Authorization 헤더 확인
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning("Authorization header missing or invalid")
            raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

        token = auth_header.split(" ")[1]
        payload = decode_jwt_token(token)  # 유틸리티 함수 사용
        request.state.member_info = payload

        return await call_next(request)