import pytest
import pathlib
import os
from zeblok.utils import seconds_to_time, Progress, validate_secret_key, validate_id, validate_token, \
    validate_model_pipeline, validate_envs_args, validate_platform_id, validate_namespace_id, validate_deployment_name, \
    validate_model_version, validate_storage_url, validate_model_folder
from zeblok.errors import InvalidCredentialsError, InvalidURL


@pytest.fixture
def progress_init():
    return Progress()


class UploadModelUtils:
    @staticmethod
    def mock_exists(path):
        return True

    @staticmethod
    def mock_is_dir(path):
        return True

    @staticmethod
    def mock_os_access(path, mode=os.W_OK):
        return True


class TestSecondsToTime:
    def test_mins(self):
        assert seconds_to_time(58 * 60) == '58:00'

    def test_hours(self):
        assert seconds_to_time(150 * 60) == '2:30:00'


class TestProgress:
    def test_set_meta(self, progress_init):
        total_length = 100
        progress_init.set_meta(total_length=total_length, object_name='temp_obj_name')
        assert progress_init.total_length == total_length

    def test_update(self, progress_init):
        current_size = 10
        progress_init.update(size=current_size)
        assert progress_init.current_size == current_size

    def test_update_int_size(self, progress_init):
        current_size = '10'
        with pytest.raises(
                expected_exception=ValueError,
                match=f'{type(current_size)} type can not be displayed. Please change it to Int.'
        ):
            progress_init.update(size=current_size)

    def test_done_progress(self, progress_init):
        progress_init.done_progress()
        assert progress_init.total_length == 0

    def test_print_status(self, progress_init):
        progress_init.print_status(current_size=1, total_length=10, displayed_time=0, prefix='')
        assert progress_init.last_printed_len == 82


class TestValidateSecretKey:
    def test_int_secret_key(self):
        with pytest.raises(
                expected_exception=InvalidCredentialsError, match="secret-key-name can only be of type String"
        ):
            validate_secret_key(key_name="secret-key-name", secret_key=1)

    def test_empty_secret_key(self):
        with pytest.raises(
                expected_exception=InvalidCredentialsError, match="secret-key-name cannot empty"
        ):
            validate_secret_key(key_name="secret-key-name", secret_key='')


class TestValidateId:
    def test_int_id(self):
        with pytest.raises(
                expected_exception=ValueError, match="id-name can only be of type String"
        ):
            validate_id(id_name="id-name", id_val=1)

    def test_empty_id(self):
        with pytest.raises(
                expected_exception=ValueError, match="id-name cannot empty"
        ):
            validate_id(id_name="id-name", id_val='')


class TestValidateToken:
    def test_int_token(self):
        with pytest.raises(expected_exception=InvalidCredentialsError, match="ERROR: Token can only be of type String"):
            validate_token(token=123)

    def test_empty_token(self):
        with pytest.raises(expected_exception=InvalidCredentialsError, match="ERROR: Token cannot empty"):
            validate_token(token="")

    def test_token_without_bearer_keyword(self):
        with pytest.raises(
                expected_exception=InvalidCredentialsError,
                match="ERROR: Token should be of the format `Bearer <your-token>`"
        ):
            validate_token(token="temp token")

    def test_token_with_len_1(self):
        with pytest.raises(
                expected_exception=InvalidCredentialsError,
                match="ERROR: Token should be of the format `Bearer <your-token>`"
        ):
            validate_token(token="temp-token")


class TestValidateModelPipeline:
    def test_int_model_pipeline(self):
        with pytest.raises(
                expected_exception=ValueError, match="image_name can only be of type String"
        ):
            validate_model_pipeline(model_pipeline=123)

    def test_empty_model_pipeline(self):
        with pytest.raises(
                expected_exception=ValueError, match="image_name cannot empty"
        ):
            validate_model_pipeline(model_pipeline="")


class TestValidateEnvArgs:
    def test_invalid_format(self):
        with pytest.raises(
                expected_exception=AssertionError,
                match="temp_env should be a string with comma-separated key value pairs. For e.g. 'k1=v1, k2=v2, k3=v3'"
        ):
            validate_envs_args(name="temp_env", val=['k1=v1', 'k2v2'])


