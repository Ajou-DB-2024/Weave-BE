from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from app.middlewares.log import get_logger
from app.common.utils.jwt_decode import decode_jwt_token
from app.common.response.formatter import error_response

class JWTAuthMiddleware(BaseHTTPMiddleware):
    """
    JWT 인증 미들웨어
    """
    async def dispatch(self, request: Request, call_next):
        logger = get_logger("JWTAuthMiddleware")

        # Swagger UI 및 OpenAPI 문서 요청, TestAPI 요청은 예외 처리
        excluded_paths = ["/docs", "/openapi.json", "/api/v0/test", "/api/v0/member/login"]
        if any(request.url.path.startswith(path) for path in excluded_paths):
            logger.info(f"Skipping JWT validation for path: {request.url.path}")
            return await call_next(request)

        # Authorization 헤더 확인
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning("Authorization header missing or invalid")
            return JSONResponse(
                status_code=401,
                content=error_response(
                    error="MISSING_AUTH_HEADER",
                    message="Authorization header is missing or invalid."
                )
            )

        token = auth_header.split(" ")[1]
        try:
            # JWT 토큰 디코딩
            payload = decode_jwt_token(token)
            request.state.member_info = payload
        except Exception as e:
            logger.error(f"Unexpected error during token validation: {e}")
            return JSONResponse(
                status_code=401,
                content=error_response(
                    error="INVALID_TOKEN",
                    message="The provided token is invalid or expired."
                )
            )

        return await call_next(request)