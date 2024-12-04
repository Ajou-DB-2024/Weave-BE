from fastapi import APIRouter, Depends, Request

from app.apis.MemberAPI.model import Member
from app.apis.MemberAPI.service.auth_service import GCPService, WeaveAuthService
from app.common.response.formatter import error_response, success_response

router = APIRouter()

@router.get("/login")
async def get_login_url(request: Request):
  try:
    authorization_url = GCPService.get_auth_url(request.client.host)
    return success_response(data={
      "url": authorization_url
    })
  except Exception as e:
    return error_response(str(e))

@router.get("/login/redirect")
async def handle_login_redirect(request: Request):  
  try:
    gcp_token_info = GCPService.get_token(request)
    univ_member_info = GCPService.get_member_depart(gcp_token_info['access_token'])

    login_result = WeaveAuthService.login(univ_member_info, gcp_token_info)
    if not login_result['result']:
      raise Exception("Login Failed")
    
    return success_response(data={
      "logined_member": login_result["member"],
      "logined_token": login_result["jwt"],
      "new_member": login_result["auto_joined"]
    })
  except Exception as e:
    print(e)
    return error_response(str(e))

@router.get("/profile")
async def get_logined_info(current_user: Member.Member = Depends(WeaveAuthService.digest_token)):
  return success_response(data=current_user)
  