from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


from ..config import settings

connect_args = {}
if settings.SQLALCHEMY_DATABASE_URL.startswith("mysql") or settings.SQLALCHEMY_DATABASE_URL.startswith("postgresql"):
    connect_args["connect_timeout"] = settings.DB_CONNECT_TIMEOUT
elif settings.SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args["timeout"] = settings.DB_CONNECT_TIMEOUT
    # Also disable thread check for sqlite in development
    connect_args["check_same_thread"] = False

engine_args = {
    "pool_recycle": settings.DB_POOL_RECYCLE,
    "pool_pre_ping": settings.DB_POOL_PRE_PING,
    "connect_args": connect_args
}

if not settings.SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_args["pool_size"] = settings.DB_POOL_SIZE
    engine_args["max_overflow"] = settings.DB_MAX_OVERFLOW

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    **engine_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_context():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()