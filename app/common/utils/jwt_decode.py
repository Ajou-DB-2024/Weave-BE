import jwt
from app.config import settings
from fastapi import HTTPException
from app.middlewares.log import get_logger

logger = get_logger("JWT Decode Utility")

def decode_jwt_token(token: str) -> dict:
    """
    JWT 토큰을 디코드하여 payload 반환. 유효성 검증 및 예외 처리 포함.
    """
    try:
        payload = jwt.decode(token, settings.TOKEN_SECRET, algorithms=[settings.TOKEN_ALGORITHM])
        logger.info(f"JWT token successfully decoded for member_id: {payload.get('sub')}")
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token has expired")
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        logger.warning("Invalid JWT token")
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.error(f"Unexpected error during JWT decoding: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error during JWT decoding")