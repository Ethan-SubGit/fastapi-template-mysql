from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import user
from app.core.database import Base, engine

def create_app() -> FastAPI:
    # 환경별 설정
    app = FastAPI(
        title="FastAPI App",
        description="FastAPI Application with environment configurations",
        version="1.0.0",
        debug=settings.DEBUG
    )

    # 데이터베이스 테이블 생성 (개발 환경에서만)
    if settings.ENV != "production":
        Base.metadata.create_all(bind=engine)

    # API 라우터 등록
    app.include_router(user.router, prefix=settings.API_V1_STR)

    return app

app = create_app()

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENV
    }