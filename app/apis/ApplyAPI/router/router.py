from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.apis.ApplyAPI.service.apply_service import ApplyService
from app.apis.ApplyAPI.model.model import RecruitSearchRequest, SubmissionSave, MemberRequest, RecruitDeadline, RecruitCreate, VoteSubmission, RecruitResultOpenRequest

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
        # 지원서 저장 서비스 호출
        result = ApplyService.save_submission(data.dict())
        
        # 저장 성공 시 메시지와 리다이렉트 URL 반환
        response_data = {
            "message": "지원서가 저장되었습니다.",
            "redirect_url": "/apply/submission"  # 리다이렉트 URL 설정
        }
        return success_response(data=response_data)
    except Exception as e:
        return error_response(error="DATABASE_ERROR", message=str(e))
    
@router.get("/apply/submission/{submission_id}")
async def get_submission_answers(submission_id: int):
    """
    특정 submission_id에 해당하는 질문과 답변을 조회합니다.
    """
    try:
        answers_data = ApplyService.get_question_answers(submission_id)
        return success_response(data=answers_data)
    except Exception as e:
        return error_response(error="DATABASE_ERROR", message=str(e))
    
@router.post("/apply/submission/list")
async def get_submission_list(data: MemberRequest):
    """
    특정 member_id에 해당하는 지원서 목록을 조회합니다.
    """
    try:
        submission_list = ApplyService.get_submission_list(data.dict())
        return success_response(data=submission_list)
    except Exception as e:
        return error_response(error="DATABASE_ERROR", message=str(e))
    
@router.post("/apply/submission/submit")
async def submit_submission(submission_id: int):
    """
    submission_id를 기반으로 지원서를 제출합니다.
    """
    try:
        # 서비스 레이어 호출
        ApplyService.submit_submission(submission_id)
        return success_response(message="지원서가 제출되었습니다.")
    except Exception as e:
        return error_response(error="SUBMISSION_ERROR", message=str(e))
    
@router.get("/apply/admission/list")
async def get_admission_list(member_id: int):
    """
    member_id를 기반으로 지원 목록을 조회합니다.
    """
    try:
        admission_list = ApplyService.get_admission_list(member_id)
        if not admission_list:
            return success_response(message="지원 내역이 없습니다.", data=[])
        return success_response(data=admission_list)
    except Exception as e:
        return error_response(error="ADMISSION_LIST_ERROR", message=str(e))
    
@router.get("/apply/admission/result")
async def get_admission_result(submission_id: int):
    """
    submission_id를 기반으로 지원 결과를 조회합니다.
    """
    try:
        admission_result = ApplyService.get_admission_result(submission_id)
        if not admission_result:
            return success_response(message="지원 결과가 존재하지 않습니다.", data={})
        return success_response(data=admission_result)
    except Exception as e:
        return error_response(error="ADMISSION_RESULT_ERROR", message=str(e))
    
@router.post("/apply/recruit/result/vote")
async def vote_submission_result(data: VoteSubmission, request: Request):
    """
    임원진이 지원자에 대한 합/불 상태를 결정합니다.
    """
    try:
        # JWT 정보를 활용하여 member_id 추출
        member_info = request.state.member_info
        member_id = member_info.get("sub")

        result = ApplyService.vote_submission_result(
            member_id=member_id,
            recruit_id=data.recruit_id,
            submission_id=data.submission_id,
            status=data.status
        )
        return success_response(message="결정 완료", data=result)
    except PermissionError as pe:
        return error_response(error="PERMISSION_DENIED", message=str(pe))
    except Exception as e:
        return error_response(error="VOTE_ERROR", message=str(e))


@router.post("/apply/recruit/result/open")
async def open_recruit_result(data: RecruitResultOpenRequest, request: Request):
    """
    모집 결과를 발표합니다.
    """
    try:
        # Step 1. JWT 토큰에서 member_id 추출
        member_info = request.state.member_info  # middleware에서 설정된 정보
        member_id = member_info.get("sub")  # JWT에서 추출된 member_id

        # Step 2. recruit_id 검증
        recruit_id = data.recruit_id

        # Step 3. 결과 발표 처리 (Service 호출)
        result = ApplyService.open_recruit_result(member_id, recruit_id)
        return success_response(data=result)

    except ValueError as ve:
        return error_response(error="VALIDATION_ERROR", message=str(ve))
    except PermissionError as pe:
        return error_response(error="PERMISSION_DENIED", message=str(pe))
    except Exception as e:
        return error_response(error="INTERNAL_SERVER_ERROR", message=str(e))


