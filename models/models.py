from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String, unique=True)
    password = Column(String)


# urls = relationship("ShortenedUrl", back_populates="created_by")

# def __repr__(self):
#     return f"<User {self.username}>"


# class ShortenedUrl(Base):
#     __tablename__ = "shortened_url"

#     url = Column(String, unique=True)
#     short_url = Column(String, unique=True)

#     user_id = Column(Integer, ForeignKey("user.id"))

#     created_by = relationship("User", back_populates="urls")

#     def __repr__(self):
#         return f"<ShortenedURL {self.url}>"
