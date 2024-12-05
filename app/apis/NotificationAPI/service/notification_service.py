from app.apis.NotificationAPI.repository.repository import NotificationRepository
from datetime import datetime


class NotificationService:
    @staticmethod
    def get_notification(noti_id: int) -> dict:
        """
        단건 알림 데이터를 반환합니다.
        """
        result = NotificationRepository.get_notification_by_id(noti_id)
        if not result:
            raise ValueError("Notification not found.")

        # 결과를 dict 형태로 가공
        notification = result[0]
        return {
            "notification_id": notification["notification_id"],
            "notification_type": notification["notification_type"],
            "title": notification["title"],
            "content": notification["content"],
            "created_at": notification["created_at"]
        }

    # @staticmethod
    # def get_notifications(member_id: int) -> dict:
    #     """
    #     특정 회원의 모든 알림 데이터를 반환합니다.
    #     """
    #     print(f"Fetching notifications for member_id: {member_id}")  # 디버깅용
    #     raw_notifications = NotificationRepository.get_notifications_by_member_id(member_id)
    #     print(f"Raw notifications: {raw_notifications}")  # 디버깅용

    #     notifications = [
    #         {
    #             "notification_id": row[0],
    #             "notification_type": row[1],
    #             "title": row[2],
    #             "content": row[3],
    #             "created_at": row[4],
    #         }
    #         for row in raw_notifications
    #     ]
    #     print(f"Processed notifications: {notifications}")  # 디버깅용

    #     result_announcement_count = NotificationRepository.get_result_announcement_count(member_id)
    #     service_announcement_count = NotificationRepository.get_service_announcement_count(member_id)

    #     print(f"Result announcement count: {result_announcement_count}")  # 디버깅용
    #     print(f"Service announcement count: {service_announcement_count}")  # 디버깅용

    #     return {
    #         "notifications": notifications,
    #         "result_announcement_count": result_announcement_count[0][0] if result_announcement_count else 0,
    #         "service_announcement_count": service_announcement_count[0][0] if service_announcement_count else 0,
    #     }


    


    # @staticmethod
    # def create_result_notifications(recruit_id: int):
    #     """
    #     결과 발표 알림을 생성합니다.
    #     """
    #     # 1. 지원한 회원들의 ID 가져오기
    #     member_ids = NotificationRepository.get_member_ids_by_recruit_id(recruit_id)
    #     if not member_ids:
    #         raise ValueError("No members found for the given recruit_id.")

    #     # 2. 리크루팅 이름 가져오기
    #     recruit_name = NotificationRepository.get_recruit_name(recruit_id)
    #     if not recruit_name:
    #         raise ValueError("Recruit name not found for the given recruit_id.")

    #     # 3. 각 회원에게 알림 생성
    #     for member_id in member_ids:
    #         title = f"리크루팅 {recruit_name} 결과 발표"
    #         content = f"리크루팅 '{recruit_name}'의 결과가 발표되었습니다."
    #         NotificationRepository.insert_notification("결과 발표", title, content)
    #         NotificationRepository.insert_notification_map(member_id)

    # @staticmethod
    # def create_announcement_notifications(notification_content: str):
    #     """
    #     공지사항 알림을 생성합니다.
    #     """
    #     # 1. 모든 회원 ID 가져오기
    #     member_ids = NotificationRepository.get_all_member_ids()
    #     if not member_ids:
    #         raise ValueError("No members found in the system.")

    #     # 2. 공지사항 알림 생성
    #     for member_id in member_ids:
    #         NotificationRepository.insert_notification(
    #             notification_type="공지사항",
    #             title="시스템 공지사항",
    #             content=notification_content
    #         )
    #         NotificationRepository.insert_notification_map(member_id)


    # @staticmethod
    # def create_closing_reminder_notifications(recruit_id: int):
    #     """
    #     지원 마감 알림을 생성합니다.
    #     """
    #     # 1. 리크루팅 이름 가져오기
    #     recruit_name = NotificationRepository.get_recruit_name(recruit_id)
    #     if not recruit_name:
    #         raise ValueError("Recruit not found for the given recruit_id.")

    #     # 2. end_date가 하루 전인 지원한 회원들의 ID 가져오기
    #     member_ids = NotificationRepository.get_member_ids_by_recruit_id_and_end_date(recruit_id)
    #     if not member_ids:
    #         raise ValueError("No members found with recruit_id and end_date condition.")

    #     # 3. 알림 생성
    #     for member_id in member_ids:
    #         title = f"리크루팅 {recruit_name} 지원 마감 임박"
    #         content = f"리크루팅 '{recruit_name}'의 지원 마감이 하루 남았습니다."
    #         NotificationRepository.insert_notification("지원 마감", title, content)
    #         NotificationRepository.insert_notification_map(member_id)
