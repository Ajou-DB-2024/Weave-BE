import json
import os
import traceback

from app.apis.MemberAPI.repository.repository import find_member_role, get_member_club_brief, get_member_manage_clubs


DEPART_MAP = {}
DEPARTMAP_FILEDIR = os.path.join(os.path.dirname(__file__), "../../../../", "data", "departmap.json")
try:
  with open(DEPARTMAP_FILEDIR, 'r', encoding='utf-8') as f:
    DEPART_MAP = json.load(f)
except FileNotFoundError:
  pass

class AjouService:
  @staticmethod
  def get_member_role(member_id: int, club_id: int) -> str:
      """
      특정 member_id와 club_id에 대한 역할(role)을 반환합니다.
      """
      role = find_member_role(member_id, club_id)
      if not role:
          raise PermissionError("Member is not associated with the club or has no role assigned.")
      return role
  @staticmethod
  def get_member_club_info(member_id: int) -> dict:
      """
      사용자가 가입한 동아리 정보를 조회
      """
      from app.apis.ApplyAPI.service.apply_service import ApplyService # circular import 방지, 지연 로드

      if not member_id:
          raise ValueError("member_id is required")
      
      admission_list = ApplyService.get_admission_list(member_id)
      applied_count = len(admission_list)

      # 간단한 요약 정보
      brief_info = get_member_club_brief(member_id,applied_count)

      # 관리 중인 동아리 목록
      manage_clubs = get_member_manage_clubs(member_id)

      return {
          "brief": brief_info,
          "manage_clubs": manage_clubs
      }

  def get_univ_depart(major: str):
    print(DEPART_MAP)
    try:
      univ_info = {}

      if major not in DEPART_MAP:
        univ_info = {
          "college": major,
          "department": ""
        }
      
      univ_info = DEPART_MAP[major]
      return {
        "college": univ_info['college'],
        "department": univ_info['department'],
        "major": major
      }

    except Exception as e:
      print(e)
      traceback.format_exc()
      return None

  def get_univ_course(job: str):
    job_code = job[:6]
    if job_code == "SS0001":
      return "학부과정"
    if job_code == "SS0002":
      return "학사수료"
    elif job_code == "GS0001":
      return "석사/박사과정"
    elif job_code == "GS0002":
      return "석사/박사수료"
    else:
      return "기타"
  
   