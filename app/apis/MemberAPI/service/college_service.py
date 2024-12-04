import json
import os
import traceback

DEPART_MAP = {}
DEPARTMAP_FILEDIR = os.path.join(os.path.dirname(__file__), "../../../../", "data", "departmap.json")
try:
  with open(DEPARTMAP_FILEDIR, 'r', encoding='utf-8') as f:
    DEPART_MAP = json.load(f)
except FileNotFoundError:
  pass

class AjouService:

  def get_univ_depart(major: str):
    print(DEPART_MAP)
    try:
      search_major = major.replace("전공", "")
      
      if search_major not in DEPART_MAP:
        raise Exception
      
      univ_info = DEPART_MAP[search_major]
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