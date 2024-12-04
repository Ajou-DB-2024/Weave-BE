from pydantic import BaseModel
from typing import Optional, List

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
    status: str
    club: ClubModel

class Answer(BaseModel):
    question_id: int
    value: str

class SubmissionSave(BaseModel):
    recruit_id: int
    member_id: int
    form_id: int
    title: str
    answers: List[Answer]