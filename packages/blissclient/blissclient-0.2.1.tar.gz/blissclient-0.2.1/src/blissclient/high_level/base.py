import os
from ..openapi.api_config import APIConfig


class Base:
    def __init__(self):
        try:
            self._api_config = APIConfig(base_path=os.environ["BLISSTERM_URL"])
        except KeyError:
            raise RuntimeError("`BLISSTERM_URL` not defined in environemnt")
