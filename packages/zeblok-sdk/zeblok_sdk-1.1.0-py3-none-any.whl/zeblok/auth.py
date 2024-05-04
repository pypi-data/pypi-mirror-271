from .utils.validations import validate_app_url, validate_datalake_url, validate_datalake_username, \
    validate_datalake_secret_key, validate_api_access_key, validate_api_access_secret, validate_bucket
from .base.base_auth import Auth


class APIAuth(Auth):
    def __init__(self, app_url: str, api_access_key: str, api_access_secret: str):
        super().__init__(
            url=app_url, user_key=api_access_key, user_password=api_access_secret, allowed_url_schemes=['https']
        )

    @staticmethod
    def _validate_url(url):
        validate_app_url(url)

    @staticmethod
    def _validate_user_key(user_key):
        validate_api_access_key(api_access_key=user_key)

    @staticmethod
    def _validate_user_password(user_password):
        validate_api_access_secret(api_access_secret=user_password)

    def get_api_creds(self):
        return self.api_access_key, self.api_access_secret

    @property
    def app_url(self):
        return self._url

    @property
    def api_access_key(self):
        return self._user_key

    @property
    def api_access_secret(self):
        return self._user_password


class DatalakeAuth(Auth):
    __slots__ = ['bucket_name', '__bucket_exists']

    def __init__(self, datalake_url: str, datalake_username: str, datalake_secret_key: str, bucket_name: str):
        super().__init__(
            url=datalake_url, user_key=datalake_username, user_password=datalake_secret_key,
            allowed_url_schemes=['https']
        )
        self.__bucket_exists = False
        validate_bucket(
            datalake_url=self._url, access_key=self._user_key,
            secret_key=self._user_password, bucket_name=bucket_name
        )
        self.bucket_name = bucket_name
        self.__bucket_exists = True

    @staticmethod
    def _validate_url(url):
        validate_datalake_url(url)

    @staticmethod
    def _validate_user_key(user_key):
        validate_datalake_username(datalake_username=user_key)

    @staticmethod
    def _validate_user_password(user_password):
        validate_datalake_secret_key(datalake_secret_key=user_password)

    @property
    def datalake_url(self):
        return self._url

    @property
    def datalake_username(self):
        return self._user_key

    @property
    def datalake_secret_key(self):
        return self._user_password

    def bucket_exists(self):
        return self.__bucket_exists

