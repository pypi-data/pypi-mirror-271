import os
from pathlib import Path
from typing import List, Dict

from minio import Minio

from .error_message import MODEL_FOLDER_PATH_DOES_NOT_EXIST, INVALID_AI_API_NAME_TYPE, EMPTY_AI_API_NAME, \
    INVALID_AI_API_TYPE_TYPE, EMPTY_AI_API_TYPE, INVALID_AI_API_TYPE, EMPTY_MODEL_FOLDER_PATH, \
    MODEL_FOLDER_PATH_NOT_DIR, MODEL_FOLDER_PARENT_PATH_NO_WRITE_PERMISSION, INVALID_API_ACCESS_KEY_TYPE, \
    EMPTY_API_ACCESS_KEY, INVALID_API_ACCESS_SECRET_TYPE, EMPTY_API_ACCESS_SECRET, INVALID_DATALAKE_USERNAME_TYPE, \
    EMPTY_DATALAKE_USERNAME, INVALID_DATALAKE_SECRET_KEY_TYPE, EMPTY_DATALAKE_SECRET_KEY, INVALID_BUCKET_NAME_TYPE, \
    EMPTY_BUCKET_NAME, EMPTY_AI_PIPELINE_NAME, INVALID_AI_PIPELINE_NAME_TYPE
from .errors import InvalidCredentialsError, DirectoryNotFoundError, BucketDoesNotExistsError, InvalidBucketName

URL_PATTERN_WITHOUT_SCHEME = "^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"


def __is_list_of_dicts(variable):
    return isinstance(variable, list) and all(isinstance(item, dict) for item in variable)


def is_scheme_present(url: str) -> bool:
    from urllib.parse import urlparse
    return True if urlparse(url).scheme != '' else False


def is_scheme_valid(url: str, allowed_schemes: List[str] = ['https']) -> bool:
    from urllib.parse import urlparse
    return True if urlparse(url).scheme in allowed_schemes else False


def __base_validate_url(url_name: str, url: str, allowed_schemes: List[str] = ['https']):
    """
    Base URL validator function

    :param url_name:
    :param url:
    :param allowed_schemes:
    :return:
    """
    from re import match
    from urllib.parse import urlparse
    from .errors import InvalidURL

    # TODO: urlparse not working as expected. Use some other library for url parsing
    if type(url) is not str:
        raise TypeError(f'{url_name} can only be of type String.')

    if url == '':
        raise InvalidURL(f'{url_name} cannot empty.')

    parsed_url = urlparse(url=url if is_scheme_present(url) else allowed_schemes[0] + "://" + url)

    if is_scheme_valid(url, allowed_schemes):
        raise InvalidURL(f'Given url scheme: {parsed_url.scheme} not allowed. Allowed url schemes: {allowed_schemes}')

    if match(URL_PATTERN_WITHOUT_SCHEME, parsed_url.netloc) is None:
        raise InvalidURL(f'{url_name} = {url} is an invalid url. Please check again.')


def validate_app_url(app_url: str):
    """

    :param app_url:
    :return:
    """
    __base_validate_url(url_name='app_url', url=app_url, allowed_schemes=['https'])


def validate_datalake_url(datalake_url: str):
    """

    :param datalake_url:
    :return:
    """
    __base_validate_url(url_name='datalake_url', url=datalake_url, allowed_schemes=['https'])


def validate_api_access_key(api_access_key: str):
    if api_access_key is None:
        raise ValueError('api_access_key cannot be None')

    if type(api_access_key) is not str:
        raise TypeError(INVALID_API_ACCESS_KEY_TYPE)

    if api_access_key.strip() == '':
        raise InvalidCredentialsError(EMPTY_API_ACCESS_KEY)


def validate_api_access_secret(api_access_secret: str):
    if api_access_secret is None:
        raise ValueError('api_access_secret cannot be None')

    if type(api_access_secret) is not str:
        raise TypeError(INVALID_API_ACCESS_SECRET_TYPE)

    if api_access_secret == '':
        raise InvalidCredentialsError(EMPTY_API_ACCESS_SECRET)


def validate_datalake_username(datalake_username: str):
    if datalake_username is None:
        raise ValueError('datalake_username cannot be None')

    if type(datalake_username) is not str:
        raise TypeError(INVALID_DATALAKE_USERNAME_TYPE)

    if datalake_username == '':
        raise InvalidCredentialsError(EMPTY_DATALAKE_USERNAME)


