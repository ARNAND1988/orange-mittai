import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import Connector

from app.db.base import Base

# =====================================================
# DATABASE MODE SWITCH
# =====================================================
# local  -> SQLite file
# cloud  -> Cloud SQL Postgres (IAM auth)
# =====================================================

DATABASE_MODE = os.getenv("DATABASE_MODE", "local")

# =====================================================
# LOCAL DATABASE (SQLite)
# =====================================================
if DATABASE_MODE == "local":
    DATABASE_URL = os.getenv(
        "LOCAL_DATABASE_URL",
        "sqlite:///./local.db"
    )

    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
    )

# =====================================================
# CLOUD DATABASE (Cloud SQL Postgres + IAM)
# =====================================================
else:
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME")

    if not all([DB_NAME, DB_USER, INSTANCE_CONNECTION_NAME]):
        raise RuntimeError(
            "Missing Cloud SQL environment variables. "
            "Ensure DB_NAME, DB_USER, and INSTANCE_CONNECTION_NAME are set."
        )

    connector = Connector()

    def getconn():
        return connector.connect(
            INSTANCE_CONNECTION_NAME,
            "pg8000",
            user=DB_USER,
            db=DB_NAME,
            enable_iam_auth=True,
        )

    engine = create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        pool_size=5,
        max_overflow=2,
        pool_recycle=1800,
    )

# =====================================================
# SESSION
# =====================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# =====================================================
# DEPENDENCY
# =====================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
