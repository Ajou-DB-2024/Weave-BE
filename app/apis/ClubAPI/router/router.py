from fastapi import APIRouter, Query
from typing import List, Optional
from app.apis.ClubAPI.service.club_service import find_clubs

router = APIRouter()

@router.get("/club/find")
def get_club(
    club_name: Optional[str] = None, 
    club_id: Optional[int] = None, 
    tag_ids: Optional[List[int]] = Query([], alias="tag_id")  # 여러 개의 태그 ID
):
    """
    동아리 이름, ID, 태그를 기반으로 동아리 검색
    """
    return find_clubs(name=club_name, club_id=club_id, tag_ids=tag_ids)
