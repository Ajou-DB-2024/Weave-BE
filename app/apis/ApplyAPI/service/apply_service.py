from app.apis.FormAPI.service.form_service import FormService
# from app.apis.NotificationAPI.service.notification_service import NotificationService
from app.apis.ApplyAPI.repository.repository import ApplyRepository
from app.apis.MemberAPI.service.college_service import AjouService
from datetime import datetime

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
        """
        지원서를 저장합니다.
        """
        # 1. FormAPI를 통해 FORM 데이터 가져오기
        form_data = FormService.get_form(data["recruit_id"])
        if not form_data:
            raise Exception("Form not found for the given recruit_id")

        # 2. SUBMISSION 데이터 저장
        submission_id = ApplyRepository.insert_submission(
            recruit_id=data["recruit_id"],
            member_id=data["member_id"],
            form_id=form_data["form_id"],
            title=data["submission_title"]
        )
        
        # 3. FORM의 질문 데이터 기반으로 ANSWER 저장
        for question, answer_content in zip(form_data["questions"], data["answer_content"]):
            ApplyRepository.insert_answer(
                submission_id=submission_id,
                question_id=question["question_id"],  # 질문 ID 추가
                value=answer_content or ""  # 답변이 없으면 빈 값으로 저장
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
    
    @staticmethod
    def submit_submission(submission_id: int):
        """
        지원서를 제출 상태로 업데이트합니다.
        """
        ApplyRepository.submit_submission(submission_id)

    @staticmethod
    def get_admission_list(member_id: int):
        """
        주어진 member_id에 대한 지원 목록 데이터를 가져옵니다.
        """
        return ApplyRepository.get_admission_list(member_id)
    
    @staticmethod
    def get_admission_result(submission_id: int):
        """
        submission_id를 기반으로 지원 결과 데이터를 가져옵니다.
        """
        return ApplyRepository.get_admission_result(submission_id)
    
    @staticmethod
    def vote_submission_result(member_id: int, recruit_id: int, submission_id: int, status: str):
        """
        recruit_id로 club_id를 찾아 역할을 확인하고 지원서 상태를 업데이트합니다.
        """
        # recruit_id를 통해 club_id 조회
        club_id = ApplyRepository.get_club_id_from_recruit(recruit_id)
        if not club_id:
            raise ValueError("Invalid recruit_id. Club not found.")

        # 역할 확인
        role = AjouService.get_member_role(member_id, club_id)
        if role == "MEMBER" or role is None:
            raise PermissionError("You do not have permission to vote.")

        # 지원서 상태 업데이트
        ApplyRepository.set_submission_result(submission_id, status)

        return {"submission_id": submission_id, "status": status}
    
    """
    @staticmethod
    def open_recruit_result(recruit_id: int):
        # Step 1. 결과 발표 상태 업데이트
        is_updated = ApplyRepository.update_recruit_announcement_status(recruit_id)
        if not is_updated:
            raise ValueError("Failed to update announcement status for the given recruit_id.")

        # Step 2. Notification 호출
        notification_data = {
            "recruit_id": recruit_id,
            "message": "지원 결과가 발표되었습니다."
        }
        NotificationService.create_notification(notification_data)

        return {
            "message": "결과 발표가 완료되었습니다.",
            "redirect_url": "/apply/recruit/result"
        }
    """

    @staticmethod
    def update_deadline(data: dict) -> dict:
        recruit_id = data["recruit_id"]
        end_date = data["end_date"]

        if not end_date:
            # 즉시 종료 처리
            ApplyRepository.update_recruit_end_date(recruit_id, datetime.now())
            message = "리크루팅을 마감하였습니다."
        else:
            # 기간 연장 처리
            ApplyRepository.update_recruit_end_date(recruit_id, end_date)
            message = "종료 기간이 연장되었습니다."

        return {
            "message": message,
            "redirect_url": "/apply/recruit"
        }
    
    @staticmethod
    def get_recruit_detail(data: dict):
        recruit_id = data.get("recruit_id")
        if not recruit_id:
            raise ValueError("recruit_id is required")
        
        # Repository 호출
        recruit_detail = ApplyRepository.get_recruit_detail(recruit_id)
        return recruit_detail
    
    @staticmethod
    def get_recruit_list(data: dict):
        club_id = data.get("club_id")
        if not club_id:
            raise Exception("club_id is required")
        
        recruit_list = ApplyRepository.get_recruit_list(club_id)
        if not recruit_list:
            raise Exception("No recruits found for the given club_id")
        
        return recruit_list
    
    @staticmethod
    def get_recruit_status(data: dict):
        recruit_id = data.get("recruit_id")
        if not recruit_id:
            raise Exception("recruit_id is required")
        
        # 데이터베이스 조회
        recruit_data = ApplyRepository.get_recruit_status(recruit_id)
        if not recruit_data:
            raise Exception("No data found for the given recruit_id")
        
        # 데이터 가공
        total_applicants = recruit_data["total_applicants"]
        draft_count = recruit_data["draft_count"]
        
        # 리크루팅 종료까지 남은 시간 계산
        now = datetime.now()
        end_date = recruit_data["end_date"]
        remaining_time = (end_date - now).total_seconds() if end_date > now else 0

        return {
            "total_applicants": total_applicants,
            "draft_count": draft_count,
            "remaining_time": max(remaining_time, 0)
        }
    
    @staticmethod
    def create_recruit(data: dict):
        """
        리크루팅 생성 로직
        """
        # FormService를 호출해 해당 클럽의 폼 목록을 가져옴
        forms = FormService.get_forms(data["club_id"])
        if not forms:
            raise ValueError("해당 클럽에 연결된 폼이 없습니다.")

        # 선택된 form_id가 유효한지 확인
        valid_form_ids = [form["form_id"] for form in forms]
        if data["form_id"] not in valid_form_ids:
            raise ValueError("선택된 폼 ID가 유효하지 않습니다.")

        # 리크루팅 데이터 삽입
        ApplyRepository.insert_recruit(
            name=data["recruit_name"],
            start_date=data["recruit_start_date"],
            end_date=data["recruit_end_date"],
            form_id=data["form_id"],
            club_id=data["club_id"]
        )