# Member API Query

# [GCP AUTH]
GCP_AUTH_TOKEN_SAVE = "INSERT INTO googleid (access_token, refresh_token, expire_date, member_id)  VALUES (%s, %s, %s, %s)"


# [MEMBER API]
MEMBER_CREATE = "INSERT INTO member (name, email, major, grade) VALUES (%s, %s, %s, %s)"

MEMBER_FINDBY_ID = "SELECT * FROM member WHERE id = %s"
MEMBER_FINDBY_EMAIL = "SELECT * FROM member WHERE email = %s"
