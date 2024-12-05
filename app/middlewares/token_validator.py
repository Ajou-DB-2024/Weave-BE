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
        try:
            # JWT 토큰 검증 및 디코딩
            payload = jwt.decode(token, settings.TOKEN_SECRET, algorithms=[settings.TOKEN_ALGORITHM])
            logger.info(f"JWT token is valid for member_id: {payload.get('sub')}")
            # JWT 정보를 request.state에 저장
            request.state.member_info = payload
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token has expired")
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            logger.warning("Invalid JWT token")
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            logger.error(f"Unexpected error in JWT validation: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error during JWT validation")

        return await call_next(request)