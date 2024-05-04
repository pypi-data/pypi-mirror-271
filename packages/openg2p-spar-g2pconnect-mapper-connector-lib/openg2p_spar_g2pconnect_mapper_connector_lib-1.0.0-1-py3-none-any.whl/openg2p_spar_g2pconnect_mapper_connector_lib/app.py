from openg2p_fastapi_common.app import Initializer as BaseInitializer
from openg2p_g2pconnect_mapper_lib.app import Initializer as MapperInitializer

from .connector import MapperConnector
from .helper import MapperConnectorHelper


class Initializer(BaseInitializer):
    def initialize(self, **kwargs):
        MapperConnector()
        MapperConnectorHelper()
        MapperInitializer()