def validate_datalake_secret_key(datalake_secret_key: str):
    if datalake_secret_key is None:
        raise ValueError('datalake_secret_key cannot be None')

    if type(datalake_secret_key) is not str:
        raise TypeError(INVALID_DATALAKE_SECRET_KEY_TYPE)
    if datalake_secret_key == '':
        raise InvalidCredentialsError(EMPTY_DATALAKE_SECRET_KEY)


def validate_bucket(datalake_url: str, access_key: str, secret_key: str, bucket_name: str):
    if bucket_name is None:
        raise ValueError("bucket_name cannot be None")

    if type(bucket_name) is not str:
        raise TypeError(INVALID_BUCKET_NAME_TYPE)

    if bucket_name == '':
        raise InvalidBucketName(EMPTY_BUCKET_NAME)

    client = Minio(
        endpoint=datalake_url, access_key=access_key,
        secret_key=secret_key, secure=True
    )

    if not client.bucket_exists(bucket_name):
        raise BucketDoesNotExistsError(f'{bucket_name} does not exists')


def validate_secret_key(key_name: str, secret_key: str):
    """
    REMOVE IT IN FUTURE VERSIONS
    :param key_name:
    :param secret_key:
    :return:
    """
    if type(secret_key) is not str:
        raise TypeError(f'{key_name} can only be of type String')
    if secret_key == '':
        raise InvalidCredentialsError(f'{key_name} cannot empty')


def validate_plan_id(plan_id: str):
    pass


def validate_datacenter_id(datacenter_id: str):
    # TODO: Validate the id from via API
    if type(datacenter_id) is not str:
        raise TypeError('datacenter_id can only be of type String')
    if datacenter_id == '':
        raise ValueError('datacenter_id cannot empty')


def basic_validate_namespace_id(namespace_id: str):
    pass


def validate_orchestration_id(orchestration_add_on_id: str):
    pass


def validate_orchestration_name(orchestration_name: str, raise_exception: bool = False):
    if orchestration_name is None:
        if raise_exception:
            raise ValueError('orchestration_name cannot be None')
        return False
    if type(orchestration_name) is not str:
        if raise_exception:
            raise TypeError('orchestration_name can only be of type String')
        return False

    if orchestration_name.strip() == '':
        if raise_exception:
            raise ValueError('orchestration_name cannot empty')
        return False

    return True


def validate_orchestration_workers(min_workers: int, max_workers: int, raise_exception: bool = False):
    if type(min_workers) is not int:
        if raise_exception:
            raise TypeError('Orchestration min_workers can only be of type Integer')
        return False

    if type(max_workers) is not int:
        if raise_exception:
            raise TypeError('Orchestration max_workers can only be of type Integer')
        return False

    if min_workers < 1:
        if raise_exception:
            raise ValueError('Orchestration min_workers should be >=1')
        return False

    if max_workers < min_workers:
        if raise_exception:
            raise ValueError('min_workers in an Orchestration cannot be greater than max_workers')
        return False

    return True


def validate_envs_args(name: str, val: list[str]):
    assert all([len(kv.split("=")) == 2 for kv in
                val]), f"{name} should be a string with comma-separated key value pairs. For e.g. 'k1=v1, k2=v2, k3=v3'"


def validate_ai_api_name(ai_api_name: str):
    if ai_api_name is None:
        raise ValueError("ai_api_name cannot be None")
    if type(ai_api_name) is not str:
        raise TypeError(INVALID_AI_API_NAME_TYPE)
    if ai_api_name.strip() == '':
        raise ValueError(EMPTY_AI_API_NAME)


def validate_ai_api_type(ai_api_type: str):
    if ai_api_type is None:
        raise ValueError("ai_api_type cannot be None")
    if type(ai_api_type) is not str:
        raise TypeError(INVALID_AI_API_TYPE_TYPE)
    if ai_api_type.strip() == '':
        raise ValueError(EMPTY_AI_API_TYPE)
    if ai_api_type.strip() not in ['bentoml', 'openvino', 'mlflow', 'llm']:
        raise ValueError(INVALID_AI_API_TYPE)


def validate_model_folder(model_folder_path: Path):
    if model_folder_path == Path(''):
        raise ValueError(EMPTY_MODEL_FOLDER_PATH)

    if not model_folder_path.exists():
        raise DirectoryNotFoundError(
            MODEL_FOLDER_PATH_DOES_NOT_EXIST.format(model_folder_path=model_folder_path.as_posix())
        )

    if not model_folder_path.is_dir():
        raise NotADirectoryError(
            MODEL_FOLDER_PATH_NOT_DIR.format(model_folder_path=model_folder_path.as_posix())
        )

    if not os.access(model_folder_path.parent, os.W_OK):
        raise PermissionError(
            MODEL_FOLDER_PARENT_PATH_NO_WRITE_PERMISSION.format(model_folder_path=model_folder_path.parent.as_posix())
        )


