import json
from abc import abstractmethod
from datetime import timedelta
import requests
from ..auth import APIAuth, DatalakeAuth
from .base_service import ServiceSpawnBase
from zipfile import ZipFile
from pathlib import Path
import minio
import os
from typing import Union
from ..utils.progressbar import Progress
from ..utils.errors import api_error, CaaSUploadError
from ..utils.misc import get_all_file_paths
from ..utils.validations import validate_model_folder
from ..dataset import DataSet


class AIRunsBase(ServiceSpawnBase):
    __slots__ = ['_plan']

    def __init__(self, api_auth: APIAuth, dataset: DataSet):
        super().__init__(api_auth)
        self._dataset = dataset

    def _call_containerization_service(
            self, presigned_get_url: str, image_name: str, file_name: str, image_id: str, caas_plan_id: str,
            deployment_type: str, error_msg: str, plan_id: Union[str, list[str], None] = None, autodeploy: bool = False,
            deployment_name: Union[str, None] = None, namespace_id: Union[str, None] = None,
            datacenter_ids: Union[str, list[str], None] = None
    ):
        response = requests.post(
            self._api_auth.app_url + "/api/v1/system/kaniko",
            auth=self._api_auth.get_api_creds(),
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                "imageName": image_name,
                "imageId": image_id,
                "url": presigned_get_url,
                "filename": file_name,
                "portalUrl": f"{self._api_auth.app_url}",
                "autoDeploy": autodeploy,
                "deploymentType": deployment_type,
                "namespaceId": namespace_id,
                "platform": datacenter_ids,
                "kioskArray": None,
                "planId": plan_id,
                "deploymentName": deployment_name,
                "caas_plan": caas_plan_id
            })
        )

        if response.status_code == 200 and response.json()['success']:
            return True

        api_error(status_code=response.status_code, message=error_msg.format(response_text=response.text))

    @staticmethod
    def _prepare_model_zip(model_folder_path: Path) -> Path:

        validate_model_folder(model_folder_path)

        print("\nPreparing model zip")
        model_zipfile_path = model_folder_path.parent.joinpath(f'{model_folder_path.name.lower()}.zip')
        with ZipFile(model_zipfile_path, 'w') as zip:
            file_paths = get_all_file_paths(directory=model_folder_path)
            for file in file_paths:
                zip.write(filename=file.as_posix(), arcname=file.relative_to(model_folder_path))
        print("Model zip prepared")
        return model_zipfile_path

    def _upload_file_to_datalake(self, file_name: Path) -> str:
        try:

            if not self._dataset.upload_object(local_file_pathname=file_name):
                raise CaaSUploadError(f"Error Uploading {file_name} to bucket {self._dataset.bucket_name}")
            print("")
            return self._dataset.get_presigned_url(object_name=file_name.name)
        finally:
            os.remove(file_name)

    @abstractmethod
    def _create(self, *args, **kwargs):
        pass

    @abstractmethod
    def create_and_spawn(self, *args, **kwargs):
        pass

    @abstractmethod
    def create(self, *args, **kwargs):
        pass
