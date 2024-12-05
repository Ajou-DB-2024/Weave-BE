SEARCH_RECRUIT = """
SELECT r.id AS recruit_id, r.name AS recruit_name, r.start_date, r.end_date, r.status,
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
    RECRUIT.status AS status,
    SUM(CASE WHEN SUBMISSION.is_announced = FALSE THEN 1 ELSE 0 END) AS pending_submissions,
    SUM(CASE WHEN SUBMISSION.is_announced = TRUE THEN 1 ELSE 0 END) AS announced_submissions
FROM SUBMISSION
JOIN RECRUIT ON SUBMISSION.recruit_id = RECRUIT.id
JOIN CLUB ON RECRUIT.club_id = CLUB.id
WHERE SUBMISSION.member_id = %s
GROUP BY RECRUIT.name, CLUB.name, CLUB.club_type, RECRUIT.status;
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

CHECK_IF_EXECUTIVE = """
SELECT 1
FROM BELONGING
WHERE member_id = %s AND club_id = %s AND role IN ('PRESIDENT', 'VICE_PRESIDENT', 'EXECUTIVE');
"""

UPDATE_ANNOUNCEMENT_STATUS = """
UPDATE RECRUIT
SET is_announced = TRUE
WHERE id = %s;
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
INSERT INTO RECRUIT (name, start_date, end_date, form_id, status)
VALUES (%s, %s, %s, %s, 'OPEN');
"""