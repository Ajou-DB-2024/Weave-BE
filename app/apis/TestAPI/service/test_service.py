import jwt
from datetime import datetime, timedelta
from app.config import settings
from app.apis.TestAPI.repository import repository

class TestService:
  @staticmethod
  def generate_jwt(user_id: int, name: str, email: str) -> str:
      """
      JWT 생성
      """
      payload = {
          "sub": user_id,  # 사용자 ID
          "name": name,  # 사용자 이름
          "email": email,  # 사용자 이메일
          "iat": datetime.utcnow(),  # 토큰 생성 시간
          "exp": datetime.utcnow() + timedelta(hours=1)  # 만료 시간 (1시간 후)
      }
      token = jwt.encode(payload, settings.TOKEN_SECRET, algorithm=settings.TOKEN_ALGORITHM)
      return token
  
  def get_result():
    """
    예시데이터를 repository를 통해 가져와 처리합니다
    """
    
    data = repository.get_data(1)
    
    return {
      "requested_at": datetime.now(),
      "count": len(data),
      "results": data
    }
  
  