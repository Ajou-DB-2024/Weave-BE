# Test API Query
CREATE_FORM = """
INSERT INTO FORM (created_by, title)
VALUES (%s, %s);
"""

INSERT_QUESTION = """
INSERT INTO QUESTION (num, title, type, form_id, is_required)
VALUES (%s, %s, %s, %s, %s);
"""

SELECT_FORM = """
SELECT id AS form_id
FROM FORM
WHERE created_by = %s AND title = %s
ORDER BY id DESC
LIMIT 1;
"""

GET_FORM_BY_RECRUIT_ID = """
SELECT f.id AS form_id, f.title, f.created_at, q.id AS question_id, q.num, q.title AS question_title, 
       q.type AS question_type, q.is_required
FROM FORM f
JOIN RECRUIT r ON r.form_id = f.id
LEFT JOIN QUESTION q ON q.form_id = f.id
WHERE r.id = %s;
"""

GET_FORMS_BY_CLUB_ID = """
SELECT f.id AS form_id, f.title, f.created_at, r.id AS recruit_id, r.name AS recruit_name,
       r.start_date, r.end_date
FROM FORM f
JOIN RECRUIT r ON r.form_id = f.id
WHERE r.club_id = %s;
"""



# [TEST API]
TEST_FINDBY_ID = "SELECT * FROM member WHERE id = %s"