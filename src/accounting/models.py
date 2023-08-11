from sqlalchemy import String, TIMESTAMP, Column, ForeignKey, Float, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship

import uuid
import enum
from datetime import datetime

from src.user.models import User


class Base(DeclarativeBase):
    pass


class OperationType(enum.Enum):
    income = 'Income'
    expenditure = 'Expenditure'


class Accounting(Base):
    __tablename__ = 'accounting'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, ForeignKey(User.username))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    user = relationship(User, back_populates='accounting')
    quantity = Column(Float, nullable=False)
    categories = Column(String, ForeignKey('categories.name'))
    operation_type = Column(Enum(OperationType), nullable=False)


User.accounting = relationship(Accounting, back_populates='user')


class Categories(Base):
    __tablename__ = 'categories'

    name = Column(String, nullable=False, unique=True, primary_key=True)
    user_id = Column(String, ForeignKey(User.username))
    is_active = Column(Boolean, default=True, nullable=False)
