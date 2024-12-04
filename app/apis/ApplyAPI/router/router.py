from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.apis.ApplyAPI.service.apply_service import ApplyService
from app.apis.ApplyAPI.model.model import RecruitSearchRequest, SubmissionSave
from app.common.response.formatter import success_response, error_response

router = APIRouter()

@router.post("/apply/recruit/find")
async def search_recruit(data: RecruitSearchRequest):
    """
    입력된 조건에 따라 리크루팅 데이터를 검색합니다.
    """
    try:
        recruits = ApplyService.search_recruit(data.dict())
        if not recruits:
            return error_response(
                error="RECRUIT_NOT_FOUND",
                message="No recruits found for the given conditions."
            )
        return success_response(data=recruits)
    except Exception as e:
        return error_response(
            error="INTERNAL_SERVER_ERROR",
            message=str(e)
        )
    
@router.post("/apply/submission/save")
async def save_submission(data: SubmissionSave):
    """
    지원서를 임시 저장합니다.
    """
    try:
        # 데이터 저장 로직 호출
        result = ApplyService.save_submission(data.dict())
        
        # 저장 성공 시 메시지와 리다이렉트 URL 반환
        response_data = {
            "message": "지원서가 저장되었습니다.",
            "redirect_url": "/apply/submission"  # 리다이렉트 URL 설정
        }
        return JSONResponse(content=success_response(data=response_data))
    except Exception as e:
        return error_response(error="DATABASE_ERROR", message=str(e))