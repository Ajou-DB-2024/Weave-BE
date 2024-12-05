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
        print(f"[DEBUG] Fetching member IDs for recruit_id: {recruit_id}")
        result = run_query(GET_MEMBER_IDS_BY_RECRUIT_ID, (recruit_id,))
        print(f"[DEBUG] Member IDs fetched: {result}")  # 결과 확인
        return result

    @staticmethod
    def create_notification(notification_type: str, title: str, content: str):
        """
        알림을 생성하고 생성된 알림 ID를 반환합니다.
        """
        print(f"[DEBUG] Creating notification with type: {notification_type}, title: {title}, content: {content}")
        run_query(INSERT_NOTIFICATION, (notification_type, title, content))
        print("[DEBUG] Notification inserted. Fetching last inserted ID.")
        result = run_query("SELECT MAX(id) AS id FROM notification;")  # 마지막 삽입된 ID 확인
        print(f"[DEBUG] Last inserted notification ID: {result}")
        return result[0]["id"] if result else None

    # @staticmethod
    # def map_notification_to_member(member_id: int, notification_id: int) -> list:
    #     """
    #     회원과 알림 간의 매핑을 생성합니다.
    #     """
    #     print(f"[DEBUG] Mapping notification_id: {notification_id} to member_id: {member_id}")
    #     result = run_query(INSERT_NOTIFICATION_MAP, (member_id, notification_id))
    #     print(f"[DEBUG] Mapping result: {result}")
    #     return result
    
    @staticmethod
    def map_notification_to_member(member_id: int, notification_id: int) -> dict:
        """
        회원과 알림 간의 매핑을 생성하거나, 중복이 있는 경우 이를 무시하고 성공으로 간주합니다.
        """
        try:
            print(f"[DEBUG] Attempting to map notification_id: {notification_id} to member_id: {member_id}")

            # 중복 여부 확인
            existing = run_query(
                "SELECT COUNT(*) AS cnt FROM notification_map WHERE member_id = %s AND notification_id = %s",
                (member_id, notification_id)
            )
            if existing[0]["cnt"] > 0:
                print(f"[INFO] Mapping already exists for member_id: {member_id} and notification_id: {notification_id}")
                return {"status": "success", "message": "Mapping already exists"}

            # 매핑 생성
            result = run_query(INSERT_NOTIFICATION_MAP, (member_id, notification_id))
            print(f"[SUCCESS] Notification mapped successfully: {result}")
            return {"status": "success", "message": "Mapping created successfully"}

        except Exception as e:
            print(f"[ERROR] Failed to map member_id: {member_id} to notification_id: {notification_id}. Error: {e}")
            return {"status": "error", "message": str(e)}


    @staticmethod
    def get_all_member_ids() -> list:
        """
        모든 회원 ID를 조회합니다.
        """
        print("Fetching all member IDs...")
        result = run_query(GET_ALL_MEMBER_IDS)
        print(f"Member IDs fetched: {result}")
        return result

    @staticmethod
    def get_recruits_with_one_day_left() -> list:
        """
        end_date 하루 전인 리크루팅을 조회합니다.
        """
        print("Fetching recruits with end_date one day away.")
        result = run_query(GET_RECRUITS_WITH_ONE_DAY_LEFT)
        print(f"Recruits with one day left: {result}")
        return result

    @staticmethod
    def get_member_ids_by_recruit_id_all_submission(recruit_id: int) -> list:
        """
        특정 리크루팅에 지원한 회원 ID를 조회합니다.
        """
        print(f"Fetching member IDs for recruit_id: {recruit_id}")
        result = run_query(GET_MEMBER_IDS_BY_RECRUIT_ID_ALL_SUBMISSION, (recruit_id,))
        print(f"Member IDs fetched: {result}")
        return result

    


