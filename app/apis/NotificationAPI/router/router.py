
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


# @router.get("/noti/list/{member_id}")
# async def get_notifications(member_id: int):
#     """
#     특정 회원 ID를 기반으로 알림 목록을 조회합니다.
#     """
#     try:
#         print(f"Fetching notifications for member_id: {member_id}")  # 디버깅용 로그
#         notifications = NotificationService.get_notifications(member_id)
#         if not notifications["notifications"]:  # 알림 데이터가 없는 경우 처리
#             print(f"No notifications found for member_id: {member_id}")  # 디버깅용 로그
#             return error_response(
#                 error="NOTIFICATIONS_NOT_FOUND",
#                 message="No notifications found for the given member_id."
#             )
#         print(f"Notifications fetched successfully: {notifications}")  # 디버깅용 로그
#         return success_response(data=notifications)
#     except ValueError as ve:
#         print(f"Validation Error: {ve}")  # 디버깅용 로그
#         return error_response(error="VALIDATION_ERROR", message=str(ve))
#     except Exception as e:
#         print(f"Unhandled Error in get_notifications: {e}")  # 디버깅용 로그
#         return error_response(error="INTERNAL_SERVER_ERROR", message=str(e))


# @router.post("/notifications/result-announcement/{recruit_id}")
# async def create_result_announcement_notifications(recruit_id: int):
#     """
#     결과 발표 시 관련 회원들에게 알림을 생성합니다.
#     """
#     try:
#         print(f"Creating result notifications for recruit_id: {recruit_id}")  # 디버깅용 로그
#         NotificationService.create_result_notifications(recruit_id)
#         print(f"Result notifications created successfully for recruit_id: {recruit_id}")  # 디버깅용 로그
#         return success_response(message="결과 발표 알림이 성공적으로 생성되었습니다.")
#     except ValueError as ve:
#         print(f"Validation Error: {ve}")  # 디버깅용 로그
#         return error_response(error="VALIDATION_ERROR", message=str(ve))
#     except Exception as e:
#         print(f"Unhandled Error in create_result_announcement_notifications: {e}")  # 디버깅용 로그
#         return error_response(error="INTERNAL_SERVER_ERROR", message=str(e))


# @router.post("/notifications/announcement/")
# async def create_announcement_notifications(notification_content: str):
#     """
#     시스템 운영자가 공지사항을 입력하면 모든 회원에게 알림을 생성합니다.
#     """
#     try:
#         print(f"Creating announcement notifications with content: {notification_content}")  # 디버깅용 로그
#         NotificationService.create_announcement_notifications(notification_content)
#         print(f"Announcement notifications created successfully")  # 디버깅용 로그
#         return success_response(message="공지사항 알림이 성공적으로 생성되었습니다.")
#     except ValueError as ve:
#         print(f"Validation Error: {ve}")  # 디버깅용 로그
#         return error_response(error="VALIDATION_ERROR", message=str(ve))
#     except Exception as e:
#         print(f"Unhandled Error in create_announcement_notifications: {e}")  # 디버깅용 로그
#         return error_response(error="INTERNAL_SERVER_ERROR", message=str(e))


# @router.post("/notifications/closing-reminder/{recruit_id}")
# async def create_closing_reminder_notifications(recruit_id: int):
#     """
#     특정 리크루팅의 지원 마감 알림을 생성합니다.
#     """
#     try:
#         print(f"Creating closing reminder notifications for recruit_id: {recruit_id}")  # 디버깅용 로그
#         NotificationService.create_closing_reminder_notifications(recruit_id)
#         print(f"Closing reminder notifications created successfully for recruit_id: {recruit_id}")  # 디버깅용 로그
#         return success_response(message="지원 마감 알림이 성공적으로 생성되었습니다.")
#     except ValueError as ve:
#         print(f"Validation Error: {ve}")  # 디버깅용 로그
#         return error_response(error="VALIDATION_ERROR", message=str(ve))
#     except Exception as e:
#         print(f"Unhandled Error in create_closing_reminder_notifications: {e}")  # 디버깅용 로그
#         return error_response(error="INTERNAL_SERVER_ERROR", message=str(e))
