from openg2p_fastapi_common.app import Initializer as BaseInitializer

from .client import (
    MapperLinkClient,
    MapperResolveClient,
    MapperUnlinkClient,
    MapperUpdateClient,
)


class Initializer(BaseInitializer):
    def initialize(self, **kwargs):
        MapperLinkClient()
        MapperUpdateClient()
        MapperUnlinkClient()
        MapperResolveClient()
