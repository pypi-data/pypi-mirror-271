from .config import ConfigClient
import pkg_resources
import urllib3
import json

version = "unknown"

try:
   version = pkg_resources.require("bcra-api-client")[0].version
except:
    pass

class BaseClient:

    def __init__(self, config: ConfigClient) -> None:
        
        self.base_url = config.base_url
        
        self.headers = {
            "Accept-Encoding": "gzip",
            "User-Agent": f"paivae/BCRA BCRA_Python_Client/{version}",
        }

        self.client = urllib3.PoolManager(
            headers = self.headers
        )


    def _get(self,
             path: str,
             params : str
             ):
        
        response = self.client.request(
            "GET",
            self.BASE + path,
            fields = params,
            headers = self.headers
        )
        

        if response.status != 200 :
            raise "Error in Query"
        
        try:
            obj = self._decoded(response)
        except Exception as e:
            print(f"Error json response: {e.message}")
        

    def _decoded(self, response):
        return json.loads(response.data.decode("utf-8"))
    