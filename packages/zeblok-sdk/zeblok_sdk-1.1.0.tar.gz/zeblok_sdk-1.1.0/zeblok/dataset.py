from .base.base_dataset import DataSetBase
from .utils.errors import api_error
import boto3
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig
from pathlib import Path
from .auth import APIAuth
import os
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from typing import Union
from tqdm import tqdm
import requests
from . import PRESIGNED_URL_EXPIRATION_SECS
from datetime import datetime, timedelta


class AwsS3(DataSetBase):
    def __init__(self, access_key: str, secret_key: str, bucket_name: str):
        self.__s3_client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

        super().__init__(
            access_key=access_key, access_secret=secret_key, bucket_name=bucket_name
        )

    def _bucket_exists(self) -> bool:
        try:
            return self.__s3_client.head_bucket(Bucket=self.bucket_name)['ResponseMetadata']['HTTPStatusCode'] == 200
        except ClientError as e:
            print(e)
            return False

    def _object_exists(self, object_name: str) -> bool:
        try:
            if self.__s3_client.head_object(
                    Bucket=self.bucket_name, Key=object_name)['ResponseMetadata']['HTTPStatusCode'] == 200:
                return True
        except ClientError as e:
            # print(e)
            return False
        return False

    def _upload_object(self, local_file_pathname: Union[str, Path], object_name=None) -> tuple[bool, str]:
        if object_name is None:
            object_name = Path(local_file_pathname).name
        mb = 1024 ** 2

        """
        Multipart Issue: https://repost.aws/questions/QUUEXu-FFVQq6rP6FEyTlkYA/python-boto3-s3-multipart-upload-in-multiple-threads-doesn-t-work
        """
        config = TransferConfig(multipart_threshold=30 * mb, multipart_chunksize=30 * mb, io_chunksize=2 * mb)

        try:

            with tqdm(
                    total=os.path.getsize(local_file_pathname),
                    unit='B', unit_scale=True,
                    desc=f'Uploading {local_file_pathname} --> {object_name}'
            ) as progress_bar:

                self.__s3_client.upload_file(
                    local_file_pathname, self.bucket_name, object_name, Config=config,
                    Callback=lambda chunk: progress_bar.update(chunk)
                )
            return True, ""
        except Exception as e:
            return False, str(e)

    def _download_object(self, object_name: str, local_dir: Path, filename: str) -> tuple[bool, str]:
        try:
            with tqdm(
                    total=self.__s3_client.head_object(Bucket=self.bucket_name, Key=object_name)['ContentLength'],
                    unit='B', unit_scale=True,
                    desc=f'Downloading {object_name} --> {local_dir.joinpath(filename)}'
            ) as progress_bar:
                self.__s3_client.download_fileobj(
                    self.bucket_name, object_name, open(local_dir.joinpath(filename), 'wb'),
                    Callback=lambda chunk: progress_bar.update(chunk)
                )
            return True, ""
        except Exception as e:
            return False, str(e)

    def _get_presigned_url(self, object_name: str):
        return self.__s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': object_name},
            ExpiresIn=PRESIGNED_URL_EXPIRATION_SECS
        )


