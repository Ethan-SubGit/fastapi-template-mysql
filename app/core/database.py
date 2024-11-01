from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.core.config import settings
import logging

# SQL 로깅 설정
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# MySQL URL을 비동기 URL로 변경
ASYNC_DATABASE_URL = settings.DATABASE_URL.replace(
    'mysql+pymysql', 'mysql+aiomysql'
)

engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300
)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all) 