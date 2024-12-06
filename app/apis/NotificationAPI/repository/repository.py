from app.db import run_query
from app.apis.NotificationAPI.repository.query import (
    GET_NOTIFICATION_BY_ID,
    GET_NOTIFICATIONS_BY_MEMBER_ID,
    GET_RESULT_ANNOUNCEMENT_COUNT,
    GET_SERVICE_ANNOUNCEMENT_COUNT,
    GET_MEMBER_IDS_BY_RECRUIT_ID,
    INSERT_NOTIFICATION,
    INSERT_NOTIFICATION_MAP,
    GET_ALL_MEMBER_IDS,
    GET_RECRUITS_WITH_ONE_DAY_LEFT,
    GET_MEMBER_IDS_BY_RECRUIT_ID_ALL_SUBMISSION,
    DUPLICATE_CHECK,
    GET_MAX_ID
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

    @staticmethod
    def get_member_ids_by_recruit_id(recruit_id: int):
        """
        주어진 recruit_id에 지원한 회원 ID를 조회합니다.
        """
        result = run_query(GET_MEMBER_IDS_BY_RECRUIT_ID, (recruit_id,))
        return result

    @staticmethod
    def create_notification(notification_type: str, title: str, content: str):
        """
        알림을 생성하고 생성된 알림 ID를 반환합니다.
        """
        run_query(INSERT_NOTIFICATION, (notification_type, title, content))
        result = run_query(GET_MAX_ID)  # 마지막 삽입된 ID 확인
        return result[0]["id"] if result else None
 
    @staticmethod
    def map_notification_to_member(member_id: int, notification_id: int) -> dict:
        """
        회원과 알림 간의 매핑을 생성하거나, 중복이 있는 경우 이를 무시하고 성공으로 간주합니다.
        """
        try:

            # 중복 여부 확인
            existing = run_query(DUPLICATE_CHECK,(member_id, notification_id))
            if existing[0]["cnt"] > 0:
                return {"status": "success", "message": "Mapping already exists"}

            # 매핑 생성
            run_query(INSERT_NOTIFICATION_MAP, (member_id, notification_id))
            return {"status": "success", "message": "Mapping created successfully"}

        except Exception as e:
            return {"status": "error", "message": str(e)}


    @staticmethod
    def get_all_member_ids() -> list:
        """
        모든 회원 ID를 조회합니다.
        """
        result = run_query(GET_ALL_MEMBER_IDS)
        return result

    @staticmethod
    def get_recruits_with_one_day_left() -> list:
        """
        end_date 하루 전인 리크루팅을 조회합니다.
        """
        result = run_query(GET_RECRUITS_WITH_ONE_DAY_LEFT)
        return result

    @staticmethod
    def get_member_ids_by_recruit_id_all_submission(recruit_id: int) -> list:
        """
        특정 리크루팅에 지원한 회원 ID를 조회합니다.
        """
        result = run_query(GET_MEMBER_IDS_BY_RECRUIT_ID_ALL_SUBMISSION, (recruit_id,))
        return result

    