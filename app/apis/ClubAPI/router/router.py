from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from app.apis.ClubAPI.service.club_service import find_clubs, create_new_club
from pydantic import BaseModel

router = APIRouter()

class ClubCreateRequest(BaseModel):
    name: str
    club_depart: str
    club_type: str
    president_id: int
    description: Optional[str] = None
    study_count: Optional[int] = None
    award_count: Optional[int] = None
    edu_count: Optional[int] = None
    event_count: Optional[int] = None
    established_date: Optional[str] = None
    location: Optional[str] = None

@router.post("/club/create")
async def create_club(request: ClubCreateRequest):
    """
    동아리 추가
    """
    result = create_new_club(
        name=request.name,
        club_depart=request.club_depart,
        club_type=request.club_type,
        president_id=request.president_id
    )

    # 성공적인 결과 반환
    if result.get("success"):
        return result

    # 에러가 발생한 경우
    raise HTTPException(status_code=400, detail=result.get("message"))

@router.get("/club/find")
def get_club(
    club_name: Optional[str] = None, 
    club_id: Optional[int] = None, 
    tag_ids: Optional[List[int]] = Query([], alias="tag_id")  # 여러 개의 태그 ID
):
    """
    동아리 이름, 태그를 기반으로 동아리 검색
    """
    return find_clubs(name=club_name, club_id=club_id, tag_ids=tag_ids)
