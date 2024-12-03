from fastapi import APIRouter, Request

from app.apis.TestAPI.service.test_service import TestService
from app.common.response.formatter import success_response

router = APIRouter()

@router.get("/test")
async def test(request: Request):
  result = TestService.get_result()
  return success_response(data=result)