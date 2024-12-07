SEARCH_RECRUIT = """
SELECT r.id AS recruit_id, r.name AS recruit_name, r.start_date, r.end_date,
       c.id AS club_id, c.name AS club_name
FROM RECRUIT r
JOIN CLUB c ON r.club_id = c.id
LEFT JOIN TAGMAP tm ON tm.club_id = c.id
LEFT JOIN TAG t ON t.id = tm.tag_id
WHERE 1=1
"""

INSERT_SUBMISSION = """
INSERT INTO SUBMISSION (recruit_id, member_id, form_id, title, submitted_at, is_submitted, is_announced)
VALUES (%s, %s, %s, %s, NOW(), FALSE, FALSE);
"""

INSERT_ANSWER = """
INSERT INTO ANSWER (submission_id, question_id, value)
VALUES (%s, %s, %s);
"""

SELECT_ANSWER = """
SELECT id
FROM ANSWER
WHERE submission_id = %s AND question_id = %s;
"""

GET_SUBMISSION_ID = """
SELECT id AS submission_id
FROM SUBMISSION
WHERE recruit_id = %s AND member_id = %s AND form_id = %s AND title = %s;
"""

SELECT_QUESTION_ANSWERS = """
SELECT 
    q.title AS question_title,
    a.value AS answer_value
FROM 
    ANSWER a
JOIN 
    QUESTION q ON a.question_id = q.id
WHERE 
    a.submission_id = %s;
"""

SELECT_SUBMISSION_LIST = """
SELECT 
    id AS submission_id
FROM 
    SUBMISSION
WHERE 
    member_id = %s;
"""

UPDATE_SUBMISSION_STATUS = """
UPDATE SUBMISSION
SET is_submitted = TRUE
WHERE id = %s;
"""

GET_ADMISSION_LIST = """
SELECT 
    RECRUIT.name AS recruit_name,
    CLUB.name AS club_name,
    CLUB.club_type AS club_type,
    SUM(CASE WHEN SUBMISSION.is_announced = FALSE THEN 1 ELSE 0 END) AS pending_submissions,
    SUM(CASE WHEN SUBMISSION.is_announced = TRUE THEN 1 ELSE 0 END) AS announced_submissions
FROM SUBMISSION
JOIN RECRUIT ON SUBMISSION.recruit_id = RECRUIT.id
JOIN CLUB ON RECRUIT.club_id = CLUB.id
WHERE SUBMISSION.member_id = %s
GROUP BY RECRUIT.name, CLUB.name, CLUB.club_type;
"""

GET_ADMISSION_RESULT = """
SELECT 
    RECRUIT.name AS recruit_name,
    SUBMISSION.result AS result
FROM SUBMISSION
JOIN RECRUIT ON SUBMISSION.recruit_id = RECRUIT.id
WHERE SUBMISSION.id = %s;
"""

UPDATE_SUBMISSION_RESULT = """
UPDATE SUBMISSION
SET result = %s
WHERE id = %s;
"""

UPDATE_ANNOUNCEMENT_STATUS = """
UPDATE SUBMISSION
SET is_announced = TRUE
WHERE recruit_id = %s;
"""

UPDATE_RECRUIT_END_DATE = """
UPDATE RECRUIT
SET end_date = %s
WHERE id = %s;
"""

SELECT_RECRUIT_DETAIL = """
SELECT 
    m.name AS member_name,
    m.id AS member_id,
    m.grade AS member_grade,
    m.major AS member_major,
    s.id AS submission_id
FROM 
    MEMBER m
JOIN 
    SUBMISSION s ON m.id = s.member_id
WHERE 
    s.recruit_id = %s;
"""

SELECT_RECRUIT_LIST = """
SELECT 
    id AS recruit_id,
    name AS recruit_name
FROM 
    RECRUIT
WHERE 
    club_id = %s;
"""

GET_RECRUIT_STATUS = """
SELECT 
    COUNT(*) AS total_applicants,
    SUM(CASE WHEN is_submitted = FALSE THEN 1 ELSE 0 END) AS draft_count,
    R.end_date
FROM RECRUIT R
LEFT JOIN SUBMISSION S ON R.id = S.recruit_id
WHERE R.id = %s
GROUP BY R.end_date
"""

INSERT_RECRUIT = """
INSERT INTO RECRUIT (name, start_date, end_date, form_id, club_id)
VALUES (%s, %s, %s, %s, %s);
"""

GET_CLUB_ID_FROM_RECRUIT = """
SELECT club_id
FROM RECRUIT
WHERE id = %s
"""

# 파일 정보를 저장
INSERT_FILE = """
INSERT INTO FILE (save_filename, org_filename, org_extension, created_by)
VALUES (%s, %s, %s, %s);
"""

# ANSWER_FILE 테이블에 매핑
INSERT_ANSWER_FILE = """
INSERT INTO ANSWER_FILE (file_id, answer_id, submission_id)
VALUES (%s, %s, %s)
"""


# 방금 삽입된 AUTO_INCREMENT ID 가져오기
GET_LAST_INSERTED_FILE_ID = """
SELECT MAX(id) AS id FROM FILE;
"""



# 특정 파일 정보 가져오기
GET_FILE_INFO_BY_ID = """
SELECT save_filename, org_filename, org_extension
FROM FILE
WHERE id = %s;
"""

# ANSWER_FILE에서 파일 매핑 삭제
DELETE_ANSWER_FILE = """
DELETE FROM ANSWER_FILE
WHERE file_id = %s;
"""

# FILE 테이블에서 파일 삭제
DELETE_FILE = """
DELETE FROM FILE
WHERE id = %s;
"""

# FILE 정보 조회 (파일 경로 확인용)
GET_FILE_INFO_BY_ID = """
SELECT save_filename
FROM FILE
WHERE id = %s;
"""

# 파일 정보를 저장
INSERT_FILE = """
INSERT INTO FILE (save_filename, org_filename, org_extension, created_by)
VALUES (%s, %s, %s, %s);
"""

# ANSWER_FILE 테이블에 매핑
INSERT_ANSWER_FILE = """
INSERT INTO ANSWER_FILE (file_id, answer_id, submission_id)
VALUES (%s, %s, %s)
"""


# 방금 삽입된 AUTO_INCREMENT ID 가져오기
GET_LAST_INSERTED_FILE_ID = """
SELECT MAX(id) AS id FROM FILE;
"""



# 특정 파일 정보 가져오기
GET_FILE_INFO_BY_ID = """
SELECT save_filename, org_filename, org_extension
FROM FILE
WHERE id = %s;
"""

# ANSWER_FILE에서 파일 매핑 삭제
DELETE_ANSWER_FILE = """
DELETE FROM ANSWER_FILE
WHERE file_id = %s;
"""

# FILE 테이블에서 파일 삭제
DELETE_FILE = """
DELETE FROM FILE
WHERE id = %s;
"""


