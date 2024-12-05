# 알림 단건 조회
GET_NOTIFICATION_BY_ID = """
SELECT id AS notification_id, notification_type, title, content, created_at
FROM notification
WHERE id = %s;
"""
# 알림 전체 조회
GET_NOTIFICATIONS_BY_MEMBER_ID = """
SELECT n.id AS notification_id, n.notification_type AS notification_type, n.title AS title, n.content AS content, n.created_at AS created_at
FROM notification n
JOIN notification_map nm ON n.id = nm.notification_id
WHERE nm.member_id = %s;
"""

GET_RESULT_ANNOUNCEMENT_COUNT = """
SELECT COUNT(*)
FROM notification n
JOIN notification_map nm ON n.id = nm.notification_id
WHERE nm.member_id = %s AND n.notification_type = '지원현황';
"""

GET_SERVICE_ANNOUNCEMENT_COUNT = """
SELECT COUNT(*)
FROM notification n
JOIN notification_map nm ON n.id = nm.notification_id
WHERE nm.member_id = %s AND n.notification_type = '공지사항';
"""

# # 결과 알림 생성
GET_MEMBER_IDS_BY_RECRUIT_ID = """
SELECT s.member_id
FROM submission s
WHERE s.recruit_id = %s AND s.is_submitted = TRUE;
"""

INSERT_NOTIFICATION = """
INSERT INTO notification (notification_type, title, content)
VALUES (%s, %s, %s);
"""

INSERT_NOTIFICATION_MAP = """
INSERT INTO notification_map (member_id, notification_id)
VALUES (%s, %s);
"""

# # 회원 목록 조회
GET_ALL_MEMBER_IDS = """
SELECT id AS member_id FROM member;
"""

# end_date 하루 전인 리크루팅 ID 조회
GET_RECRUITS_WITH_ONE_DAY_LEFT = """
SELECT id, name
FROM recruit
WHERE DATE(end_date) = DATE(NOW() + INTERVAL 1 DAY);
"""

# 특정 리크루팅에 지원한 회원 ID 조회
GET_MEMBER_IDS_BY_RECRUIT_ID_ALL_SUBMISSION = """
SELECT s.member_id
FROM submission s
WHERE s.recruit_id = %s;
"""



