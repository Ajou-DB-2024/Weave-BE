import uvicorn
from app.config import settings

from fastapi import FastAPI
from app.middlewares.log import log_requests

from app.apis.TestAPI.router import router as TestRouter
from app.apis.MemberAPI.router import router as MemberRouter
from app.apis.FormAPI.router import router as FormRouter
from app.apis.ApplyAPI.router import router as ApplyRouter

# FastAPI 앱 생성
app = FastAPI(
    title="Weave API",  # 프로젝트 이름
    description="[Ajou Univ.] 2024-2 DB 팀 프로젝트 Backend",  # 설명
    version="0.1.0",  # API 버전
)

# 라우터 등록
app.include_router(TestRouter.router, prefix="/api/v0", tags=["Test"])
app.include_router(MemberRouter.router, prefix="/api/v0", tags=["Member"])
app.include_router(FormRouter.router, prefix="/api/v0", tags=["Form"])
app.include_router(ApplyRouter.router, prefix="/api/v0", tags=["Apply"])

# 미들웨어나 이벤트 핸들러 추가 가능
@app.middleware("http")
async def middleware_wrapper(request, call_next):
    return await log_requests(request, call_next)

# 애플리케이션 실행
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",  # "파일명:FastAPI 인스턴스"
        host="localhost",  # 호스트 주소 (로컬호스트)
        port=settings.PORT,        # 포트 번호
        reload=settings.PY_ENV == "development" # 코드 변경 시 자동 재시작 (개발용 옵션)
    )