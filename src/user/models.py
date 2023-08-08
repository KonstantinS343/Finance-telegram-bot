from sqlalchemy import String, TIMESTAMP, Column, Float
from sqlalchemy.orm import DeclarativeBase

from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    username = Column(String, nullable=False, unique=True, primary_key=True)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    balance = Column(Float, default=0.0)
    email = Column(String, nullable=True, unique=True)
