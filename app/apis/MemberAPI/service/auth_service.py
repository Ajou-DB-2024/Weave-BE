import traceback
from typing import Dict
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

from app.apis.MemberAPI.model.GoogleToken import GoogleOAuthToken

from common.utils.jwt_decode import decode_jwt_token


from .college_service import AjouService
from ..repository import repository as MemberRepository

import jwt
import requests 
import urllib.parse

from passlib.context import CryptContext
from datetime import datetime, timedelta

from app.apis.MemberAPI.model import Member
from app.config import settings

API_SCOPES = [
  "https://www.googleapis.com/auth/userinfo.profile",
  "https://www.googleapis.com/auth/contacts",
  "https://www.googleapis.com/auth/directory.readonly"
]

REDIRECT_URL = settings.GOOGLE_REDIRECT_URL

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth?scope=%s&access_type=offline&login_hint=%s&response_type=code&redirect_uri=%s&client_id=%s&prompt=consent" % (
    " ".join(API_SCOPES),
    urllib.parse.quote('@ajou.ac.kr', safe=''),
    REDIRECT_URL,
    settings.GOOGLE_CLIENT_ID,
  )

class GCPService:

  def get_auth_url():
    return AUTH_URL

  def get_token(request: Request) -> GoogleOAuthToken:

    code = request.query_params.get("code")

    if not code:
      raise HTTPException(status_code=400, detail="Code not found")
    
    # 토큰 요청을 위한 데이터
    host = request.client.host
    if host == "127.0.0.1":
      host = "localhost"
    
    token_data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': REDIRECT_URL,
        'grant_type': 'authorization_code'
    }

    # 토큰 요청 보내기
    response = requests.post('https://oauth2.googleapis.com/token', data=token_data)

    # 응답 확인
    if response.status_code != 200:
        print(f"Failed to get access token. Status Code: {response.status_code}, Response: {response.text}")
        raise HTTPException(status_code=400, detail="Failed to get access token")
    
    token_info = response.json()
    return token_info

  def get_member_depart(token: str) -> Member.Member:

    response = requests.get(
      url="https://people.googleapis.com/v1/people/me?personFields=names,coverPhotos,photos,emailAddresses,organizations,memberships", 
      headers={"Authorization": f"Bearer {token}"}
    )

    if response.status_code != 200:
      raise HTTPException(status_code=400, detail="Failed to get user info")

    member_info = response.json()

    univ_info = AjouService.get_univ_depart(member_info['organizations'][0]['department'])
    if not univ_info:
      raise HTTPException(status_code=400, detail="Failed to get univ info")
    univ_info['grade'] = member_info['organizations'][0]['title']

    return {
       "name": member_info['names'][0]['displayName'],
       "email": member_info['emailAddresses'][0]['value'],
       "university": univ_info
    }

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 설정
SECRET_KEY = settings.TOKEN_SECRET  # 실제로는 보안에 취약하지 않은 랜덤한 값으로 설정해야 합니다.
ALGORITHM = settings.TOKEN_ALGORITHM
LOGIN_PERSIST_MINUTE = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def check_jwt_format(payload: dict):
  for key in ['sub', 'name', 'email', 'iat', 'exp']:
    if key not in payload:
      return False
  return True

class WeaveAuthService:

  def find_member_by_id(id: int) -> Member.Member | None:
    saved_member = MemberRepository.find_member(id)
    
    major = saved_member.pop("major")
    grade = saved_member.pop("grade")
    saved_member["university"] = AjouService.get_univ_depart(major)
    saved_member["university"]["grade"] = grade

    return saved_member

  def find_member_by_email(email: str) -> Member.Member | None:
    members = MemberRepository.find_members_by_email(email)
    if len(members) == 0:
      return None
    
    saved_member = members[0]
    
    major = saved_member.pop("major")
    grade = saved_member.pop("grade")
    saved_member["university"] = AjouService.get_univ_depart(major)
    saved_member["university"]["grade"] = grade
    
    return saved_member

  def join(member_info: Member.CommonMember) -> Member.Member:
    member = MemberRepository.create_member(member_info)

    print(f"User Joined: {member['name']} | {member['university']['college']} {member['university']['department']} {member['university']['grade']}")
    return member

  def login(univ_member: Member.Member, gcp_token: GoogleOAuthToken):
    try:
      service_member_info = WeaveAuthService.find_member_by_email(univ_member['email'])
      is_member_autojoined = False
      
      if not service_member_info:
        is_member_autojoined = True
        service_member_info = WeaveAuthService.join(univ_member)

      MemberRepository.save_gcp_token(service_member_info['id'], gcp_token)

      login_jwt = WeaveAuthService.create_token(service_member_info)

      return {
        "result": True, 
        "member": service_member_info,
        "auto_joined": is_member_autojoined,
        "jwt": login_jwt
      }
    
    except Exception as e:
      print(e)
      traceback.print_exc()
      return {"result": False}

  def create_token(member: Member.Member) -> str:
    
    iat = datetime.utcnow()
    payload = {
      'sub': member['id'],
      'name': member['name'],
      'email': member['email'],
      'iat': iat,
      'exp': iat + timedelta(minutes=LOGIN_PERSIST_MINUTE)
    }

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

  @staticmethod
  def authorize_token(token: str):
    """
    JWT 토큰 검증 및 멤버 ID 추출.
    """
    try:
        payload = decode_jwt_token(token)  # 유틸리티 함수 사용
        if "sub" not in payload:
            raise Exception("Invalid JWT format: 'sub' not found")
        return {
            "result": True,
            "member_id": payload["sub"]
        }
    except HTTPException as e:
        return {
            "result": False,
            "error": e.detail
        }

  def digest_token(token: str = Depends(oauth2_scheme)) -> Member.Member | None:
    try:
      auth_result = WeaveAuthService.authorize_token(token)
      print(auth_result)
      if not auth_result['result']:
        raise Exception("Authorization Failed")
      
      member_info = WeaveAuthService.find_member_by_id(auth_result['member_id'])
      return {
        "result": True,
        "is_logined": member_info is not None,
        "logined_member": member_info
      }
    
    except Exception as e:
        print(e)
        return {
          "result": False
        }

