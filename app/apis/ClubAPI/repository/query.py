CLUB_FINDBY_NAME = "SELECT id, name FROM CLUB WHERE name LIKE %s"

def CLUB_FINDBY_TAGS(tag_count: int) -> str:
    placeholders = ', '.join(['%s'] * tag_count)
    return f"""
    SELECT DISTINCT club.id, club.name
    FROM CLUB club
    JOIN TAGMAP tagmap ON club.id = tagmap.club_id
    WHERE tagmap.tag_id IN ({placeholders})
    GROUP BY club.id
    HAVING COUNT(DISTINCT tagmap.tag_id) = %s
    """
CLUB_NAME_CHECK = "SELECT COUNT(*) FROM CLUB WHERE name = %s"

ADD_CLUB = """
    INSERT INTO CLUB (name, club_depart, club_type)
    VALUES (%s, %s, %s)
    """
ADD_CLUB_MANAGER = """
    INSERT INTO BELONGING (member_id, club_id, role, join_date)
    VALUES (%s, %s, 'PRESIDENT', NOW())
    """
ADD_CLUB_DETAIL = """
    INSERT INTO CLUB_DETAIL (club_id, description, study_count, award_count, edu_count, event_count, established_date, location)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

UPDATE_CLUB_DETAIL = """
    UPDATE CLUB_DETAIL
    SET description = %s, study_count = %s, award_count = %s, edu_count = %s,
        event_count = %s, established_date = %s, location = %s
    WHERE club_id = %s
    """

GET_CLUB_SUMMARY = """
    SELECT 
        (SELECT COUNT(DISTINCT member_id) FROM BELONGING WHERE club_id = %s) AS total_members,
        (SELECT COUNT(DISTINCT submission.id) FROM SUBMISSION submission 
         JOIN RECRUIT recruit ON submission.recruit_id = recruit.id
         WHERE recruit.club_id = %s AND submission.is_submitted = TRUE) AS total_submissions
    """

GET_MEMBERID_BY_CLUBID = """
    SELECT id
    FROM MEMBER m
    JOIN BELONGING b ON m.id = b.member_id
    WHERE b.club_id = %s
    """

GET_ROLE_BY_CLUBID = """
    SELECT role
    FROM BELONGING 
    WHERE member_id = %s AND club_id = %s
    """

FILE_UPLOAD = """
            INSERT INTO FILE (save_filename, org_filename, org_extension, created_by)
            VALUES (%s, %s, %s, %s);
        """

GET_FILE_INFO = "SELECT save_filename, org_filename, org_extension, created_by FROM FILE WHERE id = %s;"

DELETE_FILE = "DELETE FROM FILE WHERE id = %s;"
