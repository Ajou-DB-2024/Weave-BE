from datetime import datetime
import os
from typing import Optional

from app.apis.ClubAPI.repository.repository import check_club_exist_by_id, check_club_exists, delete_file_from_db, find_club_by_name, find_clubs_by_tags, create_club, find_file_id_by_name, get_file_info, get_members_by_club_id, get_tag, map_file_to_club, save_file_to_db, unmap_file_from_club, update_club_detail, get_club_brief_summary
from app.apis.MemberAPI.service.college_service import AjouService

FILES_DIR = "files"  # 파일 저장 경로

async def upload_clubdetail_file(file, user_id: int, user_email: str, club_id: int):
    
    role = AjouService.get_member_role(user_id, club_id)
    if role not in ["PRESIDENT", "VICE_PRESIDENT"]:
        raise PermissionError("권한이 없습니다. (회장 또는 부회장만 접근 가능)") 
 
    try:
        # 현재 시간을 초 단위로 가져옴
        timestamp = int(datetime.utcnow().timestamp())

        # 파일 확장자 제거 후 파일 이름 설정
        file_extension = file.filename.split('.')[-1]
        save_filename = f"{timestamp}_{user_email.split('@')[0]}"

        # 지정된 경로에 파일 저장 (확장자 제거)
        file_location = os.path.join("files", save_filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # DB에 파일 정보 저장
        save_file_to_db(
            save_filename=save_filename,
            org_filename=file.filename,
            org_extension=file_extension,
            created_by=user_id
        )
        map_file_to_club(find_file_id_by_name(save_filename), club_id)

        return {"file_path": file_location, "original_filename": file.filename}
    
    except Exception as e:
        raise Exception(f"파일 업로드 중 오류가 발생했습니다: {str(e)}")

def download_club_file(file_id: int, user_id: int):
    # 파일 정보 확인
    file_info = get_file_info(file_id)
    if not file_info:
        raise ValueError("다운로드할 파일이 존재하지 않습니다.")
    if file_info["created_by"] != user_id:
        raise ValueError("파일을 다운로드할 권한이 없습니다.")

    # 파일 경로와 원본 파일명 반환
    file_path = os.path.join("files", file_info["save_filename"])
    if not os.path.exists(file_path):
        raise ValueError("파일이 서버에 존재하지 않습니다.")
    
    original_filename = f"{file_info['org_filename']}.{file_info['org_extension']}"
    return file_path, original_filename

def delete_club_file(file_id: int, user_id: int):
    # 파일 정보 확인
    file_info = get_file_info(file_id)
    if not file_info:
        raise ValueError("삭제할 파일이 존재하지 않습니다.")
    if file_info["created_by"] != user_id:
        raise ValueError("파일을 삭제할 권한이 없습니다.")

    # 파일 삭제
    file_path = os.path.join("files", file_info["save_filename"])
    if os.path.exists(file_path):
        os.remove(file_path)

    # DB에서 파일 삭제
    unmap_file_from_club(file_id)
    delete_file_from_db(file_id)

def find_clubs(name: Optional[str] = None, tag_ids: Optional[list[int]] = None):
    
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
                             location: Optional[str], user_id: int) -> None:
  
    role = AjouService.get_member_role(user_id, club_id) 
    if role not in ["PRESIDENT", "VICE_PRESIDENT"]:
        raise PermissionError("권한이 없습니다. (회장 또는 부회장만 접근 가능)") 

    #동아리 정보를 수정하는 서비스 함수.
    update_club_detail(club_id, description, study_count, award_count, edu_count, event_count, established_date, location)

def get_club_brief(club_id: int) -> dict:    
    if not check_club_exist_by_id(club_id):
        # 클럽이 없으면 예외 발생
        raise ValueError(f"Club with ID {club_id} not found.")
    return get_club_brief_summary(club_id)

def get_tags_by_catagory() -> list[dict]:
    try:
        result = get_tag()
        if not result:
           raise ValueError("There is no tags") 
        return result
    
    except Exception as e:
        raise ValueError(f"태그 목록을 가져오는 데 실패했습니다: {str(e)}")

def get_club_members(user_id: int, club_id: int) -> list[int]:
    role = AjouService.get_member_role(user_id, club_id)
    if role not in ["PRESIDENT", "VICE_PRESIDENT"]:
        raise PermissionError("권한이 없습니다. (회장 또는 부회장만 접근 가능)") 

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