def validate_microservice_name(microservice_name: str):
    if microservice_name is None:
        raise ValueError('microservice_name cannot be None')

    if type(microservice_name) is not str:
        raise TypeError('microservice_name can only be of type String')

    if microservice_name.strip() == '':
        raise ValueError('microservice_name cannot empty')


def validate_microservice_display_name(display_name: str, valid_display_names: List[str], err_msg: str):
    if display_name is None:
        raise ValueError('display_name cannot be None')

    if type(display_name) is not str:
        raise TypeError('display_name can only be of type String')

    if display_name.strip() == '':
        raise ValueError('display_name cannot empty')

    if display_name.strip() not in valid_display_names:
        raise ValueError(err_msg)


def validate_microservice_ports(ports: List[Dict]):
    # if not __is_list_of_dicts(ports):
    #     raise TypeError("ports can only be of type List[Dict]")

    if len(ports) == 0:
        return
    for _p in ports:
        if _p.get("protocol", None) is None:
            raise ValueError("`protocol` key missing ports. Please check your input for `ports`.")

        if _p['protocol'] not in ['HTTP', 'HTTPS', 'TCP', 'GRPC']:
            raise ValueError(
                f"protocol in `ports` should be one of `HTTP`, `HTTPS`, `TCP` or `GRPC`. Given {_p['protocol']}."
            )

        if _p.get("number", None) is None:
            raise ValueError("`number` key missing ports. Please check your input for `ports`.")

        if _p["number"] < 0 or _p["number"] > 65536:
            raise ValueError(f"port number must be between 0-65536. Given {_p['number']}.")


def validate_microservice_envs(envs: List[Dict]):
    # if not __is_list_of_dicts(envs):
    #     raise TypeError("envs can only be of type List[Dict]")

    if len(envs) == 0:
        return

    for _p in envs:
        if _p.get("key", None) is None:
            raise ValueError("`key` key missing envs. Please check your input for `ports`.")

        if _p.get("value", None) is None:
            raise ValueError("`value` key missing envs. Please check your input for `ports`.")


def validate_microservice_args(args: List[Dict]):
    # if not __is_list_of_dicts(args):
    #     raise TypeError("args can only be of type List[Dict]")

    if len(args) == 0:
        return

    for _p in args:
        if _p.get("key", None) is None:
            raise ValueError("`key` key missing args. Please check your input for `ports`.")


def validate_ai_pipeline_name(ai_pipeline_name: str):
    if ai_pipeline_name is None:
        raise ValueError("ai_pipeline_name cannot be None")
    if type(ai_pipeline_name) is not str:
        raise TypeError(INVALID_AI_PIPELINE_NAME_TYPE)
    if ai_pipeline_name.strip() == '':
        raise ValueError(EMPTY_AI_PIPELINE_NAME)


def has_permission(filepath: Path, permission: str = "read") -> bool:
    if permission == "write":
        try:
            with open(filepath, "w") as __temp_file:
                __temp_file.write("Testing write permission in file.")
            os.remove(filepath)
            return True
        except PermissionError as _:
            return False

    if permission == "read":
        try:
            with open(filepath, "r") as __temp_file:
                pass
            return True
        except PermissionError as _:
            return False

    return False


"""
OLD CODE
"""


def validate_model_version(model_version: str):
    if type(model_version) is not str:
        raise ValueError('model_version can only be of type String')
    if model_version == '':
        raise ValueError('model_version cannot empty')


def validate_model_pipeline(model_pipeline: str):
    if type(model_pipeline) is not str:
        raise ValueError('image_name can only be of type String')
    if model_pipeline == '':
        raise ValueError('image_name cannot empty')


def validate_token(token: str):
    if type(token) is not str:
        raise InvalidCredentialsError(f'ERROR: Token can only be of type String')
    if token == '':
        raise InvalidCredentialsError(f'ERROR: Token cannot empty')

    if len(token.split()) != 2 or token.split()[0] != 'Bearer':
        raise InvalidCredentialsError(f'ERROR: Token should be of the format `Bearer <your-token>`')


def validate_id(id_name: str, id_val: str):
    if type(id_val) is not str:
        raise ValueError(f'{id_name} can only be of type String')
    if id_val == '':
        raise ValueError(f'{id_name} cannot empty')
