from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import logging

# 더 자세한 로깅 설정
logging.basicConfig()
logger = logging.getLogger('sqlalchemy.engine')
logger.setLevel(logging.INFO)

# 파일로도 로그 저장하기 원한다면
handler = logging.FileHandler('sql.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def test_database_connection():
    try:
        
        test_engine = create_engine(settings.DATABASE_URL)
        with test_engine.connect() as connection:
            logging.info(f"Successfully connected to database in {settings.ENV} environment")
    except Exception as e:
        logging.error(f"Database connection failed: {str(e)}")
        raise

# 데이터베이스 연결 테스트
test_database_connection()

# 기존 엔진 설정
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 