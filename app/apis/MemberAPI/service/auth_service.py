from fastapi import HTTPException, Request

from .college_service import AjouService


import requests 
import urllib.parse

from app.config import settings

API_SCOPES = [
  "https://www.googleapis.com/auth/userinfo.profile",
  "https://www.googleapis.com/auth/contacts",
  "https://www.googleapis.com/auth/directory.readonly"
]

REDIRECT_URL = "http://%s:%s/api/v0/login/redirect"%(
  settings.HOST,
  settings.PORT
)

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth?scope=%s&access_type=offline&login_hint=%s&response_type=code&redirect_uri=%s&client_id=%s&prompt=consent" % (
    " ".join(API_SCOPES),
    urllib.parse.quote('@ajou.ac.kr', safe=''),
    REDIRECT_URL,
    settings.GOOGLE_CLIENT_ID,
  )

class GCPService:

  def get_auth_url():
    return AUTH_URL

  def get_token(request: Request):

    code = request.query_params.get("code")

    if not code:
      raise HTTPException(status_code=400, detail="Code not found")
    
    # 토큰 요청을 위한 데이터
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

  def get_user_depart(token: str):

    response = requests.get(
      url="https://people.googleapis.com/v1/people/me?personFields=names,coverPhotos,photos,emailAddresses,organizations,memberships", 
      headers={"Authorization": f"Bearer {token}"}
    )

    if response.status_code != 200:
      raise HTTPException(status_code=400, detail="Failed to get user info")

    user_info = response.json()
    univ_info = AjouService.get_univ_depart(user_info['organizations'][0]['department'])
    if not univ_info:
      raise HTTPException(status_code=400, detail="Failed to get univ info")
    univ_info['course'] = {
      "type": AjouService.get_univ_course(user_info['organizations'][0]['jobDescription']),
      "grade": user_info['organizations'][0]['title']
    }

    return {
       "name": user_info['names'][0]['displayName'],
       "email": user_info['emailAddresses'][0]['value'],
       "university": univ_info
    }

