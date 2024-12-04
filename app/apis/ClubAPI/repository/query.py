CLUB_FINDBY_NAME = "SELECT id, name FROM CLUB WHERE name LIKE %s"
CLUB_FINDBY_TAGS = """
    SELECT DISTINCT club.id, club.name
    FROM CLUB club
    JOIN TAGMAP tagmap ON club.id = tagmap.club_id
    WHERE tagmap.tag_id IN (%s)
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
