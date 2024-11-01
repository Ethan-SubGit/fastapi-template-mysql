from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import user, question
from app.core.database import init_db

app = FastAPI(
    title="FastAPI App",
    description="FastAPI Application with JWT authentication",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    # 개발 환경에서만 데이터베이스 초기화
    if settings.ENV != "production":
        print("데이터베이스 초기화 중...")
        # DB table을 계속 새로 생성하는거 중지
        # await init_db()

app.include_router(user.router, prefix=settings.API_V1_STR)
app.include_router(question.router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    

    return {
        "status": "healthy",
        "environment": settings.ENV
    }