# Member API Query

# [GCP AUTH]
GCP_AUTH_TOKEN_SAVE = "INSERT INTO TABLE googleid VALUES(%s, %s, %s, %s, %s, %s)"


# [MEMBER API]
MEMBER_CREATE = "INSERT INTO TABLE member (created_at, name, email, phone) VALUES(%s, %s, %s, %s)"

MEMBER_FINDBY_ID = "SELECT * FROM member WHERE id = %s"
MEMBER_FINDBY_EMAIL = "SELECT * FROM member WHERE email = %s"
