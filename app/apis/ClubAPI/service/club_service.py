from typing import List, Optional
from app.apis.ClubAPI.repository.repository import check_club_exists, find_club_by_name, find_clubs_by_tags, create_club, get_members_by_club_id, update_club_detail, get_club_brief_summary

def find_clubs(name: Optional[str] = None, tag_ids: Optional[List[int]] = None):
    
    # 동아리 이름으로 검색
    if name:
        clubs = find_club_by_name(name)
        if not clubs:
            return {"success": False, "data": None, "message": "No clubs found with that name"}
        return {"success": True, "data": clubs, "message": "Clubs retrieved successfully"}
    
    # 태그 ID로 검색
    if tag_ids:
        clubs = find_clubs_by_tags(tag_ids)
        if not clubs:
            return {"success": False, "data": None, "message": "No clubs found with that name"}
        return {"success": True, "data": clubs, "message": "Clubs retrieved successfully"}

def create_new_club(name: str, club_depart: str, club_type: str, president_id: int):
    try:
        # 동아리 이름 중복 확인
        if check_club_exists(name):
            raise ValueError("Club name already exists")

        # 동아리 생성
        club = create_club(name, club_depart, club_type, president_id)

        # 생성 성공 여부 확인
        if not club:
            raise Exception("Club creation failed due to an unknown reason")
        
        return club
    except ValueError as ve:
        # 특정 예외 처리
        raise ValueError(f"Validation Error: {str(ve)}")
    except Exception as e:
        # 일반 예외 처리
        raise Exception(f"An error occurred while creating the club: {str(e)}")

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
            raise Exception("There is no members")
        return [member["id"] for member in members]
    except ValueError as ve:
        # 특정 예외 처리
        raise ValueError(f"Validation Error: {str(ve)}")
    except Exception as e:
        # 일반 예외 처리
        raise Exception(f"get_club_members error: {str(e)}")