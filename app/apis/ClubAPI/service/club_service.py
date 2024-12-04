from typing import List, Optional
from fastapi import HTTPException
from app.apis.ClubAPI.repository.repository import find_club_by_name, find_clubs_by_tags, create_club, get_members_by_club_id, update_club_detail, get_club_brief_summary
from app.common.response.formatter import success_response, error_response

def find_clubs(name: Optional[str] = None, tag_ids: Optional[List[int]] = None):
    # 동아리 이름으로 검색
    if name:
        clubs = find_club_by_name(name)
        if not clubs:
            return error_response(error="Not Found", message="No clubs found with that name")
        return success_response(data=clubs, message="Clubs retrieved successfully")
    
    # 태그 ID로 검색
    if tag_ids:
        clubs = find_clubs_by_tags(tag_ids)
        if not clubs:
            return error_response(error="Not Found", message="No clubs found with selected tags")
        return success_response(data=clubs, message="Clubs retrieved successfully")
    
    return error_response(error="Bad Request", message="No valid parameters provided")

def create_new_club(name: str, club_depart: str, club_type: str, president_id: int): # 동아리추가
    try:
        club = create_club(name, club_depart, club_type, president_id)
        return success_response(data=club, message="Club created successfully")
    except ValueError as e:
        return error_response(error="Conflict", message=str(e))
    except Exception as e:
        return error_response(error="Internal Server Error", message="An error occurred while creating the club")

def update_club_information(club_id: int, description: Optional[str], study_count: Optional[int], 
                             award_count: Optional[int], edu_count: Optional[int], 
                             event_count: Optional[int], established_date: Optional[str], 
                             location: Optional[str]) -> None:
    #동아리 정보를 수정하는 서비스 함수.
    
    update_club_detail(club_id, description, study_count, award_count, edu_count, event_count, established_date, location)


def get_club_brief(club_id: int) -> dict:
    return get_club_brief_summary(club_id)

def get_club_members(club_id: int) -> list[int]:
    try:
        members = get_members_by_club_id(club_id)
        if not members:
            raise HTTPException(status_code=404, detail="해당 동아리에 회원이 없습니다.")
        return [member["id"] for member in members]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))