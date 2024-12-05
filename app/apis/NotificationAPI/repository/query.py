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

# # 공지사항 알림 생성
# GET_ALL_MEMBER_IDS = """
# SELECT id
# FROM member;
# """

# # end_date 하루 전인 리크루팅의 회원 ID 조회
# GET_MEMBER_IDS_BY_RECRUIT_ID_AND_END_DATE = """
# SELECT s.member_id
# FROM submission s
# JOIN recruit r ON s.recruit_id = r.id
# WHERE s.recruit_id = %s
#   AND s.is_submitted = TRUE
#   AND DATE(r.end_date) = DATE_SUB(CURDATE(), INTERVAL -1 DAY);
# """




