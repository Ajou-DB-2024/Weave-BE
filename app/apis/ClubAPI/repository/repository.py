from collections import defaultdict
from typing import Optional
from app.db import run_query
from . import query

def find_club_by_name(name: str) -> list[dict]: 
    #동아리 이름으로 동아리 조회
    return run_query(query.CLUB_FINDBY_NAME, (f"%{name}%",))

def find_clubs_by_tags(tag_ids: list[int]) -> list[dict]:
    #선택된 태그들에 해당하는 동아리들을 검색
    #모든 태그를 포함하는 동아리만 반환
    
    tag_count = len(tag_ids)
    sql = query.CLUB_FINDBY_TAGS(tag_count)  # 함수 호출로 수정
    return run_query(sql, (*tag_ids, tag_count))

def check_club_exists(name: str) -> bool:
    #동아리 이름이 이미 존재하는지 확인
    result = run_query(query.CLUB_NAME_CHECK, (name,))
    return result[0]['COUNT(*)'] > 0

def check_club_exist_by_id(club_id: int) -> bool:
    # 실제 DB 쿼리로 클럽을 조회
    try:
        result = run_query(query.CHECK_CLUB_EXIST, (club_id,))
        if result:
            return True  # 클럽이 존재하면
        return False  # 클럽이 없으면
    except Exception as e:
        raise ValueError(f"Database error occurred: {str(e)}")

def create_club(name: str, club_depart: str, club_type: str, president_id: int) -> dict:
    #동아리 추가
    run_query(query.ADD_CLUB, (name, club_depart, club_type))
    
    # 동아리 id를 반환
    result = run_query(query.CLUB_FINDBY_NAME, (name,))
    club_id = result[0]['id']

    # 동아리 디테일 테이블 추가
    run_query(query.ADD_CLUB_DETAIL, (club_id, None, 0, 0, 0, 0, None, None))
    # 동아리장 역할 추가
    run_query(query.ADD_CLUB_MANAGER, (president_id, club_id))

    return {"id": club_id, "name": name}

def update_club_detail(club_id: int, description: Optional[str] = None, study_count: Optional[int] = None, 
                       award_count: Optional[int] = None, edu_count: Optional[int] = None,
                       event_count: Optional[int] = None, established_date: Optional[str] = None, 
                       location: Optional[str] = None) -> None:
    # 수정된 값들을 튜플로 전달
    values = (description, study_count, award_count, edu_count, event_count, established_date, location, club_id)
    
    result = run_query(query.UPDATE_CLUB_DETAIL, values)
    if result:
        raise ValueError("detail value error.")

def get_club_brief_summary(club_id: int) -> dict:
    result = run_query(query.GET_CLUB_SUMMARY, (club_id, club_id))

    if not result:
        raise ValueError("동아리가 없습니다.")

    return result[0]

def get_members_by_club_id(club_id: int) -> list[dict]:
    return run_query(query.GET_MEMBERID_BY_CLUBID, (club_id,))

def save_file_to_db(save_filename: str, org_filename: str, org_extension: str, created_by: int):
    
    try: 
        params = (save_filename, org_filename, org_extension, created_by)
        run_query(query.FILE_UPLOAD, params)
    except Exception as e:
        raise Exception(f"파일 저장 중 오류가 발생했습니다: {str(e)}")
    
def get_file_info(file_id: int) -> dict:
    # 파일 정보 조회
    result = run_query(query.GET_FILE_INFO, (file_id,))
    return result[0] if result else None

def find_file_id_by_name(file_name: str) -> Optional[int]:

    try:
        result = run_query(query.GET_FILEID_BYFILENAME, (file_name,))
        return result[0]["id"] if result else None
    except Exception as e:
        raise Exception("파일 찾기 오류")

def map_file_to_club(file_id: int, club_id: int):
    run_query(query.MAP_FILE_CLUB, (file_id, club_id))

def delete_file_from_db(file_id: int):
    try:
        # DB에서 파일 정보 삭제
        run_query(query.DELETE_FILE, (file_id,))
    except Exception as e:
        raise Exception(f"파일 삭제 중 오류가 발생했습니다: {str(e)}")
    
def unmap_file_from_club(file_id: int):
    run_query(query.DELETE_FILE_MAP, (file_id))

def get_tag() -> list[dict]:
    try:
        result = run_query(query.GET_TAG)
        categories = defaultdict(list)
        category_names = {}

        # 카테고리별로 태그를 묶고, category_id와 category_name 매핑
        for row in result:
            categories[row['category_id']].append({
                "id": row['tag_id'],
                "name": row['tag_name']
            })
            # category_id에 해당하는 category_name 저장
            category_names[row['category_id']] = row['category_name']

        # 카테고리별로 태그 목록을 묶은 리스트 반환
        return [{
            "category": {
                "id": category_id,
                "text": category_names[category_id]  # category_id에 매칭된 category_name 참조
            },
            "selections": tags
        } for category_id, tags in categories.items()]
    except Exception as e:
        raise ValueError(f"태그 목록을 가져오는 데 실패했습니다: {str(e)}")