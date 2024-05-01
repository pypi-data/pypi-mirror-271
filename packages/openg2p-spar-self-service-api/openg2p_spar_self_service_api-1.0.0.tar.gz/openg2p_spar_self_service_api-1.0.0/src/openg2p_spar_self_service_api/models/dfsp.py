from typing import Optional

from openg2p_fastapi_common.context import dbengine
from openg2p_fastapi_common.models import BaseORMModelWithTimes
from sqlalchemy import Column, ForeignKey, Integer, String, select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import Mapped, relationship

from ..schemas import InputTypeEnum, LevelTypeEnum
from .strategy import Strategy


class DfspLevel(BaseORMModelWithTimes):
    __tablename__ = "dfsp_levels"

    name: Mapped[str] = Column(String)
    level_type: Mapped[str] = Column(String(35), default=LevelTypeEnum)
    input_type: Mapped[Optional[str]] = Column(String, default=InputTypeEnum)
    parent: Mapped[Optional[int]] = Column(Integer, nullable=True)
    validation_regex: Mapped[Optional[str]] = Column(String, nullable=True)

    class Config:
        orm_mode = True

    @classmethod
    async def get_level(cls, **kwargs):
        response = []
        async_session_maker = async_sessionmaker(dbengine.get())
        async with async_session_maker() as session:
            stmt = select(cls)
            for key, value in kwargs.items():
                if value is not None:
                    stmt = stmt.where(getattr(cls, key) == value)

            stmt = stmt.order_by(cls.id.asc())

            result = await session.execute(stmt)

            response = list(result.scalars())
        return response


class DfspLevelValue(BaseORMModelWithTimes):
    __tablename__ = "dfsp_level_values"

    name: Mapped[str] = Column(String)
    code: Mapped[str] = Column(String(20))
    description: Mapped[Optional[str]] = Column(String, nullable=True)
    parent: Mapped[Optional[int]] = Column(Integer, nullable=True)
    level_id: Mapped[int] = Column(Integer, nullable=True)
    strategy_id: Mapped[Optional[int]] = Column(
        Integer, ForeignKey("strategy.id"), nullable=True
    )

    strategy: Mapped[Optional[Strategy]] = relationship("Strategy")

    class Config:
        orm_mode = True

    @classmethod
    async def get_level_values(cls, **kwargs):
        response = []
        async_session_maker = async_sessionmaker(dbengine.get())
        async with async_session_maker() as session:
            stmt = select(cls)
            for key, value in kwargs.items():
                if value is not None:
                    stmt = stmt.where(getattr(cls, key) == value)

            stmt = stmt.order_by(cls.id.asc())

            result = await session.execute(stmt)

            response = list(result.scalars())
        return response
