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

    @staticmethod
    def get_notifications(member_id: int) -> dict:
        """
        특정 회원의 모든 알림 데이터를 반환합니다.
        """
        raw_notifications = NotificationRepository.get_notifications_by_member_id(member_id)

        notifications = [
            {
                "notification_id": row["notification_id"],
                "notification_type": row["notification_type"],
                "title": row["title"],
                "content": row["content"],
                "created_at": row["created_at"]
            }
            for row in raw_notifications
        ]

        # 결과 발표 알림 개수와 서비스 공지사항 알림 개수 가져옴
        result_announcement_count = NotificationRepository.get_result_announcement_count(member_id)
        result_announcement_count = result_announcement_count[0]["COUNT(*)"] if result_announcement_count else 0

        service_announcement_count = NotificationRepository.get_service_announcement_count(member_id)
        service_announcement_count = service_announcement_count[0]["COUNT(*)"] if service_announcement_count else 0


        return {
            "notifications": notifications,
            "result_announcement_count": result_announcement_count,
            "service_announcement_count": service_announcement_count,
        }

    @staticmethod
    def create_result_notifications(recruit_id: int):
        """
        결과 발표 알림을 생성합니다.
        """
        
        # 1. recruit_id로 회원 ID 목록 조회
        member_ids = NotificationRepository.get_member_ids_by_recruit_id(recruit_id)

        if not member_ids:
            raise ValueError(f"No members found for recruit_id: {recruit_id}")

        # 2. 알림 생성
        notification_type = "결과 발표"
        notification_title = "결과 발표 알림"
        notification_content = f"리크루팅 {recruit_id}의 결과가 발표되었습니다."
        notification_id = NotificationRepository.create_notification(
            notification_type, notification_title, notification_content
        )

        # 3. 회원과 알림 매핑 생성
        for member in member_ids:
            NotificationRepository.map_notification_to_member(member["member_id"], notification_id)

    @staticmethod
    def create_announcement_notification(notification_type: str, title: str, content: str):
        """
        공지사항 알림을 생성하고 모든 회원에게 매핑합니다.
        """
        # 1. 알림 생성
        notification_id = NotificationRepository.create_notification(notification_type, title, content)

        # 2. 모든 회원 ID 조회
        member_ids = NotificationRepository.get_all_member_ids()
        if not member_ids:
            raise ValueError("No members found.")

        # 3. 회원과 알림 매핑 생성
        for member in member_ids:
            NotificationRepository.map_notification_to_member(member["member_id"], notification_id)

    @staticmethod
    def create_closing_reminder_notifications():
        """
        지원 마감 하루 전인 리크루팅에 대해 알림을 생성합니다.
        """
        # 1. end_date 하루 전인 리크루팅 조회
        recruits = NotificationRepository.get_recruits_with_one_day_left()
        if not recruits:
            return

        for recruit in recruits:
            recruit_id = recruit["id"]
            recruit_name = recruit["name"]

            # 2. 해당 리크루팅에 지원한 회원 ID 조회
            member_ids = NotificationRepository.get_member_ids_by_recruit_id_all_submission(recruit_id)

            if not member_ids:
                continue

            # 3. 알림 생성
            notification_type = "지원 마감"
            notification_title = "지원 마감 알림"
            notification_content = f"리크루팅 '{recruit_name}'의 지원 마감이 하루 남았습니다."
            notification_id = NotificationRepository.create_notification(
                notification_type, notification_title, notification_content
            )

            # 4. 회원-알림 매핑 생성
            for member in member_ids:
                NotificationRepository.map_notification_to_member(member["member_id"], notification_id)