class TestValidatePlatformId:
    def test_int_platform_id(self):
        with pytest.raises(
                expected_exception=ValueError, match="platform_id can only be of type String"
        ):
            validate_platform_id(platform_id=123)

    def test_empty_platform_id(self):
        with pytest.raises(
                expected_exception=ValueError, match="platform_id cannot empty"
        ):
            validate_platform_id(platform_id="")


class TestValidateNamespaceId:
    def test_int_namespace_id(self):
        with pytest.raises(
                expected_exception=ValueError, match="namespace_id can only be of type String"
        ):
            validate_namespace_id(namespace_id=123)

    def test_empty_namespace_id(self):
        with pytest.raises(
                expected_exception=ValueError, match="namespace_id cannot empty"
        ):
            validate_namespace_id(namespace_id="")


class TestValidateModelVersion:
    def test_int_model_version(self):
        with pytest.raises(
                expected_exception=ValueError, match="model_version can only be of type String"
        ):
            validate_model_version(model_version=123)

    def test_empty_model_version(self):
        with pytest.raises(
                expected_exception=ValueError, match="model_version cannot empty"
        ):
            validate_model_version(model_version="")


class TestValidateDeploymentName:
    def test_int_deployment_name(self):
        with pytest.raises(
                expected_exception=ValueError, match="deployment_name can only be of type String"
        ):
            validate_deployment_name(deployment_name=123)

    def test_empty_deployment_name(self):
        with pytest.raises(
                expected_exception=ValueError, match="deployment_name cannot empty"
        ):
            validate_deployment_name(deployment_name="")


class TestValidateStorageURL:
    """
    To be deprecated in future versions
    """

    def test_int_storage_url(self):
        with pytest.raises(
                expected_exception=InvalidURL, match="storage_url can only be of type String"
        ):
            validate_storage_url(storage_url=123)

    def test_empty_storage_url(self):
        with pytest.raises(
                expected_exception=InvalidURL, match="storage_url cannot empty"
        ):
            validate_storage_url(storage_url="")


class TestValidateModelFolder:

    def test_empty_folder_path(self):
        with pytest.raises(expected_exception=ValueError, match="Model folder path is empty"):
            validate_model_folder(model_folder_path=pathlib.Path(""))


class TestValidateFolderFormat(UploadModelUtils):
    def test_empty_model_folder_path(self):
        with pytest.raises(expected_exception=ValueError, match="Model folder path is empty"):
            validate_model_folder(model_folder_path=pathlib.Path(""))

    def test_does_not_exist(self, monkeypatch):
        def mock_exists(path):
            return False

        temp_model_folder_path = r'temp_model_folder_path'
        monkeypatch.setattr(pathlib.Path, 'exists', mock_exists)
        with pytest.raises(
                expected_exception=FileNotFoundError,
                match=f"{pathlib.Path(temp_model_folder_path)} does not exist"
        ):
            validate_model_folder(model_folder_path=pathlib.Path(temp_model_folder_path))

    def test_not_a_directory(self, monkeypatch):
        def mock_is_dir(path):
            return False

        temp_model_folder_path = r'temp_model_folder_path'
        monkeypatch.setattr(pathlib.Path, 'exists', self.mock_exists)
        monkeypatch.setattr(pathlib.Path, 'is_dir', mock_is_dir)
        with pytest.raises(
                expected_exception=NotADirectoryError,
                match=f"{pathlib.Path(temp_model_folder_path)} is not a folder"
        ):
            validate_model_folder(model_folder_path=pathlib.Path(temp_model_folder_path))

    def test_no_write_access(self, monkeypatch):
        def mock_os_access(path, mode=os.W_OK):
            return False

        temp_model_folder_path = r'temp_model_folder_path'
        monkeypatch.setattr(pathlib.Path, 'exists', self.mock_exists)
        monkeypatch.setattr(pathlib.Path, 'is_dir', self.mock_is_dir)
        monkeypatch.setattr(os, 'access', mock_os_access)

        with pytest.raises(
                expected_exception=PermissionError,
                match=f"Folder doesn't have write permission: {temp_model_folder_path}"
        ):
            validate_model_folder(model_folder_path=pathlib.Path(temp_model_folder_path))
