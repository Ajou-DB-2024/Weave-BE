from typing import List, Optional
from app.apis.ClubAPI.repository.repository import find_club_by_name, find_club_by_id, find_clubs_by_tags
from app.common.response.formatter import success_response, error_response

def find_clubs(name: Optional[str] = None, club_id: Optional[int] = None, tag_ids: Optional[List[int]] = None):
    # 동아리 이름으로 검색
    if name:
        clubs = find_club_by_name(name)
        if not clubs:
            return error_response(error="Not Found", message="No clubs found with that name")
        return success_response(data=clubs, message="Clubs retrieved successfully")
    
    # 동아리 ID로 검색
    if club_id:
        clubs = find_club_by_id(club_id)
        if not clubs:
            return error_response(error="Not Found", message="No club found with that ID")
        return success_response(data=clubs, message="Club retrieved successfully")
    
    # 태그 ID로 검색
    if tag_ids:
        clubs = find_clubs_by_tags(tag_ids)
        if not clubs:
            return error_response(error="Not Found", message="No clubs found with selected tags")
        return success_response(data=clubs, message="Clubs retrieved successfully")
    
    return error_response(error="Bad Request", message="No valid parameters provided")
