from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from app.apis.ClubAPI.service.club_service import find_clubs, create_new_club, update_club_information
from pydantic import BaseModel

router = APIRouter()

class ClubDetail(BaseModel):
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

@router.patch("/club/detail")
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
