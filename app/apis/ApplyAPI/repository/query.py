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