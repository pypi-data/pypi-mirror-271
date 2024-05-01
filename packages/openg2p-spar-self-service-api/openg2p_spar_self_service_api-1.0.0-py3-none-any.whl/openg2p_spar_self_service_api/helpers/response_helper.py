from openg2p_fastapi_common.service import BaseService
from openg2p_spar_mapper_interface_lib.response import MapperResponse

from ..schemas import (
    ResponseStatus,
    SelfServiceLinkResponse,
    SelfServiceLinkResponsePayload,
    SelfServiceResolveResponse,
    SelfServiceResolveResponsePayload,
    SelfServiceUnlinkResponse,
    SelfServiceUnlinkResponsePayload,
    SelfServiceUpdateResponse,
    SelfServiceUpdateResponsePayload,
)
from .strategy_helper import StrategyHelper


class ResponseHelper(BaseService):
    async def construct_link_response(
        self, mapper_response: MapperResponse
    ) -> SelfServiceLinkResponse:
        return SelfServiceLinkResponse(
            response_status=(
                ResponseStatus.SUCCESS
                if mapper_response.status == "succ"
                else ResponseStatus.FAILURE
            ),
            response_error_code=(
                mapper_response.mapper_error_code
                if mapper_response.mapper_error_code
                else None
            ),
            response_payload=SelfServiceLinkResponsePayload(),
            response_message=(
                mapper_response.mapper_error_message
                if mapper_response.mapper_error_message
                else None
            ),
        )

    async def construct_update_response(
        self, mapper_response: MapperResponse
    ) -> SelfServiceUpdateResponse:
        return SelfServiceUpdateResponse(
            response_status=(
                ResponseStatus.SUCCESS
                if mapper_response.status == "succ"
                else ResponseStatus.FAILURE
            ),
            response_payload=SelfServiceUpdateResponsePayload(),
            response_message=(
                mapper_response.mapper_error_message
                if mapper_response.mapper_error_message
                else None
            ),
        )

    async def construct_resolve_response(
        self, mapper_response: MapperResponse
    ) -> SelfServiceResolveResponse:
        return SelfServiceResolveResponse(
            response_status=(
                ResponseStatus.SUCCESS
                if mapper_response.status == "succ"
                else ResponseStatus.FAILURE
            ),
            response_error_code=(
                mapper_response.mapper_error_code
                if mapper_response.mapper_error_code
                else None
            ),
            response_payload=SelfServiceResolveResponsePayload(
                fa=(
                    await StrategyHelper()
                    .get_component()
                    .deconstruct_fa(mapper_response.fa, mapper_response.additional_info)
                    if mapper_response.fa
                    else None
                ),
                name=mapper_response.name,
                phone_number=mapper_response.phone_number,
                additional_info=mapper_response.additional_info,
            ),
            response_message=(
                mapper_response.mapper_error_message
                if mapper_response.mapper_error_message
                else None
            ),
        )

    async def construct_unlink_response(
        self, mapper_response: MapperResponse
    ) -> SelfServiceUnlinkResponse:
        return SelfServiceUnlinkResponse(
            response_status=(
                ResponseStatus.SUCCESS
                if mapper_response.status == "succ"
                else ResponseStatus.FAILURE
            ),
            response_error_code=(
                mapper_response.mapper_error_code
                if mapper_response.mapper_error_code
                else None
            ),
            response_payload=SelfServiceUnlinkResponsePayload(),
            response_message=(
                mapper_response.mapper_error_message
                if mapper_response.mapper_error_message
                else None
            ),
        )
