from sqlalchemy import Column, String

from .database import Base


class User(Base):
    __tablename__ = "User"

    email = Column(String, primary_key=True, nullable=False, unique=True)
    github_access_token = Column(String, primary_key=True, nullable=False, unique=True)
    github_refresh_token = Column(String, primary_key=True, nullable=False, unique=True)
