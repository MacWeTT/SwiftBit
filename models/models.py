from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
import datetime
from ..database.connection import Base
import uuid


class BaseModel(Base):
    id = Column(uuid, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    class Meta:
        abstract = True


class User(BaseModel):
    __tablename__ = "users"

    is_active = Column(Boolean, default=True)

    username = Column(String, unique=True)
    password = Column(String)

    first_name = Column(String)
    last_name = Column(String)
    
    urls = relationship

    def __repr__(self):
        return f"<User {self.username}>"


class ShortenedURL(BaseModel):
    __tablename__ = "shortened_urls"

    url = Column(String, unique=True)
    short_url = Column(String, unique=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    

    def __repr__(self):
        return f"<ShortenedURL {self.url}>"
