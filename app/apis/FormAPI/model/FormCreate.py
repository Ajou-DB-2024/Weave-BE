from pydantic import BaseModel
from typing import List

class Question(BaseModel):
    title: str
    type: str
    is_required: bool = False

class FormCreate(BaseModel):
    title: str
    created_by: int
    questions: List[Question]