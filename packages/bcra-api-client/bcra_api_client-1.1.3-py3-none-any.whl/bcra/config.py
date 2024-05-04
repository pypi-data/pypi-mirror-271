import os

ENV_KEY = "BCRA_API_KEY"


class ConfigClient:
    def __init__(self,
                 api_key: str = os.getenv(ENV_KEY),
                 connect_timeout: int = 400) -> None:
        self.base_url = None
        self.api_key = api_key
        self.connect_timeout = connect_timeout

    def set_base_url(self, base_url: str) -> None:
        self.base_url = base_url
