from dataclasses import dataclass

@dataclass
class CommonMember:
  """
    공통 멤버타입 필드
  """
  name: str
  email: str
  major: str

@dataclass
class DBMember(CommonMember):
  """
    DB에 등록된 멤버가 가지고 있는 필드
  """
  id: int
  created_at: str

@dataclass
class DBSavedMember(DBMember):
  """
    DB에 저장된 멤버정보가 가지고 있는 필드
  """
  major: str

@dataclass
class MemberUnivInfo:
  college: str
  department: str
  major: str
  grade: str

@dataclass
class Member(DBMember):
  """
    서비스에서 사용되는 멤버객체의 타입
  """
  university: MemberUnivInfo
