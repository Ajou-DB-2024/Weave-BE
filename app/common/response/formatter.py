# app/utils.py

from app.common.response.standard_response import StandardResponse

def success_response(data = None, message: str = "") -> dict:
    """
    성공 응답을 생성.
    """
    return StandardResponse(
        success=True,
        data=data,
        message=message
    ).dict()

def error_response(error: str, message: str = "") -> dict:
    """
    에러 응답을 생성.
    """
    return StandardResponse(
        success=False,
        error=error,
        message=message
    ).dict()
