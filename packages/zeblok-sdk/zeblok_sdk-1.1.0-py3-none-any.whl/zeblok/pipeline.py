from typing import Union, Tuple, List, Dict
from pathlib import Path
import time
from .utils.errors import api_error
import requests
import json
from .base.base_airuns import AIRunsBase
from .auth import APIAuth
from . import DOCKER_HUB_URL
from .utils.validations import validate_ai_pipeline_name
from . import PLAN_TYPE_MICROSERVICE, PLAN_TYPE_CAAS
from .utils.error_message import NO_AI_PIPELINE_STATE, NO_AI_PIPELINE_IMAGE_NAME
from .dataset import DataSet


class Pipeline(AIRunsBase):
    def __int__(self, api_auth: APIAuth, dataset: DataSet):
        super().__init__(api_auth, dataset)

    @staticmethod
    def __print_info(ai_pipelines: List[Dict], state: str, error_message: str = None):
        print(f"AI-Pipelines with state: {state}")
        if len(ai_pipelines) > 0:
            for idx, data in enumerate(ai_pipelines):
                print(f"\t{idx + 1}. {data['pipeline_name']}")
                print(
                    f"\t\timage_name: {data['image_name']} | created_at: {data['created_at']}"
                )
                print(
                    f"\t\tnamespace: {data['namespace']} | added_by: {data['added_by']} | organisation: {data['organisation']}"
                )
                print(f"\t\tPlans: {', '.join([p['name'] + ' (' + p['id'] + ')' for p in data['plans']])}")

                print("\t\tPipeline Runs:")
                if len(data['pipeline_runs']) > 0:
                    for idx_pr, pr in enumerate(data['pipeline_runs']):
                        print(f"\t\t\t{idx_pr + 1}. {pr['name']}")
                        print(
                            f"\t\t\t\tid: {pr['id']} | status: {pr['status']} | start_time: {pr['start_time']} | start_time: {pr['start_time']} | end_time: {pr['end_time']}"
                        )
                else:
                    print("\t\t\tNo Pipeline runs")
                print()
        else:
            print(f"\t{'No resources available' if error_message is None else error_message}")

    def __process_single_element(self, element: Dict, element_type: str) -> Dict:
        if element_type == 'pipeline':
            pipeline_data = {
                'id': element.get('_id', ''), 'pipeline_name': element.get('pipelineName', ''),
                'image_name': element.get('dockerImageTag', ''),
                'pipeline_runs': element.get('pipeline_runs', []),
                'created_at': element.get('createdAt', ''),
                'plans': [
                    self._plan.get_filtered_details(
                        plan_id=run_param['planId'], fields_req=['id', 'name']
                    ) for run_param in element['runParams']
                ]
            }

            if element.get('namespaceId', False) and element['namespaceId'].get('name', False):
                pipeline_data['namespace'] = element['namespaceId']['name']

            if element.get('addedBy', False) and element['addedBy'].get('email', False):
                pipeline_data['added_by'] = element['addedBy']['email']

            if element.get('organisationId', False) and element['organisationId'].get('name', False):
                pipeline_data['organisation'] = element['organisationId']['name']

            return pipeline_data

        if element_type == 'pipeline_runs':
            return {
                'id': element.get('_id', ''), 'name': element.get('name', ''), 'status': element.get('status', ''),
                'start_time': element.get('startTime', ''), 'end_time': element.get('endTime', '')
            }

    def __get_pipelines_runs(self, ai_pipeline_id: str):
        url = f"{self._api_auth.app_url}/api/v1/pipelinerun"
        response = requests.get(
            url, headers={'Content-Type': 'application/json'}, auth=self._api_auth.get_api_creds(),
            params={"pipelineId": ai_pipeline_id}
        )

        data_retrieval_success = response.status_code == 200 and response.json()['success']

        if not data_retrieval_success:
            api_error(
                status_code=response.status_code,
                message=f"Unable to fetch pipeline runs information for pipeline: {ai_pipeline_id}. \nReceived response: {response.text}"
            )
        return list(map(
            lambda data: self.__process_single_element(data, element_type='pipeline_runs'), response.json()['data']
        ))

    def __process_response(
            self,
            response: requests.Response, return_data: bool = True,
            raise_exception: bool = True, error_message: str = None, check_runs: bool = True
    ) -> Union[List[Dict], Dict, bool, None]:
        ai_pipeline_data = []
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
            for data in response.json()['data']:
                if check_runs:
                    data['pipeline_runs'] = self.__get_pipelines_runs(ai_pipeline_id=data['_id'])
                ai_pipeline_data.append(self.__process_single_element(data, element_type='pipeline'))

        return ai_pipeline_data

    def __get(
            self,
            state: str = 'ready', return_data: bool = True, raise_exception: bool = True, error_message: str = None,
            check_runs: bool = True
    ):
        if state is None:
            raise ValueError("state cannot be None")

        if type(state) is not str:
            raise TypeError('state can only be of type String')

        if state not in ['created', 'ready']:
            raise ValueError(f"state given: {state}. Acceptable value on of these: ['created', 'ready']")

        url = f"{self._api_auth.app_url}/api/v1/pipeline"
        response = requests.get(
            url, headers={'Content-Type': 'application/json'}, auth=self._api_auth.get_api_creds(),
            params={"state": state}
        )

        return self.__process_response(
            response=response, return_data=return_data, raise_exception=raise_exception,
            error_message=error_message, check_runs=check_runs
        )

    def _create(self, ai_pipeline_name: str, ai_pipeline_plan_id: str, datacenter_id: str, namespace_id: str):
        validate_ai_pipeline_name(ai_pipeline_name=ai_pipeline_name)

        image_version = int(time.time())

        image_name = f"{DOCKER_HUB_URL}/{'-'.join(ai_pipeline_name.strip().split(' '))}:{image_version}".lower()

        response = requests.post(
            f"{self._api_auth.app_url}/api/v1/pipeline/",
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                "pipelineName": ai_pipeline_name,
                "planId": [ai_pipeline_plan_id],
                "namespaceId": namespace_id,
                "yamlString": "from",
                "platform": [datacenter_id],
                "env": [],
                "args": [],
                "dockerImageTag": image_name
            }),
            auth=self._api_auth.get_api_creds()
        )

        if response.status_code == 200 and response.json()['success']:
            return response.json()['data']['_id'], image_name

        api_error(
            status_code=response.status_code,
            message=f"Unable to create AI-Pipeline.\nMessage from server: {response.text}"
        )

    def validate(self, image_name: str, state: str) -> bool:
        if image_name is None:
            raise ValueError("image_name cannot be None")

        if type(image_name) is not str:
            raise TypeError('image_name can only be of type String')

        if image_name.strip() == "":
            raise ValueError("image_name cannot be empty")

        ai_pipeline_data = self.__get(
            state=state, return_data=True, raise_exception=False, error_message=None, check_runs=False
        )

        return image_name.strip() in [_ai_pipeline['image_name'] for _ai_pipeline in ai_pipeline_data]

    def create_and_spawn(
            self, ai_pipeline_name: str, ai_pipeline_folder_path: str, caas_plan_id: str, ai_pipeline_plan_id: str,
            namespace_id: str
    ):
        self._namespace.validate_id(namespace_id=namespace_id, raise_exception=True)
        datacenter_id = self._validate_plan_and_get_datacenter(ai_pipeline_plan_id, PLAN_TYPE_MICROSERVICE)
        caas_datacenter_id = self._validate_plan_and_get_datacenter(caas_plan_id, PLAN_TYPE_CAAS)

        if caas_datacenter_id != datacenter_id:
            raise ValueError("CaaS plan and AI-Pipeline plan should belong to the same Datacenter.")

        model_zipfile_path = self._prepare_model_zip(model_folder_path=Path(ai_pipeline_folder_path))
        presigned_url = self._upload_file_to_datalake(file_name=model_zipfile_path)
        ai_pipeline_id, image_name = self._create(
            ai_pipeline_name.strip(), ai_pipeline_plan_id, datacenter_id, namespace_id
        )

        self._call_containerization_service(
            presigned_get_url=presigned_url, image_name=image_name, file_name=model_zipfile_path.name,
            image_id=ai_pipeline_id, namespace_id=namespace_id, deployment_name=ai_pipeline_name.strip(),
            datacenter_ids=[datacenter_id], deployment_type='pipeline', autodeploy=True, plan_id=[ai_pipeline_plan_id],
            caas_plan_id=caas_plan_id,
            error_msg="""
            Unable to create AI-Pipeline. Auto-Deploy: Error in Containerization or Spawning.
            Message from server:
            \t{response_text}
            """
        )

        print(
            f"""
            \nSuccessfully uploaded the Model folder | Filename: {model_zipfile_path.name}, Image Name: {image_name}
            \nAI-Pipeline will be spawned shortly
            """
        )

        return image_name

    def create(
            self, ai_pipeline_name: str, ai_pipeline_folder_path: str, caas_plan_id: str, ai_pipeline_plan_id: str,
            namespace_id: str
    ):
        self._namespace.validate_id(namespace_id=namespace_id, raise_exception=True)
        datacenter_id = self._validate_plan_and_get_datacenter(ai_pipeline_plan_id, PLAN_TYPE_MICROSERVICE)
        caas_datacenter_id = self._validate_plan_and_get_datacenter(caas_plan_id, PLAN_TYPE_CAAS)

        if caas_datacenter_id != datacenter_id:
            raise ValueError("CaaS plan and AI-Pipeline plan should belong to the same Datacenter.")

        model_zipfile_path = self._prepare_model_zip(model_folder_path=Path(ai_pipeline_folder_path))
        presigned_url = self._upload_file_to_datalake(file_name=model_zipfile_path)
        ai_pipeline_id, image_name = self._create(
            ai_pipeline_name.strip(), ai_pipeline_plan_id, datacenter_id, namespace_id
        )

        self._call_containerization_service(
            presigned_get_url=presigned_url, image_name=image_name, file_name=model_zipfile_path.name,
            image_id=ai_pipeline_id, namespace_id=namespace_id, deployment_name=ai_pipeline_name.strip(),
            datacenter_ids=[datacenter_id], deployment_type='pipeline', autodeploy=False, plan_id=[ai_pipeline_plan_id],
            caas_plan_id=caas_plan_id,
            error_msg="""
                    Unable to create AI-Pipeline. Auto-Deploy: Error in Containerization or Spawning.
                    Message from server:
                    \t{response_text}
                    """
        )

        print(
            f"Created AI-Pipeline with image name: {image_name}. Please use spawn() with {image_name} image_name after the deployment is ready. Please check your email to know the deployment status."
        )
        return image_name

    def spawn(
            self, ai_pipeline_plan_id: str, namespace_id: str, ai_pipeline_image_name: str
    ):
        self._namespace.validate_id(namespace_id=namespace_id, raise_exception=True)
        datacenter_id = self._validate_plan_and_get_datacenter(ai_pipeline_plan_id, PLAN_TYPE_MICROSERVICE)

        if not self.validate(image_name=ai_pipeline_image_name, state="created"):
            raise ValueError(NO_AI_PIPELINE_IMAGE_NAME.format(image_name=ai_pipeline_image_name))

        image_name = ai_pipeline_image_name.strip()
        ai_pipeline_name = image_name.split('/')[-1]

        response = requests.post(
            f"{self._api_auth.app_url}/api/v1/system/crosscloud",
            headers={'Content-Type': 'application/json'},
            auth=self._api_auth.get_api_creds(),
            data=json.dumps({
                "deploymentName": ai_pipeline_name,
                "planId": [ai_pipeline_plan_id],
                "namespaceId": namespace_id,
                "platform": [datacenter_id],
                "imageName": image_name,
                "deploymentType": "pipeline"
            })
        )

        if response.status_code == 200 and response.json()['success']:
            print(f"Deployment {ai_pipeline_name} created. Please visit: {self._api_auth.app_url}/app/workspace")
            return response.json()['success']

        api_error(
            status_code=response.status_code, message=f"""
            Unable to spawn the AI-Pipeline with image name {image_name}.
            Message from server:
            \t{response.text}
            """
        )

    def get_all(self, state: str = 'ready', print_stdout: bool = True) -> List[Dict]:
        ai_pipelines_data = self.__get(
            state=state, return_data=True, raise_exception=False,
            error_message=NO_AI_PIPELINE_STATE.format(state=state), check_runs=True
        )
        if print_stdout:
            self.__print_info(
                ai_pipelines=ai_pipelines_data, state=state,
                error_message=NO_AI_PIPELINE_STATE.format(state=state)
            )

        return ai_pipelines_data
