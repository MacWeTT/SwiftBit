from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import DateTime, Column
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./database/db.sqlite3"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class CustomBaseModel:
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


Base = declarative_base(cls=CustomBaseModel)

Base.metadata.create_all(bind=engine)
