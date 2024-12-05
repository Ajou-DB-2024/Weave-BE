from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
import jwt
from app.config import settings
from app.middlewares.log import get_logger

class JWTAuthMiddleware(BaseHTTPMiddleware):
    """
    JWT 인증 미들웨어
    """
    async def dispatch(self, request: Request, call_next):
        logger = get_logger("JWTAuthMiddleware")

        # Swagger UI 및 OpenAPI 문서 요청, TestAPI 요청은 예외 처리
        if (
            request.url.path.startswith("/docs")
            or request.url.path.startswith("/openapi.json")
            or request.url.path.startswith("/api/v0/test")
            or request.url.path.startswith("/api/v0/login")
        ):
            logger.info(f"Skipping JWT validation for path: {request.url.path}")
            return await call_next(request)

        # Authorization 헤더 확인
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning("Authorization header missing or invalid")
            raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
        
        token = auth_header.split(" ")[1]
        try:
            # JWT 토큰 검증
            jwt.decode(token, settings.TOKEN_SECRET, algorithms=[settings.TOKEN_ALGORITHM])
            logger.info("JWT token is valid")
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token has expired")
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            logger.warning("Invalid JWT token")
            raise HTTPException(status_code=401, detail="Invalid token")

        return await call_next(request)