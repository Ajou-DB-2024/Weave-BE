from dataclasses import dataclass

from app.apis.MemberAPI.model import MemberUnivInfo

@dataclass
class Member:
  id: int
  created_at: str
  name: str
  email: str
  phone: str
  major: str

@dataclass
class ExtendedMember(Member):
  university: MemberUnivInfo

@dataclass
class MemberUnivInfo:
  college: str
  department: str
  major: str

@dataclass
class UnivCourse:
  type: str
  grade: str

