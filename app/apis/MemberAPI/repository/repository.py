
from datetime import datetime, timedelta
from typing import List
from app import db as DBQueryRunner
from app.apis.MemberAPI.model import Member
from . import query

from ..model.GoogleToken import GoogleOAuthToken

def save_gcp_token(member_id: int, token: GoogleOAuthToken) -> bool:
    params = (
        token['access_token'], 
        token['refresh_token'], 
        (datetime.now() + timedelta(seconds=token['expires_in'])).strftime('%Y-%m-%d %H:%M:%S'),
        member_id
    )
    DBQueryRunner.run_query(query.GCP_AUTH_TOKEN_SAVE, params)

    return True

def find_member(id: int) -> Member.DBSavedMember | None:
    service_member = DBQueryRunner.run_query(query.MEMBER_FINDBY_ID, id)

    if len(service_member) == 0:
        return None

    return service_member[0]

def find_members_by_email(email: str) -> List[Member.DBSavedMember]:
    service_member = DBQueryRunner.run_query(query.MEMBER_FINDBY_EMAIL, email)
    return service_member

def create_member(user_info: Member.Member) -> Member.Member:
    member_id = DBQueryRunner.run_query(
        query.MEMBER_CREATE,
        (
            user_info['name'], user_info['email'], 
            user_info['university']['major'], 
            user_info['university']['grade']
        )
    )
    user_info['id'] = member_id
    return user_info

def find_member_role(member_id: int, club_id: int) -> str:
    """
    DB에서 member_id와 club_id로 역할(role)을 찾습니다.
    """
    result = DBQueryRunner.run_query(query.FIND_MEMBER_ROLE, (member_id, club_id))
    return result[0]["role"] if result else None

@staticmethod
def get_member_club_brief(member_id: int, applied_count: int) -> dict:
    """
    사용자의 요약 동아리 정보 조회
    """
    try:
        # 가입한 동아리 개수 조회
        result = DBQueryRunner.run_query(query.GET_MEMBER_CLUB_BRIEF, member_id)
        join_count = result[0]["join_count"] if result else 0

        return {
            "join_count": join_count,
            "applied_count": applied_count
        }
    except Exception as e:
        raise Exception(f"Failed to fetch club brief info: {e}")

@staticmethod
def get_member_manage_clubs(member_id: int) -> list:
    """
    사용자가 관리 중인 동아리 정보 조회
    """
    result = DBQueryRunner.run_query(query.GET_MEMBER_MANAGE_CLUBS, (member_id,))
    return [{"id": row["id"], "name": row["name"]} for row in result]

    