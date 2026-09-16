from datetime import datetime

from sqlalchemy import UniqueConstraint, Index, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import  Column, Integer

class Base(DeclarativeBase):
    """所有 ORM 模型的基类"""
    pass

class TimestampMixin:
    """通用的时间戳混入类 (Mixin)，供需要自动生成创建/更新时间的表继承"""
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间"
    )