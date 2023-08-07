from sqlalchemy import String, TIMESTAMP, Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship

import uuid
from datetime import datetime

from src.user.models import User


class Base(DeclarativeBase):
    pass


class Accounting(Base):
    __tablename__ = 'accounting'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, ForeignKey(User.username))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    user = relationship(User, back_populates='accounting')
    quantity = Column(Integer, nullable=False)
    categories = Column(UUID, ForeignKey('categories.id'))


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
