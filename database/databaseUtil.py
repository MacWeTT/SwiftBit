from .connection import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Annotated
from services.authentication import getCurrentUser


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(getCurrentUser)]
