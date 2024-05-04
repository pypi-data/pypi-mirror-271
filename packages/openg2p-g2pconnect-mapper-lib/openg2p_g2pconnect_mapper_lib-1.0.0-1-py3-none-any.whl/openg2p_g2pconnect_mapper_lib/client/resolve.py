import logging

import httpx
from openg2p_fastapi_common.errors.base_exception import BaseAppException
from openg2p_fastapi_common.service import BaseService

from ..schemas import ResolveRequest, ResolveResponse

_logger = logging.getLogger("mapper_client_resolve")


class MapperResolveClient(BaseService):
    async def resolve_request(
        self, resolve_request: ResolveRequest, resolve_url: str = None, timeout=60
    ) -> ResolveResponse:
        try:
            client = httpx.AsyncClient()
            res = await client.post(
                resolve_url,
                content=resolve_request.model_dump_json(),
                headers={"content-type": "application/json"},
                timeout=timeout,
            )
            await client.aclose()
            res.raise_for_status()
            resolve_response: ResolveResponse = ResolveResponse.model_validate(
                res.json()
            )
            return resolve_response
        except httpx.HTTPStatusError as e:
            _logger.error(
                f"Error in resolve request: {e.response.status_code} {e.response.text}"
            )
            raise BaseAppException(
                message="Error in resolve request",
                code=str(e.response.status_code),
            ) from e