@router.patch("/apply/recruit/deadline")
async def update_recruit_deadline(data: RecruitDeadline, request: Request):
    """
    리크루팅 종료 기간을 연장하거나 즉시 종료합니다.
    """
    try:
        member_info = request.state.member_info  # middleware에서 설정된 정보
        member_id = member_info.get("sub")  # JWT에서 추출된 member_id

        result = ApplyService.update_deadline(data.dict(), member_id)
        return success_response(data=result)
    except Exception as e:
        return error_response(error="UPDATE_FAILED", message=str(e))
    except PermissionError as pe:
        return error_response(error="PERMISSION_DENIED", message=str(pe))
    
@router.get("/apply/recruit/detail")
async def get_recruit_detail(recruit_id: int, request: Request):
    """
    리크루팅 상세 정보를 조회합니다.
    """
    try:
        member_info = request.state.member_info  # middleware에서 설정된 정보
        member_id = member_info.get("sub")  # JWT에서 추출된 member_id

        recruit_detail = ApplyService.get_recruit_detail({"recruit_id": recruit_id}, member_id)
        if not recruit_detail:
            return error_response(
                error="DETAIL_NOT_FOUND",
                message="No details found for the given recruit_id."
            )
        return success_response(data=recruit_detail)
    except Exception as e:
        return error_response(error="INTERNAL_SERVER_ERROR", message=str(e))
    except PermissionError as pe:
        return error_response(error="PERMISSION_DENIED", message=str(pe))
    
@router.get("/apply/recruit/list")
async def get_recruit_list(club_id: int, request: Request):
    """
    특정 club_id에 해당하는 리크루팅 목록을 조회합니다.
    """
    try:
        member_info = request.state.member_info  # middleware에서 설정된 정보
        member_id = member_info.get("sub")  # JWT에서 추출된 member_id

        recruit_list = ApplyService.get_recruit_list({"club_id": club_id}, member_id)
        if not recruit_list:
            return error_response(
                error="RECRUIT_NOT_FOUND",
                message="No recruits found for the given club_id."
            )
        return success_response(data=recruit_list)
    except Exception as e:
        return error_response(error="INTERNAL_SERVER_ERROR", message=str(e))
    
@router.get("/apply/recruit/status")
async def get_recruit_status(recruit_id: int, request: Request):
    """
    특정 recruit_id에 해당하는 리크루팅 상태를 조회합니다.
    """
    try:
        member_info = request.state.member_info  # middleware에서 설정된 정보
        member_id = member_info.get("sub")  # JWT에서 추출된 member_id

        recruit_status = ApplyService.get_recruit_status({"recruit_id": recruit_id}, member_id)
        if not recruit_status:
            return error_response(
                error="RECRUIT_STATUS_NOT_FOUND",
                message="Recruit status not found for the given recruit_id."
            )
        return success_response(data=recruit_status)
    except Exception as e:
        return error_response(error="INTERNAL_SERVER_ERROR", message=str(e))
    

@router.post("/apply/recruit/create")
async def create_recruit(data: RecruitCreate, request: Request):
    """
    리크루팅을 생성합니다.
    """
    try:
        member_info = request.state.member_info  # middleware에서 설정된 정보
        member_id = member_info.get("sub")  # JWT에서 추출된 member_id

        # ApplyService를 통해 리크루팅 생성
        result = ApplyService.create_recruit(data.dict(), member_id)

        # 성공 응답 반환
        response_data = {
            "message": "리크루팅 생성이 완료되었습니다.",
            "redirect_url": "/apply/recruit"
        }
        return JSONResponse(content=success_response(data=response_data))
    except ValueError as ve:
        # 입력 값 관련 에러 처리
        return error_response(error="VALIDATION_ERROR", message=str(ve))
    except Exception as e:
        # 일반 에러 처리
        return error_response(error="DATABASE_ERROR", message=str(e))