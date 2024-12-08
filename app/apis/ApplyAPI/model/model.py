from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime

class RecruitSearchRequest(BaseModel):
    recruit_name: Optional[str] = None
    tag_id: Optional[int] = None
    club_id: Optional[int] = None

class ClubModel(BaseModel):
    club_id: int
    club_name: str

class RecruitResponse(BaseModel):
    recruit_id: int
    recruit_name: str
    start_date: Optional[str]
    end_date: Optional[str]
    club: ClubModel

class AnswerContent(BaseModel):
    question_id: int
    value: Optional[str]  = None # 답변 내용 (텍스트)
    file_id: Optional[int] = None # 첨부 파일 ID

class SubmissionSave(BaseModel):
    recruit_id: int
    submission_title: str
    answer_content: List[AnswerContent]

class MemberRequest(BaseModel):
    member_id: int

class RecruitResultOpenRequest(BaseModel):
    recruit_id: int

class RecruitDeadline(BaseModel):
    recruit_id: int
    end_date: Optional[datetime] = None

    @field_validator("end_date", mode="before")
    def validate_end_date(cls, value):
        """
        end_date가 없을 경우 None을 유지하거나 적절한 값으로 설정합니다.
        """
        if value is None:
            return None  # None을 유지 (즉시 종료)
        try:
            return datetime.fromisoformat(value) if isinstance(value, str) else value
        except ValueError:
            raise ValueError("Invalid datetime format for end_date. Use ISO 8601 format.")
        
class RecruitCreate(BaseModel):
    recruit_name: str = Field(..., description="리크루팅 이름")
    recruit_start_date: Optional[datetime] = None  # 입력값 없으면 DB에서 처리
    recruit_end_date: datetime = Field(..., description="리크루팅 종료 날짜")
    form_id: int = Field(..., description="연결할 폼 ID")
    club_id: int = Field(..., description="클럽 ID")

class VoteSubmission(BaseModel):
    recruit_id: int
    submission_id: int
    status: str
        