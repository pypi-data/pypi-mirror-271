import logging

import httpx
from openg2p_fastapi_common.errors.base_exception import BaseAppException
from openg2p_fastapi_common.service import BaseService

from ..schemas import UnlinkRequest, UnlinkResponse

_logger = logging.getLogger("mapper_client_unlink")


class MapperUnlinkClient(BaseService):
    async def unlink_request(
        self, unlink_request: UnlinkRequest, unlink_url: str = None, timeout=60
    ) -> UnlinkResponse:
        try:
            client = httpx.AsyncClient()
            res = await client.post(
                unlink_url,
                content=unlink_request.model_dump_json(),
                headers={"content-type": "application/json"},
                timeout=timeout,
            )
            await client.aclose()
            res.raise_for_status()
            unlink_response: UnlinkResponse = UnlinkResponse.model_validate(res.json())
            return unlink_response
        except httpx.HTTPStatusError as e:
            _logger.error(
                f"Error in unlink request: {e.response.status_code} {e.response.text}"
            )
            raise BaseAppException(
                message="Error in unlink request",
                code=e.response.status_code,
                detail=e.response.text,
            ) from e
