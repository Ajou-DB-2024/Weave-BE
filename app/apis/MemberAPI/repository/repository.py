
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

    