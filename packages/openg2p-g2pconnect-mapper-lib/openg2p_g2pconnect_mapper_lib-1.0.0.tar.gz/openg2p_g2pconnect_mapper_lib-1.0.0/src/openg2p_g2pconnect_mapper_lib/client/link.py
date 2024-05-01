import logging

import httpx
from openg2p_fastapi_common.errors.base_exception import BaseAppException
from openg2p_fastapi_common.service import BaseService

from ..schemas import LinkRequest, LinkResponse

_logger = logging.getLogger("mapper_client_link")


class MapperLinkClient(BaseService):
    async def link_request(
        self, link_request: LinkRequest, link_url: str = None, timeout=60
    ) -> LinkResponse:
        try:
            client = httpx.AsyncClient()
            res = await client.post(
                link_url,
                content=link_request.model_dump_json(),
                headers={"content-type": "application/json"},
                timeout=timeout,
            )
            await client.aclose()
            res.raise_for_status()
            link_response: LinkResponse = LinkResponse.model_validate(res.json())
            return link_response
        except httpx.HTTPStatusError as e:
            _logger.error(
                f"Error in link request: {e.response.status_code} {e.response.text}"
            )
            raise BaseAppException(
                message="Error in link request",
                code=e.response.status_code,
                detail=e.response.text,
            ) from e
