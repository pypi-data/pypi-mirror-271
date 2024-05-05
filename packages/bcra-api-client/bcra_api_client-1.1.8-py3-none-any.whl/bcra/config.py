import os

BASE = "https://api.bcra.gob.ar/"
ENV_KEY = "BCRA_API_KEY"


class ConfigClient:
    def __init__(self,
                 api_key: str = os.getenv(ENV_KEY),
                 connect_timeout: int = 400) -> None:
        self.base_url = BASE
        self.api_key = api_key
        self.connect_timeout = connect_timeout
