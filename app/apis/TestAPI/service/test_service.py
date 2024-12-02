from datetime import datetime

from app.apis.TestAPI.repository import repository

class TestService:
  
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