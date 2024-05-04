from statistics import Stadistics
import os

BASE = "https://api.bcra.gob.ar/"
ENV_KEY = "BCRA_API_KEY"

class Client (
    Stadistics
): 
    def __init__(self,
                 api_key: str = os.getenv(ENV_KEY)
                 ) -> None:
        super().__init__()
        