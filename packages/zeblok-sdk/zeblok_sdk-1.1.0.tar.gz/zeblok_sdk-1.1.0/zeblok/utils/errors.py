import sys
from typing import Union, Dict
import json


# sys.tracebacklimit = 0


class InvalidCredentialsError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidURL(Exception):
    def __init__(self, message):
        super().__init__(message)


class AuthenticationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class AuthorizationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class NoResourcesError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ResourceNotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ServerError(Exception):
    def __init__(self, message):
        super().__init__(message)


class DirectoryNotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidBucketName(Exception):
    def __init__(self, message):
        super().__init__(message)


class BucketDoesNotExistsError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ObjectDoesNotExistsError(Exception):
    def __init__(self, message):
        super().__init__(message)


class FileUploadError(Exception):
    def __init__(self, message):
        super().__init__(message)


class FileDownloadError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ModelDeploymentError(Exception):
    def __init__(self, message):
        super().__init__(message)


class PipelineCreationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class AIAPICreationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class AIAPISpawnError(Exception):
    def __init__(self, message):
        super().__init__(message)


class CaaSUploadError(Exception):
    def __init__(self, message):
        super().__init__(message)


def api_error(status_code: int, message: str = ""):
    if status_code == 200:
        raise NoResourcesError(message if message else "No respective resources in this environment.")

    if status_code == 401:
        raise AuthenticationError(
            "User not authenticated. Please check your token or api_access_key or api_access_secret"
        )

    if status_code == 403:
        print(message)
        raise AuthorizationError(
            "User not authorized. Please check if you have the appropriate permissions to access/spawn the respective resource."
        )

    if status_code == 404:
        raise ResourceNotFoundError(
            message if message else "The resource you requested was not found."
        )

    raise ServerError(f"\nStatus code = {status_code} | {message}")
