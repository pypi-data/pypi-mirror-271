import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from openg2p_fastapi_common.service import BaseService
from openg2p_g2pconnect_common_lib.schemas import RequestHeader
from openg2p_g2pconnect_mapper_lib.schemas import (
    LinkRequest,
    LinkRequestMessage,
    LinkResponse,
    LinkStatusReasonCode,
    ResolveRequest,
    ResolveRequestMessage,
    ResolveResponse,
    ResolveStatusReasonCode,
    SingleLinkRequest,
    SingleResolveRequest,
    SingleUnlinkRequest,
    SingleUpdateRequest,
    UnlinkRequest,
    UnlinkRequestMessage,
    UnlinkResponse,
    UnlinkStatusReasonCode,
    UpdateRequest,
    UpdateRequestMessage,
    UpdateResponse,
    UpdateStatusReasonCode,
)
from openg2p_spar_mapper_interface_lib.response import MapperResponse


class MapperConnectorHelper(BaseService):
    async def construct_link_request(
        self,
        id: str,
        fa: str,
        name: Optional[str],
        phone_number: Optional[str],
        additional_info: Optional[List[Dict[str, Any]]],
    ) -> LinkRequest:
        link_request_message = LinkRequestMessage(
            transaction_id=str(uuid.uuid4()),
            link_request=[
                SingleLinkRequest(
                    reference_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    id=id,
                    fa=fa,
                    name=name,
                    phone_number=phone_number,
                    additional_info=additional_info,
                )
            ],
        )

        link_request = LinkRequest(
            signature="",
            header=RequestHeader(
                message_id=str(uuid.uuid4()),
                message_ts=str(datetime.now()),
                action="link",
                sender_id="",
                sender_uri="",
                total_count=1,
            ),
            message=link_request_message,
        )

        return link_request

    async def construct_unlink_request(self, id: str) -> UnlinkRequest:
        unlink_request_message = UnlinkRequestMessage(
            transaction_id=str(uuid.uuid4()),
            unlink_request=[
                SingleUnlinkRequest(
                    reference_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    id=id,
                )
            ],
        )

        unlink_request = UnlinkRequest(
            signature="",
            header=RequestHeader(
                message_id=str(uuid.uuid4()),
                message_ts=str(datetime.now()),
                action="unlink",
                sender_id="",
                sender_uri="",
                total_count=1,
            ),
            message=unlink_request_message,
        )

        return unlink_request

    async def construct_resolve_request(self, id: str) -> ResolveRequest:
        resolve_request_message = ResolveRequestMessage(
            transaction_id=str(uuid.uuid4()),
            resolve_request=[
                SingleResolveRequest(
                    reference_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    id=id,
                    scope="details",
                )
            ],
        )

        resolve_request = ResolveRequest(
            signature="",
            header=RequestHeader(
                message_id=str(uuid.uuid4()),
                message_ts=str(datetime.now()),
                action="resolve",
                sender_id="",
                sender_uri="",
                total_count=1,
            ),
            message=resolve_request_message,
        )

        return resolve_request

    async def construct_update_request(
        self,
        id: str,
        fa: str,
        name: Optional[str],
        phone_number: Optional[str],
        additional_info: Optional[List[Dict[str, Any]]],
    ) -> UpdateRequest:
        update_request_message = UpdateRequestMessage(
            transaction_id=str(uuid.uuid4()),
            update_request=[
                SingleUpdateRequest(
                    reference_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    id=id,
                    fa=fa,
                    name=name,
                    phone_number=phone_number,
                    additional_info=additional_info,
                )
            ],
        )

        update_request = UpdateRequest(
            signature="",
            header=RequestHeader(
                message_id=str(uuid.uuid4()),
                message_ts=str(datetime.now()),
                action="update",
                sender_id="",
                sender_uri="",
                total_count=1,
            ),
            message=update_request_message,
        )

        return update_request

    async def construct_mapper_response_link(
        self, response: LinkResponse
    ) -> MapperResponse:
        mapper_response = MapperResponse(
            id="",
            fa=response.message.link_response[0].fa,
            name="",
            phone_number="",
            account_provider_info=None,
            additional_info=response.message.link_response[0].additional_info,
            status=response.message.link_response[0].status,
            mapper_error_code=(
                LinkStatusReasonCode(
                    response.message.link_response[0].status_reason_code
                )
                if response.message.link_response[0].status_reason_code
                else None
            ),
            mapper_error_message=response.message.link_response[
                0
            ].status_reason_message,
        )
        return mapper_response

    async def construct_mapper_response_unlink(
        self, response: UnlinkResponse
    ) -> MapperResponse:
        mapper_response = MapperResponse(
            id=response.message.unlink_response[0].id,
            fa="",
            name="",
            phone_number="",
            account_provider_info=None,
            additional_info=[],
            status=response.message.unlink_response[0].status,
            mapper_error_code=(
                UnlinkStatusReasonCode(
                    response.message.unlink_response[0].status_reason_code
                )
                if response.message.unlink_response[0].status_reason_code
                else None
            ),
            mapper_error_message=response.message.unlink_response[
                0
            ].status_reason_message,
        )
        return mapper_response

    async def construct_mapper_response_resolve(
        self, response: ResolveResponse
    ) -> MapperResponse:
        mapper_response = MapperResponse(
            id=response.message.resolve_response[0].id,
            fa=response.message.resolve_response[0].fa,
            name="",
            phone_number="",
            account_provider_info=response.message.resolve_response[
                0
            ].account_provider_info,
            additional_info=response.message.resolve_response[0].additional_info,
            status=response.message.resolve_response[0].status,
            mapper_error_code=(
                ResolveStatusReasonCode(
                    response.message.resolve_response[0].status_reason_code
                )
                if response.message.resolve_response[0].status_reason_code
                else None
            ),
            mapper_error_message=response.message.resolve_response[
                0
            ].status_reason_message,
        )
        return mapper_response

    async def construct_mapper_response_update(
        self, response: UpdateResponse
    ) -> MapperResponse:
        mapper_response = MapperResponse(
            id=response.message.update_response[0].id,
            fa="",
            name="",
            phone_number="",
            account_provider_info=None,
            additional_info=response.message.update_response[0].additional_info,
            status=response.message.update_response[0].status,
            mapper_error_code=(
                UpdateStatusReasonCode(
                    response.message.update_response[0].status_reason_code
                )
                if response.message.update_response[0].status_reason_code
                else None
            ),
            mapper_error_message=response.message.update_response[
                0
            ].status_reason_message,
        )
        return mapper_response
