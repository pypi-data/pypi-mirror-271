from typing import Annotated

from fastapi import Depends
from openg2p_fastapi_auth.dependencies import JwtBearerAuth
from openg2p_fastapi_auth.models.credentials import AuthCredentials
from openg2p_fastapi_common.controller import BaseController
from openg2p_spar_mapper_interface_lib.interface import MapperInterface
from openg2p_spar_mapper_interface_lib.response import MapperResponse

from ..config import Settings
from ..helpers import ResponseHelper, StrategyHelper
from ..schemas import (
    STRATEGY_ID_KEY,
    SelfServiceLinkRequest,
    SelfServiceLinkResponse,
    SelfServiceResolveResponse,
    SelfServiceUnlinkResponse,
    SelfServiceUpdateRequest,
    SelfServiceUpdateResponse,
    TestStrategyResponse,
)

_config = Settings.get_config()


class SelfServiceController(BaseController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._mapper_interface = MapperInterface().get_component()
        self._link_url = _config.mapper_api_url + _config.mapper_link_path
        self._update_url = _config.mapper_api_url + _config.mapper_update_path
        self._resolve_url = _config.mapper_api_url + _config.mapper_resolve_path
        self._unlink_url = _config.mapper_api_url + _config.mapper_unlink_path

        self.router.prefix += ""
        self.router.tags += ["selfservice"]

        self.router.add_api_route(
            "/test_strategy",
            self.test_strategy,
            responses={200: {"model": TestStrategyResponse}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/link",
            self.link,
            responses={200: {"model": SelfServiceLinkResponse}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/update",
            self.update,
            responses={200: {"model": SelfServiceUpdateResponse}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/resolve",
            self.resolve,
            responses={200: {"model": SelfServiceResolveResponse}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/unlink",
            self.unlink,
            responses={200: {"model": SelfServiceUnlinkResponse}},
            methods=["POST"],
        )

    @property
    def id_mapper_interface(self):
        if not self._mapper_interface:
            self._mapper_interface = MapperInterface.get_component()
        return self._mapper_interface

    async def test_strategy(
        self,
        auth: Annotated[AuthCredentials, Depends(JwtBearerAuth())],
        self_service_link_request: SelfServiceLinkRequest,
    ) -> TestStrategyResponse:
        constructed_id = await StrategyHelper().get_component().construct_id(auth)
        constructed_fa = (
            await StrategyHelper()
            .get_component()
            .construct_fa(self_service_link_request.request_payload.fa)
        )

        return TestStrategyResponse(
            constructed_id=constructed_id, constructed_fa=constructed_fa
        )

    async def link(
        self,
        auth: Annotated[AuthCredentials, Depends(JwtBearerAuth())],
        self_service_link_request: SelfServiceLinkRequest,
    ) -> SelfServiceLinkResponse:
        constructed_id = await StrategyHelper().get_component().construct_id(auth)
        constructed_fa = (
            await StrategyHelper()
            .get_component()
            .construct_fa(self_service_link_request.request_payload.fa)
        )

        mapper_response: MapperResponse = await self.id_mapper_interface.link(
            id=constructed_id,
            fa=constructed_fa,
            name=self_service_link_request.request_payload.name,
            phone_number=self_service_link_request.request_payload.phone_number,
            additional_info=[
                {
                    STRATEGY_ID_KEY: self_service_link_request.request_payload.fa.strategy_id
                }
            ],
            link_url=self._link_url,
        )
        self_service_link_response: SelfServiceLinkResponse = (
            await ResponseHelper()
            .get_component()
            .construct_link_response(mapper_response)
        )

        return self_service_link_response

    async def update(
        self,
        auth: Annotated[AuthCredentials, Depends(JwtBearerAuth())],
        self_service_update_request: SelfServiceUpdateRequest,
    ) -> SelfServiceUpdateResponse:
        constructed_id = await StrategyHelper().get_component().construct_id(auth)
        constructed_fa = (
            await StrategyHelper()
            .get_component()
            .construct_fa(self_service_update_request.request_payload.fa)
        )
        mapper_response: MapperResponse = await self.id_mapper_interface.update(
            id=constructed_id,
            fa=constructed_fa,
            name=self_service_update_request.request_payload.name,
            phone_number=self_service_update_request.request_payload.phone_number,
            additional_info=[
                {
                    STRATEGY_ID_KEY: self_service_update_request.request_payload.fa.strategy_id
                }
            ],
            update_url=self._update_url,
        )
        self_service_update_response: SelfServiceUpdateResponse = (
            await ResponseHelper()
            .get_component()
            .construct_update_response(mapper_response)
        )

        return self_service_update_response

    async def resolve(
        self,
        auth: Annotated[AuthCredentials, Depends(JwtBearerAuth())],
    ) -> SelfServiceResolveResponse:
        constructed_id = await StrategyHelper().get_component().construct_id(auth)
        mapper_response: MapperResponse = await self.id_mapper_interface.resolve(
            id=constructed_id,
            resolve_url=self._resolve_url,
        )
        self_service_resolve_response: SelfServiceResolveResponse = (
            await ResponseHelper()
            .get_component()
            .construct_resolve_response(mapper_response)
        )

        return self_service_resolve_response

    async def unlink(
        self,
        auth: Annotated[AuthCredentials, Depends(JwtBearerAuth())],
    ) -> SelfServiceUnlinkResponse:
        constructed_id = await StrategyHelper().get_component().construct_id(auth)

        mapper_response: MapperResponse = await self.id_mapper_interface.unlink(
            id=constructed_id,
            unlink_url=self._unlink_url,
        )
        self_service_unlink_response: SelfServiceUnlinkResponse = (
            await ResponseHelper()
            .get_component()
            .construct_unlink_response(mapper_response)
        )

        return self_service_unlink_response
