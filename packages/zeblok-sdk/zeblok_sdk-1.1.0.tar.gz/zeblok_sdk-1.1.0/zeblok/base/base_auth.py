from abc import ABC, abstractmethod
from typing import List


class Auth(ABC):
    __slots__ = ['_url', '_user_key', '_user_password', '_allowed_url_schemes']

    def __init__(self, user_key: str, user_password: str, url: str, allowed_url_schemes: List[str] = ['https']):
        # TODO: Fix url validation. Facing issue with urlparse
        # cls._validate_url(url=url)
        self._validate_user_key(user_key=user_key)
        self._validate_user_password(user_password=user_password)

        self._url = url.strip()  # if is_scheme_present(url=url) else allowed_url_schemes[0] + "://" + url
        self._user_key = user_key.strip()
        self._user_password = user_password.strip()
        self._allowed_url_schemes = allowed_url_schemes.sort()

    @staticmethod
    @abstractmethod
    def _validate_user_key(user_key):
        pass

    @staticmethod
    @abstractmethod
    def _validate_user_password(user_password):
        pass

    @staticmethod
    @abstractmethod
    def _validate_url(url):
        pass
