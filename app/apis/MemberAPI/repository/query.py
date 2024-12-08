# Member API Query

# [GCP AUTH]
GCP_AUTH_TOKEN_SAVE = "INSERT INTO googleid (access_token, refresh_token, expire_date, member_id)  VALUES (%s, %s, %s, %s)"


# [MEMBER API]
MEMBER_CREATE = "INSERT INTO member (name, email, major, grade) VALUES (%s, %s, %s, %s)"

MEMBER_FINDBY_ID = "SELECT * FROM member WHERE id = %s"
MEMBER_FINDBY_EMAIL = "SELECT * FROM member WHERE email = %s"

FIND_MEMBER_ROLE = """
SELECT role
FROM BELONGING
WHERE member_id = %s AND club_id = %s
"""

GET_MEMBER_CLUB_BRIEF = """
SELECT 
    COUNT(DISTINCT club_id) AS join_count
FROM BELONGING
WHERE member_id = %s;
"""

GET_MEMBER_MANAGE_CLUBS = """
SELECT 
    C.id, 
    C.name
FROM CLUB C
JOIN BELONGING B ON C.id = B.club_id
WHERE B.member_id = %s AND B.role IN ('PRESIDENT', 'VICE_PRESIDENT', 'EXECUTIVE');
"""