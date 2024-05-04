import logging

import httpx
from openg2p_fastapi_common.errors.base_exception import BaseAppException
from openg2p_fastapi_common.service import BaseService

from ..schemas import UpdateRequest, UpdateResponse

_logger = logging.getLogger("mapper_client_update")


class MapperUpdateClient(BaseService):
    async def update_request(
        self, update_request: UpdateRequest, update_url: str = None, timeout=60
    ) -> UpdateResponse:
        try:
            client = httpx.AsyncClient()
            res = await client.post(
                update_url,
                content=update_request.model_dump_json(),
                headers={"content-type": "application/json"},
                timeout=timeout,
            )
            await client.aclose()
            res.raise_for_status()
            update_response: UpdateResponse = UpdateResponse.model_validate(res.json())
            return update_response
        except httpx.HTTPStatusError as e:
            _logger.error(
                f"Error in update request: {e.response.status_code} {e.response.text}"
            )
            raise BaseAppException(
                message="Error in update request",
                code=str(e.response.status_code),
            ) from e
