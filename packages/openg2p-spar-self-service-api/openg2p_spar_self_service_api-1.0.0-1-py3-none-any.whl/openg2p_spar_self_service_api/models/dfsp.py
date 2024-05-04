from typing import Optional

from openg2p_fastapi_common.context import dbengine
from openg2p_fastapi_common.models import BaseORMModelWithTimes
from sqlalchemy import ForeignKey, Integer, String, select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..schemas import InputTypeEnum, LevelTypeEnum
from .strategy import Strategy


class DfspLevel(BaseORMModelWithTimes):
    __tablename__ = "dfsp_levels"

    name: Mapped[str] = mapped_column(String)
    level_type: Mapped[str] = mapped_column(String(35), default=LevelTypeEnum)
    input_type: Mapped[Optional[str]] = mapped_column(String, default=InputTypeEnum)
    parent: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    validation_regex: Mapped[Optional[str]] = mapped_column(String, nullable=True)

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

    name: Mapped[str] = mapped_column(String)
    code: Mapped[str] = mapped_column(String(20))
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    parent: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    level_id: Mapped[int] = mapped_column(Integer, nullable=True)
    strategy_id: Mapped[Optional[int]] = mapped_column(
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
