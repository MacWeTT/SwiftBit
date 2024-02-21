from services.authentication import getCurrentUser, getOptionalCurrentUser
from .connection import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(getCurrentUser)]
optional_user = Annotated[dict, Depends(getOptionalCurrentUser)]
