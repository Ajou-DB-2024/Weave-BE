
from app import db as DBQueryRunner
import query

from ..model.GoogleToken import GoogleOAuthToken

def save_token(token: GoogleOAuthToken):
    params = (
        token.access_token, 
        token.expires_in, 
        token.refresh_token, 
    )
    DBQueryRunner.run_query(query.GCP_AUTH_TOKEN_SAVE, params)

    return True

def find_member(id: int):
    service_member = DBQueryRunner.run_query(query.MEMBER_FINDBY_ID, str(id))

    if len(service_member) == 0:
        return None

    return service_member[0]

def find_members_by_email(email: str):
    service_member = DBQueryRunner.run_query(query.MEMBER_FINDBY_EMAIL, email)
    return service_member