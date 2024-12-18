# 알림 단건 조회
GET_NOTIFICATION_BY_ID = """
SELECT id AS notification_id, notification_type, title, content, created_at
FROM NOTIFICATION
WHERE id = %s;
"""
# 알림 전체 조회
GET_NOTIFICATIONS_BY_MEMBER_ID = """
SELECT n.id AS notification_id, n.notification_type AS notification_type, n.title AS title, n.content AS content, n.created_at AS created_at
FROM NOTIFICATION n
JOIN notification_map nm ON n.id = nm.notification_id
WHERE nm.member_id = %s;
"""

GET_RESULT_ANNOUNCEMENT_COUNT = """
SELECT COUNT(*)
FROM NOTIFICATION n
JOIN notification_map nm ON n.id = nm.notification_id
WHERE nm.member_id = %s AND n.notification_type = '지원현황';
"""

GET_SERVICE_ANNOUNCEMENT_COUNT = """
SELECT COUNT(*)
FROM NOTIFICATION n
JOIN notification_map nm ON n.id = nm.notification_id
WHERE nm.member_id = %s AND n.notification_type = '공지사항';
"""

# # 결과 알림 생성
GET_MEMBER_IDS_BY_RECRUIT_ID = """
SELECT s.member_id
FROM SUBMISSION s
WHERE s.recruit_id = %s AND s.is_submitted = TRUE;
"""

INSERT_NOTIFICATION = """
INSERT INTO NOTIFICATION (notification_type, title, content)
VALUES (%s, %s, %s);
"""

INSERT_NOTIFICATION_MAP = """
INSERT INTO NOTIFICATION_MAP (member_id, notification_id)
VALUES (%s, %s);
"""

# # 회원 목록 조회
GET_ALL_MEMBER_IDS = """
SELECT id AS member_id FROM MEMBER;
"""

# end_date 하루 전인 리크루팅 ID 조회
GET_RECRUITS_WITH_ONE_DAY_LEFT = """
SELECT id, name
FROM RECRUIT
WHERE DATE(end_date) = DATE(NOW() + INTERVAL 1 DAY);
"""

# 특정 리크루팅에 지원한 회원 ID 조회
GET_MEMBER_IDS_BY_RECRUIT_ID_ALL_SUBMISSION = """
SELECT s.member_id
FROM SUBMISSION s
WHERE s.recruit_id = %s;
"""

# 중복 체크를 위한 COUNT
DUPLICATE_CHECK = """
SELECT COUNT(*) AS cnt FROM NOTIFICATION_MAP WHERE member_id = %s AND notification_id = %s
"""



GET_MAX_ID = """
SELECT MAX(id) AS id FROM NOTIFICATION;
"""