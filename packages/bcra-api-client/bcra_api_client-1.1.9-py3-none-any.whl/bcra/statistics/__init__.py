from bcra.config import ConfigClient
from .variables import Variables

PATH_ROOT = "estadisticas/v1/"


class Statistics:
    def __init__(self, config: ConfigClient) -> None:
        self.variables = Variables(config, PATH_ROOT)
