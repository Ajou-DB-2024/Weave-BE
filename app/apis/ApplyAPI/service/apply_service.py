from app.apis.ApplyAPI.repository.repository import ApplyRepository

class ApplyService:
    @staticmethod
    def search_recruit(data: dict) -> list:
        """
        검색 조건에 따라 리크루팅 데이터를 반환합니다.
        """
        raw_data = ApplyRepository.search_recruit(data)
        recruits = []
        for row in raw_data:
            recruits.append({
                "recruit_id": row["recruit_id"],
                "recruit_name": row["recruit_name"],
                "start_date": row["start_date"],
                "end_date": row["end_date"],
                "status": row["status"],
                "club": {
                    "club_id": row["club_id"],
                    "club_name": row["club_name"]
                }
            })
        return recruits
    
    @staticmethod
    def save_submission(data: dict) -> dict:
        # 1. SUBMISSION 데이터 저장
        submission_id = ApplyRepository.insert_submission(
            recruit_id=data["recruit_id"],
            member_id=data["member_id"],
            form_id=data["form_id"],
            title=data["title"]
        )
        
        # 2. ANSWER 데이터 저장
        for answer in data["answers"]:
            ApplyRepository.insert_answer(
                submission_id=submission_id,
                question_id=answer["question_id"],
                value=answer["value"]
            )
        
        return {"submission_id": submission_id}
    
    @staticmethod
    def get_question_answers(submission_id: int):
        data = ApplyRepository.get_question_answers(submission_id)
        if not data:
            raise Exception("No answers found for the given submission")
        return data
    
    @staticmethod
    def get_submission_list(data: dict):
        member_id = data.get("member_id")
        if not member_id:
            raise Exception("member_id is required")
        
        submission_list = ApplyRepository.get_submission_list(member_id)
        if not submission_list:
            raise Exception("No submissions found for the given member_id")
        
        return submission_list