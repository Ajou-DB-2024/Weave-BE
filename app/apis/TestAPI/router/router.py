from fastapi import APIRouter, Request

from app.apis.TestAPI.service.test_service import TestService
from app.common.response.formatter import success_response, error_response

from app.config import settings

router = APIRouter()

@router.get("/test")
async def test(request: Request):
  result = TestService.get_result()
  return success_response(data=result)

@router.get("/test/check-env/")
async def check_env():
    """
    환경 변수의 로드 상태를 확인하는 API
    """
    return {
        "MYSQL_HOST": settings.MYSQL_HOST,
        "MYSQL_PORT": settings.MYSQL_PORT,
        "MYSQL_USER": settings.MYSQL_USER,
        "MYSQL_DB": settings.MYSQL_DB,
        "HOST": settings.HOST,
        "PORT": settings.PORT,
        "PY_ENV": settings.PY_ENV,
    }

@router.post("/test/generate-jwt/")
async def generate_jwt(user_id: int, name: str, email: str):
    """
    JWT 생성 API
    """
    try:
        token = TestService.generate_jwt(user_id=user_id, name=name, email=email)
        return success_response(data={"jwt": token})
    except Exception as e:
        return error_response(error="JWT_GENERATION_ERROR", message=str(e))