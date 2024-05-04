from bcra.base import BaseClient
from bcra.statistics import PATH_ROOT

class Variables(BaseClient):
    
    def __init__(self) -> None:
        self.path = PATH_ROOT + "principalesvariables"


    def get(self,
            idVariable: int = None,
            from_: str = None,
            to: str = None):
        
        path_params = ""

        if(idVariable != None and from_ != None and to != None):
            path_params = f"{self.path}/{idVariable}/{from_}/{to}"

        return self._get(path=self.path, params=path_params)