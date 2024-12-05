
from fastapi import APIRouter
from app.apis.NotificationAPI.service.notification_service import NotificationService
from app.common.response.formatter import success_response, error_response

router = APIRouter()

@router.get("/noti/{noti_id}")
async def get_notification(noti_id: int):
    """
    특정 알림 ID를 기반으로 단건 알림 데이터를 조회합니다.
    """
    try:
        print(f"Fetching notification for id: {noti_id}")  # 디버깅용 로그
        notification = NotificationService.get_notification(noti_id)
        if not notification:
            print(f"No notification found for id: {noti_id}")  # 디버깅용 로그
            return error_response(
                error="NOTIFICATION_NOT_FOUND",
                message="Notification not found for the given id."
            )
        print(f"Notification fetched successfully: {notification}")  # 디버깅용 로그
        return success_response(data=notification)
    except ValueError as ve:
        print(f"Validation Error: {ve}")  # 디버깅용 로그
        return error_response(error="VALIDATION_ERROR", message=str(ve))
    except Exception as e:
        print(f"Unhandled Error in get_notification: {e}")  # 디버깅용 로그
        return error_response(error="INTERNAL_SERVER_ERROR", message=str(e))


@router.get("/noti/list/{member_id}")
async def get_notifications(member_id: int):
    """
    특정 회원 ID를 기반으로 알림 목록을 조회합니다.
    """
    try:
        notifications = NotificationService.get_notifications(member_id)
        if not notifications["notifications"]:  # 알림 데이터가 없는 경우 처리
            return error_response(
                error="NOTIFICATIONS_NOT_FOUND",
                message="No notifications found for the given member_id."
            )
        return success_response(data=notifications)
    except ValueError as ve:
        return error_response(error="VALIDATION_ERROR", message=str(ve))
    except Exception as e:
        return error_response(error="INTERNAL_SERVER_ERROR", message=str(e))

@router.post("/notifications/result-announcement/{recruit_id}")
async def create_result_announcement_notifications(recruit_id: int):
    """
    결과 발표 시 관련 회원들에게 알림을 생성합니다.
    """
    try:
        print(f"[DEBUG] Received request to create notifications for recruit_id: {recruit_id}")
        NotificationService.create_result_notifications(recruit_id)
        return success_response(message="결과 발표 알림이 성공적으로 생성되었습니다.")
    except ValueError as ve:
        print(f"[ERROR] Validation Error: {ve}")
        return error_response(error="VALIDATION_ERROR", message=str(ve))
    except Exception as e:
        print(f"[ERROR] Internal Server Error: {e}")
        return error_response(error="INTERNAL_SERVER_ERROR", message=str(e))
    
"""curl 명령어로 post 호출 필요"""
@router.post("/notifications/announcement/")
async def create_announcement_notification(notification_type: str, title: str, content: str):
    """
    공지사항 알림을 생성하고 모든 회원에게 알림을 전송합니다.
    """
    try:
        print(f"Received announcement data: type={notification_type}, title={title}, content={content}")
        # 공지사항 알림 생성 서비스 호출
        NotificationService.create_announcement_notification(notification_type, title, content)
        print("Announcement notification created successfully.")
        return success_response(message="공지사항 알림이 성공적으로 생성되었습니다.")
    except ValueError as ve:
        print(f"Validation error occurred: {ve}")
        return error_response(error="VALIDATION_ERROR", message=str(ve))
    except Exception as e:
        print(f"Error occurred during announcement notification creation: {e}")
        return error_response(error="INTERNAL_SERVER_ERROR", message=str(e))



"""방법1: scheduler 설정하면 하루에 한 번 실행 가능 -> main.py 수정 필요. 그렇지 않으면 직접 호출해야 함. """
"""방법2: curl 명령어로 post 호출"""
@router.post("/notifications/closing-reminder/")
async def create_closing_reminder_notifications():
    """
    end_date 하루 전인 리크루팅에 대한 지원 마감 알림을 생성합니다.
    """
    try:
        NotificationService.create_closing_reminder_notifications()
        return success_response(message="지원 마감 알림이 성공적으로 생성되었습니다.")
    except Exception as e:
        print(f"Error occurred during closing reminder notification creation: {e}")
        return error_response(error="INTERNAL_SERVER_ERROR", message=str(e))