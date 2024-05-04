from typing import Optional

from openg2p_fastapi_auth.models.orm.login_provider import (
    LoginProvider as OriginalLoginProvider,
)
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .strategy import Strategy


class LoginProvider(OriginalLoginProvider):
    strategy_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("strategy.id"), nullable=True
    )
    strategy: Mapped[Optional[Strategy]] = relationship("Strategy")
