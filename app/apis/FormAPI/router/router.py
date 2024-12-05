from fastapi import APIRouter, HTTPException
from app.apis.FormAPI.service.form_service import FormService
from app.apis.FormAPI.model.FormCreate import FormCreate
from app.common.response.formatter import success_response, error_response


router = APIRouter()

@router.post("/form/create/")
async def create_form(data: FormCreate):
    """
    클라이언트에서 전송된 폼 데이터를 기반으로 FORM을 생성합니다.
    """
    
    try:
        # 요청 데이터 검증 및 서비스 호출
        result = FormService.create_form(data.dict())
        return success_response(data=result)
    except ValueError as ve:
        # 값 검증 관련 예외 처리
        return error_response(error="VALIDATION_ERROR", message=str(ve))
    except ConnectionError as ce:
        # 데이터베이스 연결 관련 예외 처리
        return error_response(error="DATABASE_ERROR", message="Database connection failed. " + str(ce))
    except Exception as e:
        # 알 수 없는 예외 처리
        return error_response(error="UNKNOWN_ERROR", message="An unexpected error occurred: " + str(e))
    
@router.get("/form/{recruit_id}")
async def get_form(recruit_id: int):
    """
    특정 recruit_id에 해당하는 폼 데이터를 조회합니다.
    """
    try:
        form_data = FormService.get_form(recruit_id)
        if not form_data:
            # 에러 응답 반환
            return error_response(
                error="FORM_NOT_FOUND",
                message="Form not found for the given recruit_id."
            )
        return success_response(data=form_data)
    except Exception as e:
        # 일반 예외 처리
        return error_response(
            error="INTERNAL_SERVER_ERROR",
            message=str(e)
        )
    
@router.get("/form/{club_id}")
async def get_forms(club_id: int):
    """
    특정 club_id에 해당하는 모든 폼 데이터를 조회합니다.
    """
    try:
        forms = FormService.get_forms(club_id)
        if not forms:
            return error_response(
                error="FORMS_NOT_FOUND",
                message="No forms found for the given club_id."
            )
        return success_response(data=forms)
    except Exception as e:
        return error_response(
            error="INTERNAL_SERVER_ERROR",
            message=str(e)
        )