class AzureBlob(DataSetBase):
    def __init__(self, access_key: str, secret_key: str, bucket_name: str):
        self.__container_client = BlobServiceClient(
            account_url=f"https://{access_key}.blob.core.windows.net",
            credential={
                "account_name": access_key,
                "account_key": secret_key
            }
        )

        super().__init__(
            access_key=access_key, access_secret=secret_key, bucket_name=bucket_name
        )

    def _bucket_exists(self) -> bool:
        return self.__container_client.get_container_client(container=self.bucket_name).exists()

    def _object_exists(self, object_name: str) -> bool:
        return self.__container_client.get_blob_client(container=self.bucket_name, blob=object_name).exists()

    def _upload_object(self, local_file_pathname: Union[str, Path], object_name=None) -> tuple[bool, str]:
        if object_name is None:
            object_name = Path(local_file_pathname).name
        try:
            size = os.stat(local_file_pathname).st_size
            with tqdm.wrapattr(
                    open(local_file_pathname, 'rb'), "read", total=size,
                    desc=f'Uploading {local_file_pathname} --> {object_name}'
            ) as data:
                self.__container_client.get_container_client(self.bucket_name).upload_blob(
                    name=object_name, data=data, overwrite=True
                )
            return True, ""
        except Exception as e:
            return False, str(e)

    def _download_object(self, object_name: str, local_dir: Path, filename: str) -> tuple[bool, str]:
        try:
            _blob_client = self.__container_client.get_blob_client(container=self.bucket_name, blob=object_name)
            with tqdm(
                    total=_blob_client.get_blob_properties().size, unit='B', unit_scale=True,
                    desc=f'Downloading {object_name} --> {local_dir.joinpath(filename)}'
            ) as progress_bar:
                with open(local_dir.joinpath(filename), "wb") as local_file:
                    download_stream = _blob_client.download_blob()
                    bytes_downloaded = 0
                    for chunk in download_stream.chunks():
                        local_file.write(chunk)
                        bytes_downloaded += len(chunk)
                        progress_bar.update(len(chunk))
            return True, ""
        except Exception as e:
            return False, str(e)

    def _get_presigned_url(self, object_name: str):
        sas_blob = generate_blob_sas(
            account_name=self.__container_client.credential.account_name,
            account_key=self.__container_client.credential.account_key, container_name=self.bucket_name,
            blob_name=object_name, permission=BlobSasPermissions(read=True, write=False, create=False),
            expiry=datetime.utcnow() + timedelta(seconds=PRESIGNED_URL_EXPIRATION_SECS)
        )
        return f"https://{self.__container_client.credential.account_name}.blob.core.windows.net/{self.bucket_name}/{object_name}?{sas_blob}"


class DataSet:
    def __init__(self, api_auth: APIAuth, access_key: str, secret_key: str, bucket_name: str):
        if api_auth is None:
            raise ValueError("api_auth cannot be None")

        if type(api_auth) != APIAuth:
            raise TypeError("api_auth can only be of type APIAuth")

        self.__api_auth = api_auth

        if access_key is None or access_key == "":
            raise ValueError("access_key cannot be None or empty")

        if type(access_key) != str:
            raise TypeError("access_key can only be of type string")

        if secret_key is None or secret_key == "":
            raise ValueError("secret_key cannot be None or empty")

        if type(secret_key) != str:
            raise TypeError("secret_key can only be of type string")

        self.__object_store = self.__identify_object_store()

        if self.__object_store == "AZURE":
            self.__object_store_client = AzureBlob(
                access_key=access_key, secret_key=secret_key, bucket_name=bucket_name
            )
        elif self.__object_store == "AWS":
            self.__object_store_client = AwsS3(access_key=access_key, secret_key=secret_key, bucket_name=bucket_name)
        else:
            raise NotImplementedError("Need to integrate MinIO.")

    def __identify_object_store(self):
        response = requests.get(
            f"{self.__api_auth.app_url}/api/v1/datasets/objectStorage/type",
            headers={'Content-Type': 'application/json'},
            auth=self.__api_auth.get_api_creds()
        )

        if response.status_code == 200 and response.json()['success']:
            return response.json()['data']

        api_error(
            status_code=response.status_code, message=f"""
            Unable to identify the object store being used.
            Message from server:
            \t{response.text}
            """
        )

    @property
    def bucket_name(self):
        return self.__object_store_client.bucket_name

    def bucket_exists(self) -> bool:
        return self.__object_store_client.bucket_exists()

    def object_exists(self, object_name: str) -> bool:
        return self.__object_store_client.object_exists(object_name=object_name)

    def upload_object(self, local_file_pathname: Union[str, Path], object_name: str = None) -> bool:
        return self.__object_store_client.upload_object(
            local_file_pathname=Path(local_file_pathname),
            object_name=object_name
        )

    def download_object(self, object_name: str, local_dir: str, filename: str) -> bool:
        return self.__object_store_client.download_object(
            object_name=object_name,
            local_dir=local_dir,
            filename=filename
        )

    def get_presigned_url(self, object_name: str) -> str:
        return self.__object_store_client.get_presigned_url(object_name=object_name)
