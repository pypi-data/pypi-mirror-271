from enum import Enum

from openg2p_fastapi_common.context import dbengine
from openg2p_fastapi_common.models import BaseORMModelWithTimes
from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import Mapped, mapped_column, relationship


class StrategyType(Enum):
    ID = "ID"
    FA = "FA"


class Strategy(BaseORMModelWithTimes):
    __tablename__ = "strategy"

    description: Mapped[str] = mapped_column(String)
    strategy_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=StrategyType,
    )
    deconstruct_strategy: Mapped[str] = mapped_column(String)
    construct_strategy: Mapped[str] = mapped_column(String)

    level_values = relationship("DfspLevelValue", back_populates="strategy")

    @classmethod
    async def get_strategy(cls, **kwargs):
        response = None
        async_session_maker = async_sessionmaker(dbengine.get())
        async with async_session_maker() as session:
            stmt = select(cls)
            for key, value in kwargs.items():
                if value is not None:
                    stmt = stmt.where(getattr(cls, key) == value)

            result = await session.execute(stmt)

            response = result.scalars().first()
        return response
