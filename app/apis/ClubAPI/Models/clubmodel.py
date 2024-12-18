from typing import Optional
from pydantic import BaseModel
from dataclasses import dataclass

class MemberListResponse(BaseModel):
    member_ids: list[int]

    class Config:
        orm_mode = True

@dataclass
class ClubDetail(BaseModel):
    name: str
    club_depart: str
    club_type: str
    president_id: int

@dataclass
class ClubDetailEdit(BaseModel):
    club_id: int
    description: Optional[str] = None
    study_count: Optional[int] = None
    award_count: Optional[int] = None
    edu_count: Optional[int] = None
    event_count: Optional[int] = None
    established_date: Optional[str] = None
    location: Optional[str] = None
