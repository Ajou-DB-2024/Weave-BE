import pymysql
from typing import Any, List, Tuple
from app.config import settings

# 데이터베이스 연결 정보
DB_CONFIG = {
    "host": settings.MYSQL_HOST,
    "user": settings.MYSQL_USER,
    "password": settings.MYSQL_PASSWORD,
    "database": settings.MYSQL_DB,
    "port": settings.MYSQL_PORT,
    "cursorclass": pymysql.cursors.DictCursor,  # 결과를 딕셔너리 형태로 반환
}

def run_query(sql: str, params: Tuple[Any, ...] = ()) -> List[dict]:
    """
    주어진 SQL 문을 실행하고 결과를 반환하는 함수.

    Args:
        sql (str): 실행할 SQL문.
        params (Tuple[Any, ...]): SQL문의 파라미터 값.

    Returns:
        List[dict]: SQL 실행 결과.
    """
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # SQL 실행
            cursor.execute(sql, params)
            
            # SELECT 쿼리일 경우 결과 반환
            if sql.strip().lower().startswith("select"):
                result = cursor.fetchall()
                return result
            
            # INSERT, UPDATE, DELETE 쿼리일 경우 커밋
            connection.commit()
            return []
    except Exception as e:
        print(f"Database query failed: {e}")
        raise
    finally:
        connection.close()
