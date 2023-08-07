from sqlalchemy import String, TIMESTAMP, Column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase

from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    username = Column(String, nullable=False, unique=True, primary_key=True)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    accounting = relationship('Accounting', back_populates='user')
