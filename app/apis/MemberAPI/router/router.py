from fastapi import APIRouter, Depends, Request

from app.apis.MemberAPI.model import Member
from app.apis.MemberAPI.service.auth_service import GCPService, WeaveAuthService
from app.apis.MemberAPI.service.college_service import AjouService
from app.common.response.formatter import error_response, success_response

router = APIRouter()

@router.get("/member/login")
async def get_login_url():
  try:
    authorization_url = GCPService.get_auth_url()
    return success_response(data={
      "url": authorization_url
    })
  except Exception as e:
    return error_response(str(e))

@router.get("/member/login/redirect")
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

@router.get("/member/profile")
async def get_logined_info(current_user: Member.Member = Depends(WeaveAuthService.digest_token)):
  return success_response(data=current_user)

@router.get("/member/club")
async def get_member_clubs(request: Request):
    """
    사용자가 가입한 동아리 정보를 조회합니다.
    """
    try:
        # JWT에서 member_id 가져오기
        member_info = request.state.member_info
        member_id = member_info.get("sub")

        # 동아리 정보 조회
        member_club_info = AjouService.get_member_club_info(member_id)
        return success_response(data=member_club_info)
    except ValueError as ve:
        return error_response(error="VALIDATION_ERROR", message=str(ve))
    except Exception as e:
        return error_response(error="INTERNAL_SERVER_ERROR", message=str(e))