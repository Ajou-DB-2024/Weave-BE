from typing import List, Optional
from app.db import run_query
import query

def find_club_by_name(name: str) -> List[dict]: 
    #동아리 이름으로 동아리 조회
    return run_query(query.CLUB_FINDBY_NAME, (f"%{name}%",))

def find_clubs_by_tags(tag_ids: List[int]) -> List[dict]:
    #선택된 태그들에 해당하는 동아리들을 검색
    #모든 태그를 포함하는 동아리만 반환
    
    tag_count = len(tag_ids)
    sql = query.CLUB_FINDBY_TAGS(tag_count)  # query.py에서 SQL 쿼리 가져오기
    
    # 태그 개수에 맞는 자리 표시자 생성
    placeholders = ', '.join(['%s'] * tag_count)
    sql = sql % placeholders
    return run_query(sql, (*tag_ids, tag_count))


def check_club_exists(name: str) -> bool:
    #동아리 이름이 이미 존재하는지 확인
    result = run_query(query.CLUB_NAME_CHECK, (name,))
    return result[0]['COUNT(*)'] > 0

def create_club(name: str, club_depart: str, club_type: str, president_id: int) -> dict:
    #동아리 추가
    
    # 동아리 존재 여부 확인
    if check_club_exists(name):
        raise ValueError("Club name already exists")

    run_query(query.ADD_CLUB, (name, club_depart, club_type))
    
    # 동아리 id를 반환
    result = run_query(query.CLUB_FINDBY_NAME, (name,))
    club_id = result[0]['id']

    # 동아리 디테일이 있다면 추가 
    # 디테일 정보가 제공되면 처리
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