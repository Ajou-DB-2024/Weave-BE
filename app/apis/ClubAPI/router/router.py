from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from app.apis.ClubAPI.service.club_service import find_clubs, create_new_club, update_club_information, get_club_brief
from app.apis.ClubAPI.Models.clubmodel import ClubDetail, ClubBriefResponse

router = APIRouter()

@router.get("/club/brief", response_model=ClubBriefResponse)
async def club_brief(club_id: int):
    try:
        result = get_club_brief(club_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/club/detailedit")
async def update_club_detail(request: ClubDetail):
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
        return {"message": "동아리 정보가 성공적으로 수정되었습니다."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/club/create")
async def create_club(request: ClubDetail): #동아리 추가
    
    result = create_new_club(
        name=request.name,
        club_depart=request.club_depart,
        club_type=request.club_type,
        president_id=request.president_id
    )

    if result.get("success"):
        return result
    raise HTTPException(status_code=400, detail=result.get("message"))

@router.get("/club/find")
def get_club(
    club_name: Optional[str] = None, 
    club_id: Optional[int] = None, 
    tag_ids: Optional[List[int]] = Query([], alias="tag_id")  # 여러 개의 태그 ID
):  
    return find_clubs(name=club_name, club_id=club_id, tag_ids=tag_ids)
