from fastapi import APIRouter

from app.common.response.formatter import success_response

router = APIRouter()

@router.get("/test")
async def test():
  result = {
    "message": "Hello, World!"
  }
  return success_response(data=result)