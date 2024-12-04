from app.db import run_query
from app.apis.ApplyAPI.repository.query import SEARCH_RECRUIT, INSERT_SUBMISSION, INSERT_ANSWER, GET_SUBMISSION_ID, GET_SUBMISSION_BY_ID

class ApplyRepository:
    @staticmethod
    def search_recruit(data: dict) -> list:
        """
        검색 조건에 따라 리크루팅 데이터를 조회합니다.
        """
        query = SEARCH_RECRUIT
        params = []

        # 조건 추가
        if "recruit_name" in data and data["recruit_name"]:
            query += " AND r.name LIKE %s"
            params.append(f"%{data['recruit_name']}%")

        if "tag_id" in data and data["tag_id"]:
            query += " AND t.id = %s"
            params.append(data["tag_id"])

        if "club_id" in data and data["club_id"]:
            query += " AND c.id = %s"
            params.append(data["club_id"])

        query += " ORDER BY r.start_date DESC"

        return run_query(query, tuple(params))
    
    @staticmethod
    def insert_submission(recruit_id: int, member_id: int, form_id: int, title: str) -> int:
        run_query(INSERT_SUBMISSION, (recruit_id, member_id, form_id, title))
        result = run_query(GET_SUBMISSION_ID, (recruit_id, member_id, form_id, title))
        return result[0]["submission_id"]  # 삽입된 submission_id 반환

    @staticmethod
    def insert_answer(submission_id: int, question_id: int, value: str):
        run_query(INSERT_ANSWER, (submission_id, question_id, value))
    
    @staticmethod
    def get_submission_by_id(submission_id: int) -> dict:
        try:
            result = run_query(GET_SUBMISSION_BY_ID, (submission_id,))
            return result[0] if result else None
        except Exception as e:
            raise Exception(f"Database error: {e}")