from app.db import run_query
from app.apis.NotificationAPI.repository.query import (
    GET_NOTIFICATION_BY_ID,
    GET_NOTIFICATIONS_BY_MEMBER_ID,
    GET_RESULT_ANNOUNCEMENT_COUNT,
    GET_SERVICE_ANNOUNCEMENT_COUNT,
    # GET_MEMBER_IDS_BY_RECRUIT_ID,
    # INSERT_NOTIFICATION,
    # INSERT_NOTIFICATION_MAP,
    # GET_RECRUIT_NAME,
    # GET_ALL_MEMBER_IDS,
    # INSERT_NOTIFICATION,
    # INSERT_NOTIFICATION_MAP,
    # GET_MEMBER_IDS_BY_RECRUIT_ID_AND_END_DATE
)

class NotificationRepository:
    @staticmethod
    def get_notification_by_id(notification_id: int) -> dict:
        """
        단건 알림 데이터를 조회합니다.
        """
        return run_query(GET_NOTIFICATION_BY_ID, (notification_id,))

    @staticmethod
    def get_notifications_by_member_id(member_id: int) -> list:
        """
        특정 회원의 알림 목록 데이터를 조회합니다.
        """
        return run_query(GET_NOTIFICATIONS_BY_MEMBER_ID, (member_id,))

    @staticmethod
    def get_result_announcement_count(member_id: int) -> list:
        result = run_query(GET_RESULT_ANNOUNCEMENT_COUNT, (member_id,))
        return result

    @staticmethod
    def get_service_announcement_count(member_id: int) -> list:
        result = run_query(GET_SERVICE_ANNOUNCEMENT_COUNT, (member_id,))
        return result


    # @staticmethod
    # def get_member_ids_by_recruit_id(recrWuit_id: int) -> list:
    #     """
    #     특정 recruit_id에 지원한 회원들의 ID를 반환합니다.
    #     """
    #     return [row[0] for row in run_query(GET_MEMBER_IDS_BY_RECRUIT_ID, (recruit_id,))]

    # @staticmethod
    # def get_recruit_name(recruit_id: int) -> str:
    #     """
    #     특정 recruit_id의 리크루팅 이름을 반환합니다.
    #     """
    #     result = run_query(GET_RECRUIT_NAME, (recruit_id,))
    #     return result[0][0] if result else None

    # @staticmethod
    # def insert_notification(notification_type: str, title: str, content: str):
    #     """
    #     알림 데이터를 삽입합니다.
    #     """
    #     run_query(INSERT_NOTIFICATION, (notification_type, title, content))

    # @staticmethod
    # def insert_notification_map(member_id: int):
    #     """
    #     Notification Map에 데이터를 삽입합니다.
    #     """
    #     run_query(INSERT_NOTIFICATION_MAP, (member_id,))

    # @staticmethod
    # def get_all_member_ids() -> list:
    #     """
    #     모든 회원 ID를 반환합니다.
    #     """
    #     return [row[0] for row in run_query(GET_ALL_MEMBER_IDS)]

    # @staticmethod
    # def insert_notification(notification_type: str, title: str, content: str):
    #     """
    #     알림 데이터를 삽입합니다.
    #     """
    #     run_query(INSERT_NOTIFICATION, (notification_type, title, content))

    # @staticmethod
    # def insert_notification_map(member_id: int):
    #     """
    #     Notification Map에 데이터를 삽입합니다.
    #     """
    #     run_query(INSERT_NOTIFICATION_MAP, (member_id,))

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

    # @staticmethod
    # def get_member_ids_by_recruit_id_and_end_date(recruit_id: int) -> list:
    #     """
    #     특정 recruit_id와 end_date가 하루 전인 회원들의 ID를 반환합니다.
    #     """
    #     return [row[0] for row in run_query(GET_MEMBER_IDS_BY_RECRUIT_ID_AND_END_DATE, (recruit_id,))]

    # @staticmethod
    # def get_recruit_name(recruit_id: int) -> str:
    #     """
    #     특정 recruit_id의 리크루팅 이름을 반환합니다.
    #     """
    #     result = run_query(GET_RECRUIT_NAME, (recruit_id,))
    #     return result[0][0] if result else None

    # @staticmethod
    # def insert_notification(notification_type: str, title: str, content: str):
    #     """
    #     알림 데이터를 삽입합니다.
    #     """
    #     run_query(INSERT_NOTIFICATION, (notification_type, title, content))

    # @staticmethod
    # def insert_notification_map(member_id: int):
    #     """
    #     Notification Map에 데이터를 삽입합니다.
    #     """
    #     run_query(INSERT_NOTIFICATION_MAP, (member_id,))
