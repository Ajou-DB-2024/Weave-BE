from app.db import run_query
from datetime import datetime
from app.apis.ApplyAPI.repository.query import SEARCH_RECRUIT, INSERT_SUBMISSION, INSERT_ANSWER, GET_SUBMISSION_ID, SELECT_QUESTION_ANSWERS, SELECT_SUBMISSION_LIST, UPDATE_SUBMISSION_STATUS, GET_ADMISSION_LIST, GET_ADMISSION_RESULT, UPDATE_SUBMISSION_RESULT, GET_CLUB_ID_FROM_RECRUIT, UPDATE_ANNOUNCEMENT_STATUS, UPDATE_RECRUIT_END_DATE, SELECT_RECRUIT_DETAIL, SELECT_RECRUIT_LIST, GET_RECRUIT_STATUS, INSERT_RECRUIT

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
        """
        SUBMISSION 데이터를 삽입하고 생성된 submission_id를 반환합니다.
        """
        run_query(INSERT_SUBMISSION, (recruit_id, member_id, form_id, title))
        result = run_query(GET_SUBMISSION_ID, (recruit_id, member_id, form_id, title))
        return result[0]["submission_id"]

    @staticmethod
    def insert_answer(submission_id: int, question_id: int, value: str):
        """
        ANSWER 데이터를 삽입합니다.
        """
        run_query(INSERT_ANSWER, (submission_id, question_id, value))
    
    @staticmethod
    def get_question_answers(submission_id: int):
        try:
            result = run_query(SELECT_QUESTION_ANSWERS, (submission_id,))
            return result
        except Exception as e:
            raise Exception(f"Database error: {e}")
        
    @staticmethod
    def get_submission_list(member_id: int):
        try:
            result = run_query(SELECT_SUBMISSION_LIST, (member_id,))
            return result
        except Exception as e:
            raise Exception(f"Database error: {e}")
        
    @staticmethod
    def submit_submission(submission_id: int):
        """
        submission_id를 기반으로 지원서를 제출 상태로 업데이트.
        """
        try:
            run_query(UPDATE_SUBMISSION_STATUS, (submission_id,))
        except Exception as e:
            raise Exception(f"Database error occurred: {e}")
        
    @staticmethod
    def get_admission_list(member_id: int):
        """
        주어진 member_id에 대한 지원 목록 조회.
        """
        try:
            results = run_query(GET_ADMISSION_LIST, (member_id,))
            return results
        except Exception as e:
            raise Exception(f"Database error occurred: {e}")
        
    @staticmethod
    def get_admission_result(submission_id: int):
        """
        submission_id에 해당하는 지원 결과를 조회합니다.
        """
        try:
            result = run_query(GET_ADMISSION_RESULT, (submission_id,))
            return result[0] if result else None
        except Exception as e:
            raise Exception(f"Database error occurred: {e}")
        
    @staticmethod
    def set_submission_result(submission_id: int, status: str):
        """
        submission_id에 해당하는 지원자의 상태를 업데이트합니다.
        """
        try:
            run_query(UPDATE_SUBMISSION_RESULT, (status, submission_id))
        except Exception as e:
            raise Exception(f"Database error while updating submission result: {e}")

    @staticmethod
    def get_club_id_from_recruit(recruit_id: int) -> int:
        """
        recruit_id로 club_id를 조회합니다.
        """
        result = run_query(GET_CLUB_ID_FROM_RECRUIT, (recruit_id,))
        return result[0]["club_id"] if result else None

    """
    @staticmethod
    def update_recruit_announcement_status(recruit_id: int) -> bool:
        try:
            result = run_query(UPDATE_ANNOUNCEMENT_STATUS, (recruit_id,))
            return True if result else False
        except Exception as e:
            raise Exception(f"Database error: {e}")
    """
       
    @staticmethod
    def update_recruit_end_date(recruit_id: int, end_date: datetime):
        run_query(UPDATE_RECRUIT_END_DATE, (end_date, recruit_id))

    @staticmethod
    def get_recruit_detail(recruit_id: int):
        try:
            result = run_query(SELECT_RECRUIT_DETAIL, (recruit_id,))
            return result
        except Exception as e:
            raise Exception(f"Database error: {e}")
    
    @staticmethod
    def get_recruit_list(club_id: int):
        try:
            result = run_query(SELECT_RECRUIT_LIST, (club_id,))
            return result
        except Exception as e:
            raise Exception(f"Database error: {e}")
        
    @staticmethod
    def get_recruit_status(recruit_id: int):
        try:
            result = run_query(GET_RECRUIT_STATUS, (recruit_id,))
            if result:
                return result[0]
            return None
        except Exception as e:
            raise Exception(f"Database error: {e}")
        
    @staticmethod
    def create_recruit(recruit_name: str, recruit_start_date: str, recruit_end_date: str, form_id: int):
        try:
            run_query(INSERT_RECRUIT, (recruit_name, recruit_start_date, recruit_end_date, form_id))
        except Exception as e:
            raise Exception(f"Database error: {e}")