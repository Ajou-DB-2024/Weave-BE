from app.apis.FormAPI.repository.repository import FormRepository
from datetime import datetime

class FormService:
    @staticmethod
    def create_form(data: dict, member_id: int) -> dict:

        # FORM 데이터 생성
        form_id = FormRepository.create_form(
            created_by=member_id,
            title=data["title"],
        )

        # 질문 데이터 생성
        FormRepository.insert_questions(form_id=form_id, questions=data["questions"])

        return {
            "id": form_id,
            "title": data["title"],
            "questions": data["questions"]
        }
    
    @staticmethod
    def get_form(recruit_id: int) -> dict:
        """
        특정 recruit_id에 해당하는 폼 데이터를 조회하고 응답 형식으로 변환합니다.
        """
        raw_data = FormRepository.get_form_by_recruit_id(recruit_id)
        if not raw_data:
            return None  # 데이터가 없는 경우

        # FORM 데이터 추출
        form_data = {
            "form_id": raw_data[0]["form_id"],
            "title": raw_data[0]["title"],
            "created_at": raw_data[0]["created_at"],
            "questions": []
        }

        # QUESTION 데이터 추가
        for row in raw_data:
            if row["question_id"]:  # 질문 데이터가 있는 경우만 추가
                form_data["questions"].append({
                    "question_id": row["question_id"],
                    "num": row["num"],
                    "title": row["question_title"],
                    "type": row["question_type"],
                    "is_required": row["is_required"]
                })

        return form_data
    
    @staticmethod
    def get_forms(club_id: int) -> list:
        """
        특정 club_id에 해당하는 폼 데이터를 조회하고 응답 형식으로 변환합니다.
        """
        raw_data = FormRepository.get_forms_by_club_id(club_id)
        if not raw_data:
            return []  # 데이터가 없을 경우 빈 리스트 반환

        # 폼 데이터 가공
        forms = []
        for row in raw_data:
            forms.append({
                "form_id": row["form_id"],
                "title": row["title"],
                "created_at": row["created_at"],
                "recruit": {
                    "recruit_id": row["recruit_id"],
                    "name": row["recruit_name"],
                    "start_date": row["start_date"],
                    "end_date": row["end_date"]
                }
            })
        return forms