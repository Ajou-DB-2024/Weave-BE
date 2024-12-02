# app/main.py
from fastapi import FastAPI
from app.routers import example_router  # 라우터 모듈 임포트

# FastAPI 앱 생성
app = FastAPI(
    title="My FastAPI Project",  # 프로젝트 이름
    description="This is a sample FastAPI project.",  # 설명
    version="0.1.0",  # API 버전
)

# 라우터 등록
app.include_router(example_router.router, prefix="/api/v1", tags=["Example"])

# 미들웨어나 이벤트 핸들러 추가 가능
@app.on_event("startup")
async def startup_event():
    print("Application is starting...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Application is shutting down...")
