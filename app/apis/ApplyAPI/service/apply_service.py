from fastapi import UploadFile
from fastapi.responses import FileResponse
from app.apis.FormAPI.service.form_service import FormService
from app.apis.MemberAPI.service.college_service import AjouService
from app.apis.NotificationAPI.service.notification_service import NotificationService
from app.apis.ApplyAPI.repository.repository import ApplyRepository
from datetime import datetime

import os

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
    

    @staticmethod
    def open_recruit_result(member_id: int, recruit_id: int):
        """
        모집 결과를 발표합니다.
        """
        # Step 1. recruit_id로 club_id 조회
        club_id = ApplyRepository.get_club_id_from_recruit(recruit_id)
        if not club_id:
            raise ValueError("Invalid recruit_id. Club not found.")

        # Step 2. 임원진 권한 확인
        role = AjouService.get_member_role(member_id, club_id)
        if role not in ["PRESIDENT", "VICE_PRESIDENT", "EXECUTIVE"]:
            raise PermissionError("You do not have permission to open recruit results.")

        # Step 3. 결과 발표 상태 업데이트
        is_announced = ApplyRepository.update_recruit_announcement_status(recruit_id)
        if not is_announced:
            raise ValueError("Failed to update announcement status for the given recruit_id.")

        # Step 4. Notification 호출
        NotificationService.create_result_notifications(recruit_id)

        return {
            "message": "NotificationAPI로 결과 발표 알림이 전송되었습니다.",
            "redirect_url": "/apply/recruit/result"
        }


    @staticmethod
    def update_deadline(data: dict, member_id: int) -> dict:
        recruit_id = data["recruit_id"]
        end_date = data["end_date"]

        # Step 1. recruit_id로 club_id 조회
        club_id = ApplyRepository.get_club_id_from_recruit(recruit_id)
        if not club_id:
            raise ValueError("Invalid recruit_id. Club not found.")

        # Step 2. 임원진 권한 확인
        role = AjouService.get_member_role(member_id, club_id)
        if role not in ["PRESIDENT", "VICE_PRESIDENT", "EXECUTIVE"]:
            raise PermissionError("You do not have permission.")

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
    def get_recruit_detail(data: dict, member_id: int):
        recruit_id = data.get("recruit_id")
        if not recruit_id:
            raise ValueError("recruit_id is required")
        
         # Step 1. recruit_id로 club_id 조회
        club_id = ApplyRepository.get_club_id_from_recruit(recruit_id)
        if not club_id:
            raise ValueError("Invalid recruit_id. Club not found.")

        # Step 2. 임원진 권한 확인
        role = AjouService.get_member_role(member_id, club_id)
        if role not in ["PRESIDENT", "VICE_PRESIDENT", "EXECUTIVE"]:
            raise PermissionError("You do not have permission.")
        
        # Repository 호출
        recruit_detail = ApplyRepository.get_recruit_detail(recruit_id)
        return recruit_detail
    
    @staticmethod
    def get_recruit_list(data: dict, member_id: int):
        club_id = data.get("club_id")
        if not club_id:
            raise Exception("club_id is required")
        
        role = AjouService.get_member_role(member_id, club_id)
        if role not in ["PRESIDENT", "VICE_PRESIDENT", "EXECUTIVE"]:
            raise PermissionError("You do not have permission.")
        
        recruit_list = ApplyRepository.get_recruit_list(club_id)
        if not recruit_list:
            raise Exception("No recruits found for the given club_id")
        
        return recruit_list
    
    @staticmethod
    def get_recruit_status(data: dict, member_id: int):
        recruit_id = data.get("recruit_id")
        if not recruit_id:
            raise Exception("recruit_id is required")
        
        # Step 1. recruit_id로 club_id 조회
        club_id = ApplyRepository.get_club_id_from_recruit(recruit_id)
        if not club_id:
            raise ValueError("Invalid recruit_id. Club not found.")

        # Step 2. 임원진 권한 확인
        role = AjouService.get_member_role(member_id, club_id)
        if role not in ["PRESIDENT", "VICE_PRESIDENT", "EXECUTIVE"]:
            raise PermissionError("You do not have permission.")
        
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
    def create_recruit(data: dict, member_id: int):
        """
        리크루팅 생성 로직
        """
        club_id = data.get("club_id")        
        role = AjouService.get_member_role(member_id, club_id)
        if role not in ["PRESIDENT", "VICE_PRESIDENT", "EXECUTIVE"]:
            raise PermissionError("You do not have permission.")
        
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

    # 파일 업로드
    @staticmethod
    async def add_file(submission_id: int, answer_id: int, file: UploadFile):
        """
        파일을 저장하고 관련 정보를 DB에 추가합니다.
        """
        # 1. member 정보 가져오기 (email, member_id)
        member_info = ApplyRepository.get_member_info_by_submission(submission_id)
        if not member_info:
            raise ValueError(f"Submission ID {submission_id}에 대한 member 정보를 찾을 수 없습니다.")
        
        email = member_info["email"]
        member_id = member_info["id"]

        # 2. 원본 파일명 및 확장자 생성
        org_filename = file.filename
        org_extension = os.path.splitext(org_filename)[1].lstrip(".")

        # 3. 저장 파일명 생성
        timestamp = int(datetime.utcnow().timestamp())
        save_filename = f"{timestamp}_{email.split('@')[0]}"
        save_path = os.path.join("files", save_filename)

        # 4. 파일 저장
        with open(save_path, "wb") as f:
            f.write(await file.read())

        # 5. 파일 정보를 DB에 저장
        file_id = ApplyRepository.add_file(save_filename, org_filename, org_extension, created_by=member_id)

        # 6. 파일과 ANSWER 매핑
        ApplyRepository.map_file_to_answer(file_id, answer_id, submission_id)

    # 파일 다운로드
    @staticmethod
    def download_file(file_id: int) -> FileResponse:
        """
        파일 ID를 기준으로 파일을 찾아 다운로드를 처리합니다.
        """
        # 1. 파일 정보 조회
        file_info = ApplyRepository.get_file_info_by_id(file_id)
        if not file_info:
            raise ValueError(f"File with ID {file_id} does not exist.")
        
        # 2. 파일 경로 확인
        save_filename = file_info["save_filename"]
        org_filename = file_info["org_filename"]
        save_path = os.path.join("files", save_filename)
        
        if not os.path.exists(save_path):
            raise FileNotFoundError(f"File not found at path: {save_path}")
        
        # 3. FileResponse로 파일 응답
        return FileResponse(
            path=save_path,
            media_type="application/octet-stream",
            filename=org_filename  # 원본 파일명으로 다운로드 제공
        )
    
    @staticmethod
    def delete_file(file_id: int):
        """
        파일을 삭제하고 관련 정보를 DB에서 제거합니다.
        """
        # 1. 파일 정보 조회
        file_info = ApplyRepository.get_file_info_by_id(file_id)
        if not file_info:
            raise ValueError(f"File with ID {file_id} does not exist.")

        # 2. 파일 경로 확인 및 삭제
        save_filename = file_info["save_filename"]
        save_path = os.path.join("files", save_filename)

        if os.path.exists(save_path):
            os.remove(save_path)  # 실제 파일 삭제
        

        # 3. answer_file에서 매핑 삭제
        ApplyRepository.delete_answer_file_mapping(file_id)

        # 4. file 테이블에서 파일 정보 삭제
        ApplyRepository.delete_file(file_id)