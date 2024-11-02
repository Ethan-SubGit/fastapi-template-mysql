from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import user, question
from app.core.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 개발 환경에서만 데이터베이스 초기화
    if settings.ENV != "production":
        print("데이터베이스 초기화 중...")
        # await init_db()
    yield

app = FastAPI(
    title="FastAPI App",
    description="FastAPI Application with JWT authentication",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(user.router, prefix=settings.API_V1_STR)
app.include_router(question.router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    

    return {
        "status": "healthy",
        "environment": settings.ENV
    }