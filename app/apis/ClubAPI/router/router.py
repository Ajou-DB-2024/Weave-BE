from fastapi import APIRouter, Query
from typing import List, Optional
from app.apis.ClubAPI.service.club_service import find_clubs, create_new_club, get_club_members, update_club_information, get_club_brief
from app.apis.ClubAPI.Models.clubmodel import ClubDetail, ClubBriefResponse, ClubDetailEdit, MemberListResponse
from app.common.response.formatter import error_response, success_response

router = APIRouter()

@router.get("/club/members", response_model=MemberListResponse)
async def club_members(club_id: int = Query(...)):
    if not club_id:
        return error_response(error="INVALID_INPUT", message="club_id는 필수 입력입니다.")
    
    try:
        members = get_club_members(club_id)
        return success_response(data={"member_ids": members}, message="Club members retrieved successfully")
      
    except Exception as e:
        return error_response(error="SERVER_ERROR", message=str(e))

@router.get("/club/brief", response_model=ClubBriefResponse)
async def club_brief(club_id: int):
    try:
        result = get_club_brief(club_id)
        return success_response(data=result, message="Club brief retrieved successfully.")
        
    except ValueError as e:
        return error_response(error="NOT_FOUND", message=str(e))

@router.patch("/club/detailedit")
async def update_club_detail(request: ClubDetailEdit):
    try:
        update_club_information(
            request.club_id,
            request.description,
            request.study_count,
            request.award_count,
            request.edu_count,
            request.event_count,
            request.established_date,
            request.location
        )
        return success_response(data=None, message="동아리 정보가 성공적으로 수정되었습니다.")
    
    except ValueError as e:
        return error_response(error="INVALID_INPUT", message=str(e))

@router.post("/club/create")
async def create_club(request: ClubDetail):  # 동아리 추가
    try:
        result = create_new_club(
            name=request.name,
            club_depart=request.club_depart,
            club_type=request.club_type,
            president_id=request.president_id
        )
        if result.get("success"):
            return  success_response(data=result, message="Club created successfully")
        return error_response(error="INVALID_INPUT", message=result.get("message"))
    except Exception as e:
        return error_response(error="SERVER_ERROR", message=str(e))

@router.get("/club/find")
def get_club(
    club_name: Optional[str] = None, 
    tag_ids: Optional[List[int]] = Query([], alias="tag_id")  # 여러 개의 태그 ID
):  
    try:
        result = find_clubs(name=club_name, tag_ids=tag_ids)
        if not result.get("success"):
            return error_response(error="NOT_FOUND", message=result.get("message"))
        return success_response(data=result.get("data"), message=result.get("message"))
    
    except Exception as e:
        return error_response(error="SERVER_ERROR", message=str(e))
    except ValueError as ve:
        return error_response(error="VALUES_ERROR", message=str(ve))