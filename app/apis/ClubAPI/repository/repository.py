from typing import List, Optional
from app.db import run_query

def find_club_by_name(name: str) -> List[dict]: 
    #동아리 이름으로 동아리 조회
    
    sql = "SELECT id, name FROM CLUB WHERE name LIKE %s"
    return run_query(sql, (f"%{name}%",))

def find_club_by_id(club_id: int) -> List[dict]: 
    #동아리 ID로 동아리 조회
    
    sql = "SELECT id, name FROM CLUB WHERE id = %s"
    return run_query(sql, (club_id,))

def find_clubs_by_tags(tag_ids: List[int]) -> List[dict]:
    #선택된 태그들에 해당하는 동아리들을 검색
    #모든 태그를 포함하는 동아리만 반환
    
    tag_count = len(tag_ids)
    sql = """
    SELECT DISTINCT club.id, club.name
    FROM CLUB club
    JOIN TAGMAP tagmap ON club.id = tagmap.club_id
    WHERE tagmap.tag_id IN (%s)
    GROUP BY club.id
    HAVING COUNT(DISTINCT tagmap.tag_id) = %s
    """
    placeholders = ', '.join(['%s'] * tag_count)
    sql = sql % placeholders
    return run_query(sql, (*tag_ids, tag_count))
