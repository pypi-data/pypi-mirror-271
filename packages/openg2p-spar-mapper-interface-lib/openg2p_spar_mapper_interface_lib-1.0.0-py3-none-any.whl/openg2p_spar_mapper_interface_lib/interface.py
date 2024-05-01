from typing import Any, Dict, List, Optional

from openg2p_fastapi_common.service import BaseService

from .response import MapperResponse


class MapperInterface(BaseService):
    async def link(
        self,
        id: str,
        fa: str,
        name: Optional[str],
        phone_number: Optional[str],
        additional_info: Optional[List[Dict[str, Any]]],
        link_url: str,
    ) -> MapperResponse:
        raise NotImplementedError()

    async def unlink(self, id: str, unlink_url: str) -> MapperResponse:
        raise NotImplementedError()

    async def resolve(self, id: str, resolve_url: str) -> MapperResponse:
        raise NotImplementedError()

    async def update(
        self,
        id: str,
        fa: str,
        name: Optional[str],
        phone_number: Optional[str],
        additional_info: Optional[List[Dict[str, Any]]],
        update_url: str,
    ) -> MapperResponse:
        raise NotImplementedError()
