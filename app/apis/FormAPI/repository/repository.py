from app.db import run_query
from app.apis.FormAPI.repository.query import CREATE_FORM, INSERT_QUESTION, SELECT_FORM, GET_FORM_BY_RECRUIT_ID, GET_FORMS_BY_CLUB_ID

class FormRepository:
    @staticmethod
    def create_form(created_by: int, title: str) -> int:
        """
        FORM 데이터를 삽입하고 생성된 form_id를 반환합니다.
        """
        # 1. FORM 데이터 삽입
        run_query(CREATE_FORM, (created_by, title))
        
        # 2. 마지막 삽입된 form_id 가져오기
        form_id_result = run_query(SELECT_FORM, (created_by, title))
        if not form_id_result:
            raise Exception("Failed to retrieve last inserted form_id")
        form_id = form_id_result[0]["form_id"]

        return form_id

    @staticmethod
    def insert_questions(form_id: int, questions: list):
        """
        FORM ID와 연결된 QUESTION 데이터를 삽입합니다.
        """
        # 3. QUESTION 데이터 삽입
        for idx, question in enumerate(questions, start=1):
            run_query(
                INSERT_QUESTION,
                (idx, question["title"], question["type"], form_id, question["is_required"])
            )

    @staticmethod
    def get_form_by_recruit_id(recruit_id: int) -> list:
        """
        특정 recruit_id에 해당하는 폼과 관련된 데이터를 조회합니다.
        """
        return run_query(GET_FORM_BY_RECRUIT_ID, (recruit_id,))
    
    @staticmethod
    def get_forms_by_club_id(club_id: int) -> list:
        """
        특정 club_id에 해당하는 모든 폼 데이터를 조회합니다.
        """
        return run_query(GET_FORMS_BY_CLUB_ID, (club_id,))