from bcra.base import BaseClient
from bcra.config import ConfigClient
from bcra.exceptions import PathIncomplete


class Variables(BaseClient):

    def __init__(self, config: ConfigClient, path_base: str) -> None:
        self.path = path_base
        super().__init__(config)

    def get(self):
        path = self.path + "principalesvariables"

        response = self._get(path=path)
        return response['results']

    def filter(self,
               id_variable: int = None,
               from_: str = None,
               to: str = None):

        if id_variable is None:
            raise PathIncomplete(
                f"id_variable no puede estar vacio"
            )

        if from_ is None or len(from_) == 0:
            raise PathIncomplete(
                f"fecha desde no puede estar vacio"
            )

        if to is None or len(from_) == 0 :
            raise PathIncomplete(
                f"fecha hasta no puede estar vacio"
            )

        # TODO - Validacion de formato fechas

        self.path = f"{self.path}datosvariable/{id_variable}/{from_}/{to}"
        print(self.path)

        response = self._get(path=self.path)
        return response['results']
