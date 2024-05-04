from typing import Union, Tuple, List, Dict
from pathlib import Path
import time
from .utils.errors import api_error
import requests
import json
from .base.base_airuns import AIRunsBase
from .auth import APIAuth
from . import DOCKER_HUB_URL
from .utils.validations import validate_ai_api_name, validate_ai_api_type
from .utils.error_message import NO_AI_API_STATE
from . import PLAN_TYPE_API, PLAN_TYPE_CAAS
from .utils.error_message import NO_AI_API_IMAGE_NAME
from .dataset import DataSet


class API(AIRunsBase):
    def __int__(self, api_auth: APIAuth, dataset: DataSet):
        super().__init__(api_auth, dataset)

    @staticmethod
    def __print_info(ai_apis: List[Dict], state: str, error_message: str = None):
        print(f"AI-APIs with state: {state}")
        if len(ai_apis) > 0:
            for idx, data in enumerate(ai_apis):
                print(f"\t{idx + 1}. id: {data['id']} | image_name: {data['image_name']} | type: {data['type']}")
        else:
            print(f"\t{'No resources available' if error_message is None else error_message}")

    @staticmethod
    def __process_single_element(element: Dict) -> Dict:
        return {
            'id': element.get('_id', ''), 'image_name': element.get('imageName', ''), 'type': element.get('type', '')
        }

    @classmethod
    def __process_response(
            cls,
            response: requests.Response, return_data: bool = True,
            raise_exception: bool = True, error_message: str = None,
    ) -> Union[List[Dict], Dict, bool, None]:
        ai_api_data = []
        data_retrieval_success = response.status_code == 200 and response.json()['success'] and response.json()[
            'totalCount'] > 0

        if not return_data:
            return True if data_retrieval_success else False

        if not data_retrieval_success and raise_exception:
            api_error(
                status_code=response.status_code,
                message=response.text if error_message is None else error_message
            )

        if data_retrieval_success:
            ai_api_data = list(map(lambda data: cls.__process_single_element(data), response.json()['data']))

        return ai_api_data

    def __get(
            self,
            state: str = 'deployed', return_data: bool = True, raise_exception: bool = True, error_message: str = None
    ):
        if state is None:
            raise ValueError("state cannot be None")

        if type(state) is not str:
            raise TypeError('state can only be of type String')

        if state not in ['deployed', 'ready']:
            raise ValueError(f"state given: {state}. Acceptable value on of these: ['deployed', 'ready']")

        url = f"{self._api_auth.app_url}/api/v1/k8deployments" if state == 'deployed' else f"{self._api_auth.app_url}/api/v1/aimodel"
        response = requests.get(
            url, headers={'Content-Type': 'application/json'}, auth=self._api_auth.get_api_creds(),
            params={"deploymentStatus": state} if state == 'deployed' else {"state": "ready"}
        )

        return self.__process_response(
            response=response, return_data=return_data, raise_exception=raise_exception,
            error_message=error_message
        )

    def _create(self, ai_api_name: str, ai_api_type: str) -> Tuple[str, str]:
        validate_ai_api_name(ai_api_name=ai_api_name)
        validate_ai_api_type(ai_api_type=ai_api_type)

        image_version = int(time.time())

        image_name = f"{DOCKER_HUB_URL}/{'-'.join(ai_api_name.strip().split(' '))}:{image_version}".lower()

        response = requests.post(
            f"{self._api_auth.app_url}/api/v1/aimodel/",
            headers={'Content-Type': 'application/json'},
            data=json.dumps({"imageName": image_name, "type": ai_api_type.strip()}),
            auth=self._api_auth.get_api_creds()
        )

        if response.status_code == 201 and response.json()['success']:
            return response.json()['data']['_id'], image_name

        api_error(
            status_code=response.status_code,
            message=f"Unable to create AI-API.\nMessage from server: {response.text}"
        )

    def validate(self, image_name: str, state: str) -> bool:
        if image_name is None:
            raise ValueError("image_name cannot be None")

        if type(image_name) is not str:
            raise TypeError('image_name can only be of type String')

        if image_name.strip() == "":
            raise ValueError("image_name cannot be empty")

        ai_api_data = self.__get(state=state, return_data=True, raise_exception=False, error_message=None)

        return image_name.strip() in [_ai_api['image_name'] for _ai_api in ai_api_data]

    def create_and_spawn(
            self, ai_api_name: str, model_folder_path: str, ai_api_plan_id: str, namespace_id: str, caas_plan_id: str,
            ai_api_type='llm'
    ):
        self._namespace.validate_id(namespace_id=namespace_id, raise_exception=True)
        datacenter_id = self._validate_plan_and_get_datacenter(ai_api_plan_id, PLAN_TYPE_API)

        caas_datacenter_id = self._validate_plan_and_get_datacenter(caas_plan_id, PLAN_TYPE_CAAS)

        if caas_datacenter_id != datacenter_id:
            raise ValueError("CaaS plan and AI-API plan should belong to the same Datacenter.")

        model_zipfile_path = self._prepare_model_zip(model_folder_path=Path(model_folder_path))

        presigned_url = self._upload_file_to_datalake(file_name=model_zipfile_path)

        ai_api_id, image_name = self._create(ai_api_name, ai_api_type)

        self._call_containerization_service(
            presigned_get_url=presigned_url, image_name=image_name, file_name=model_zipfile_path.name,
            image_id=ai_api_id, namespace_id=namespace_id, deployment_name=ai_api_name, datacenter_ids=datacenter_id,
            deployment_type='aimodel', autodeploy=True, plan_id=ai_api_plan_id, caas_plan_id=caas_plan_id,
            error_msg="""
            Unable to create AI-API. Auto-Deploy: Error in Containerization or Spawning.
            Message from server:
            \t{response_text}
            """
        )

        print(
            f"""
            \nSuccessfully uploaded the Model folder | Filename: {model_zipfile_path.name}, Image Name: {image_name}
            \nAI-API will be spawned shortly
            """
        )
        return image_name

    def create(
            self, ai_api_name: str, model_folder_path: str, caas_plan_id: str, ai_api_type='llm'
    ) -> str:
        model_zipfile_path = self._prepare_model_zip(model_folder_path=Path(model_folder_path))
        presigned_url = self._upload_file_to_datalake(file_name=model_zipfile_path)

        ai_api_id, image_name = self._create(ai_api_name, ai_api_type)

        __caas_datacenter_id = self._validate_plan_and_get_datacenter(caas_plan_id, PLAN_TYPE_CAAS)

        self._call_containerization_service(
            presigned_get_url=presigned_url, image_name=image_name, file_name=model_zipfile_path.name,
            image_id=ai_api_id, deployment_type='aimodel', autodeploy=False, caas_plan_id=caas_plan_id,
            error_msg="""
            Unable to create AI-API. Non Auto-Deploy: Error in Containerization.
            Message from server:
            \t{response_text}
            """
        )

        print(
            f"Created AI-API with image name: {image_name}. Please use spawn() with {image_name} image_name."
        )
        return image_name

    def spawn(self, image_name: str, namespace_id: str, plan_id: str):
        self._namespace.validate_id(namespace_id=namespace_id, raise_exception=True)
        datacenter_id = self._validate_plan_and_get_datacenter(plan_id, PLAN_TYPE_API)
        if not self.validate(image_name=image_name, state='ready'):
            raise ValueError(NO_AI_API_IMAGE_NAME.format(image_name=image_name))

        image_name = image_name.strip()

        ai_api_name = image_name.split('/')[-1]

        response = requests.post(
            f"{self._api_auth.app_url}/api/v1/k8deployments/",
            headers={'Content-Type': 'application/json'},
            auth=self._api_auth.get_api_creds(),
            data=json.dumps({
                "imageName": image_name, "namespaceId": namespace_id,
                "platform": datacenter_id,
                "planId": plan_id,
                "kioskId": None,
                "nodePreference": "NO PREFERENCE",
                "deploymentType": "aimodel",
                "deploymentName": ai_api_name
            })
        )

        if response.status_code == 201 and response.json()['success']:
            print(f"Deployment {ai_api_name} created. Please visit: {self._api_auth.app_url}/app/admin/runtimes")
            return response.json()['success']

        api_error(
            status_code=response.status_code, message=f"""
            Unable to spawn the AI-API with image name {image_name}.
            Message from server:
            \t{response.text}
            """
        )

    def get_all(self, state: str = 'deployed', print_stdout: bool = True):
        ai_api_data = self.__get(
            state=state, return_data=True, raise_exception=False,
            error_message=NO_AI_API_STATE.format(state=state)
        )
        if print_stdout:
            self.__print_info(ai_apis=ai_api_data, state=state, error_message=NO_AI_API_STATE.format(state=state))

        return ai_api_data
