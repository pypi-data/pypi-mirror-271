from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from .request import SparRequest
from .response import SparResponse


class LevelTypeEnum(Enum):
    BANK = "bank"
    BRANCH = "branch"
    ACCOUNT = "account"
    MOBILE_WALLET_PROVIDER = "mobile_wallet_provider"
    MOBILE_NUMBER = "mobile_number"
    EMAIL_WALLET_PROVIDER = "email_wallet_provider"
    EMAIL_ADDRESS = "email_address"


class InputTypeEnum(Enum):
    INPUT = "input"
    SELECT = "select"


class DfspLevelSchema(BaseModel):
    id: int
    name: str
    level_type: LevelTypeEnum
    input_type: InputTypeEnum = None
    parent: Optional[int] = None
    validation_regex: Optional[str] = None


class DfspLevelRequestPayload(BaseModel):
    parent: Optional[int]


class DfspLevelRequest(SparRequest):
    request_payload: DfspLevelRequestPayload


class DfspLevelResponse(SparResponse):
    response_payload: List[DfspLevelSchema]


class DfspLevelValueSchema(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str]
    parent: Optional[int]
    level_id: int
    strategy_id: Optional[int]


class DfspLevelValueRequestPayload(BaseModel):
    level_id: Optional[int]
    parent: Optional[int]


class DfspLevelValueRequest(SparRequest):
    request_payload: DfspLevelValueRequestPayload


class DfspLevelValueResponse(SparResponse):
    response_payload: List[DfspLevelValueSchema]
