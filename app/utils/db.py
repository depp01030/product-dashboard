# app/utils/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.utils.config import get_database_uri, load_env

# 載入 .env 環境變數
load_env()

# 取得資料庫連線字串
DATABASE_URL = get_database_uri()

# 建立資料庫引擎與 Session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 宣告 ORM 基礎類別，供 models 繼承
Base = declarative_base()


# === Dependency：建立 DB session ===
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
