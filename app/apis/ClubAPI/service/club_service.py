from typing import List, Optional
from app.apis.ClubAPI.repository.repository import find_club_by_name, find_clubs_by_tags, create_club
from app.common.response.formatter import success_response, error_response

def find_clubs(name: Optional[str] = None, club_id: Optional[int] = None, tag_ids: Optional[List[int]] = None):
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
