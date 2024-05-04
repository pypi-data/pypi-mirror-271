from .config import ConfigClient
from .statistics import Statistics

BASE = "https://api.bcra.gob.ar/"


class Client:
    def __init__(self, config: ConfigClient = None) -> None:
        if config is None:
            config = ConfigClient()

        self.statistics = Statistics(config)
