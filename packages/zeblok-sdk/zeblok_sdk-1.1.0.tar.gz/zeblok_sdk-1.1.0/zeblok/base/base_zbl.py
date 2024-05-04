from abc import ABC, abstractmethod
from typing import List

from ..auth import APIAuth


class ZBLBase(ABC):
    def __init__(self, api_auth: APIAuth):
        self._api_auth = api_auth

    @abstractmethod
    def get_all(self, *args, **kwargs) -> List[dict]:
        pass


