from abc import ABC, abstractmethod
from ..utils.errors import BucketDoesNotExistsError, ObjectDoesNotExistsError, FileUploadError, FileDownloadError
from pathlib import Path
from typing import Union
from ..utils.validations import has_permission


class DataSetBase(ABC):
    __slots__ = ['__bucket_name', '__bucket_does_not_exists']

    def __init__(self, access_key: str, access_secret: str, bucket_name: str):
        if bucket_name is None or bucket_name == "":
            raise ValueError("bucket_name cannot be None or empty")

        if type(bucket_name) != str:
            raise TypeError("bucket_name can only be of type string")

        self.__bucket_name = bucket_name
        self.__bucket_does_not_exists = None

        if not self.bucket_exists():
            raise BucketDoesNotExistsError(f"Bucket `{self.__bucket_name}` does not exist.")

    @property
    def bucket_name(self):
        return self.__bucket_name

    @abstractmethod
    def _bucket_exists(self) -> bool:
        pass

    def bucket_exists(self) -> bool:
        if self.__bucket_does_not_exists is not None:
            return not self.__bucket_does_not_exists

        if type(self.__bucket_name) != str or self.__bucket_name is None or self.__bucket_name == "":
            self.__bucket_does_not_exists = True
            return False

        self.__bucket_does_not_exists = not self._bucket_exists()

        return not self.__bucket_does_not_exists

    @abstractmethod
    def _object_exists(self, object_name: str) -> bool:
        pass

    def object_exists(self, object_name: str) -> bool:
        if self.__bucket_does_not_exists:
            return False

        if type(object_name) != str or object_name is None or object_name == "":
            return False

        return self._object_exists(object_name=object_name)

    @abstractmethod
    def _upload_object(self, *args, **kwargs) -> tuple[bool, str]:
        pass

    def upload_object(self, local_file_pathname: Union[str, Path], object_name: str = None) -> bool:
        if object_name is not None and type(object_name) == "":
            raise ValueError("object_name cannot be empty")

        if object_name is not None and type(object_name) != str:
            raise TypeError("object_name can only be of type string")

        if not self.bucket_exists():
            raise BucketDoesNotExistsError(f"Bucket `{self.bucket_name}` does not exist.")

        if not Path(local_file_pathname).exists():
            raise FileNotFoundError(f"File `{local_file_pathname}` does not exist.")

        if not has_permission(filepath=Path(local_file_pathname), permission="read"):
            raise PermissionError(
                f"Directory: {Path(local_file_pathname).as_posix()} doesn't have the read permission."
            )

        res, msg = self._upload_object(local_file_pathname=local_file_pathname, object_name=object_name)
        if not res and msg != '':
            raise FileUploadError(msg)
        return res

    @abstractmethod
    def _download_object(self, *args, **kwargs) -> tuple[bool, str]:
        pass

    def download_object(self, object_name: str, local_dir: str, filename: str) -> bool:
        if object_name is None or object_name == "":
            raise ValueError("object_name cannot be None or empty")

        if type(object_name) != str:
            raise TypeError("object_name can only be of type string")

        if filename is None or filename == "":
            raise ValueError("filename cannot be None or empty")

        if type(filename) != str:
            raise TypeError("filename can only be of type string")

        if not self.bucket_exists():
            raise BucketDoesNotExistsError(f"Bucket `{self.bucket_name}` does not exist.")

        if not self.object_exists(object_name=object_name):
            raise ObjectDoesNotExistsError(f"Object `{object_name}` does not exist in bucket {self.bucket_name}.")

        local_dir = Path(local_dir)
        if not local_dir.is_dir():
            raise NotADirectoryError(f"`{local_dir.as_posix()}` does not exist.")

        if not has_permission(filepath=local_dir.joinpath("temp_zbl_sdk_test.txt"), permission="write"):
            raise PermissionError(f"Directory: {local_dir} doesn't have permission to create or write files.")

        res, msg = self._download_object(object_name=object_name, local_dir=Path(local_dir), filename=filename)
        if not res and msg != '':
            raise FileDownloadError(msg)
        return res

    @abstractmethod
    def _get_presigned_url(self, *args, **kwargs):
        pass

    def get_presigned_url(self, object_name: str) -> str:
        if object_name is None or object_name == "":
            raise ValueError("object_name cannot be None or empty")

        if type(object_name) != str:
            raise TypeError("object_name can only be of type string")

        if not self.object_exists(object_name=object_name):
            raise ObjectDoesNotExistsError(f"Object `{object_name}` does not exist in bucket {self.bucket_name}.")

        return self._get_presigned_url(object_name)
