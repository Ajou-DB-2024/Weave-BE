from fastapi import APIRouter, Request

from app.apis.MemberAPI.service.auth_service import GCPService
from app.common.response.formatter import error_response, success_response

router = APIRouter()

@router.get("/login")
async def get_login_url():
  try:
    authorization_url = GCPService.get_auth_url()
    return success_response(data={
      "url": authorization_url
    })
  except Exception as e:
    return error_response(str(e))

@router.get("/login/redirect")
async def handle_login_redirect(request: Request):  
  try:
    gcp_token_info = GCPService.get_token(request)
    univ_user_info = GCPService.get_user_depart(gcp_token_info['access_token'])

    return success_response(data=univ_user_info)
  except Exception as e:
    print(e)
    return error_response(str(e))

