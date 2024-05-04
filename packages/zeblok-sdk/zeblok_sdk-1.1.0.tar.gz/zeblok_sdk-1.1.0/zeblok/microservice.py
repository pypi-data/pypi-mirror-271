from .auth import APIAuth
from .base.base_service import ServiceSpawnBase
from .plan import Plan
from .namespace import Namespace
from .utils.errors import api_error
from .utils.error_message import NO_MICROSERVICES, NO_MICROSERVICES_ID, INVALID_MICROSERVICE_DISPLAY_NAME
import requests
import json
from typing import List, Union, Dict
from . import PLAN_TYPE_MICROSERVICE
from .utils.validations import validate_microservice_name, validate_microservice_display_name, \
    validate_microservice_ports, validate_microservice_envs, validate_microservice_args


class MicroService(ServiceSpawnBase):
    def __init__(self, api_auth: APIAuth):
        super().__init__(api_auth)
        self.__plan = Plan(api_auth=api_auth)
        self.__namespace = Namespace(api_auth=api_auth)

    @staticmethod
    def __print_info(microservices: List[Dict], error_message: str = None):
        print("MicroServices:")
        if len(microservices) > 0:
            for idx, data in enumerate(microservices):
                print(f"\t{idx + 1}. {data['name']}")
                print(
                    f"\t\tid: {data['id']} | description: {data['description']} | added by: {data['added_by']} | organisation: {data['organisation']} | is_public: {data['is_public']}"
                )
                print(f"\t\tPlans: {', '.join([p['name'] + ' (' + p['id'] + ')' for p in data['plans']])}")
                print(f"\t\tDisplay Name: {', '.join(data['display_names'])}")
                print()
        else:
            print("No resources available" if error_message is None else error_message)

    @staticmethod
    def __process_single_element(element: Dict) -> Dict:
        e = {
            'id': element.get('_id', None), 'name': element.get('name', None),
            'description': element.get('description', None),
            'is_public': element.get('isPublic', None),
            'added_by': None if element.get('addedBy', None) is None else element['addedBy'].get('name', None),
            'organisation': None if element.get('organisationId', None) is None else element['organisationId'].get(
                'name', None),
            'plans': None if element.get('plans', None) is None else list(
                map(lambda x: {'id': x.get('_id', None), 'name': x.get('planName', None)}, element['plans'])),
            'display_names': None if element.get('imageTag', None) is None else list(
                map(lambda x: x.get('displayName', ""), element['imageTag']))
        }

        return e

    def __process_response(
            self,
            response: requests.Response, return_data: bool = True,
            raise_exception: bool = True, error_message: str = None,
    ) -> Union[List[Dict], Dict, bool, None]:
        microservice_data = None
        data_retrieval_success = response.status_code == 200 and response.json()['success']

        if not return_data and not raise_exception:
            return True if data_retrieval_success else False

        if not data_retrieval_success and raise_exception:
            api_error(
                status_code=response.status_code,
                message=response.text if error_message is None else error_message
            )

        __resp_data = response.json()['data']
        if type(__resp_data) == dict:
            microservice_data = self.__process_single_element(__resp_data)
        elif type(__resp_data) == list:
            microservice_data = list(map(lambda data: self.__process_single_element(data), __resp_data))

        return microservice_data

    @staticmethod
    def __basic_id_validation(resource_id: str):
        if type(resource_id) is not str:
            raise TypeError(f'microservice_id can only be of type String')
        if resource_id.strip() == '':
            raise ValueError(f'microservice_id cannot empty')

    def __get(
            self, resource_id: str = None, return_data: bool = True,
            raise_exception: bool = True, error_message: str = None,
    ) -> Union[List[Dict], Dict, bool, None]:
        __base_url = f"{self._api_auth.app_url}/api/v1/microservices"

        if resource_id is None:
            response = requests.get(
                __base_url + "?isActive=true", headers={'Content-Type': 'application/json'},
                auth=self._api_auth.get_api_creds()
            )
        else:
            self.__basic_id_validation(resource_id=resource_id)
            response = requests.get(
                f"{__base_url}/{resource_id.strip()}?isActive=true", headers={'Content-Type': 'application/json'},
                auth=self._api_auth.get_api_creds()
            )

        return self.__process_response(
            response=response, return_data=return_data, raise_exception=raise_exception, error_message=error_message
        )

    def validate_id(self, microservice_id: str, raise_exception: bool = False):
        if microservice_id is None:
            if raise_exception:
                raise ValueError("microservice_id cannot be None")
            return False

        return self.__get(
            resource_id=microservice_id, return_data=False, raise_exception=raise_exception,
            error_message=NO_MICROSERVICES_ID.format(microservice_id=microservice_id)
        )

    def get_by_id(self, microservice_id: str, print_stdout: bool = True) -> Dict:
        if microservice_id is None or microservice_id == "":
            raise ValueError("microservice_id cannot be empty or None")

        err_msg = NO_MICROSERVICES_ID.format(microservice_id=microservice_id)

        microservice_data = self.__get(
            resource_id=microservice_id, return_data=True,
            raise_exception=True, error_message=err_msg
        )

        if print_stdout:
            self.__print_info(microservices=[microservice_data], error_message=err_msg)

        return microservice_data

    def get_all(self, print_stdout: bool = True):
        microservice_data = self.__get(
            resource_id=None, return_data=True,
            raise_exception=True, error_message=NO_MICROSERVICES
        )

        if print_stdout:
            self.__print_info(microservices=microservice_data, error_message=NO_MICROSERVICES)

        return microservice_data

    def spawn(
            self, display_name: str, microservice_id: str, plan_id: str, microservice_name: str,
            namespace_id: str, envs: List[Dict] = [], ports: List[Dict] = [], args: List[Dict] = [],
            command: str = None
    ):
        self.__namespace.validate_id(namespace_id=namespace_id, raise_exception=True)

        _microservice_data = self.get_by_id(microservice_id=microservice_id, print_stdout=False)

        datacenter_id = self._validate_plan_and_get_datacenter(
            plan_id=plan_id, service_type=PLAN_TYPE_MICROSERVICE,
            plans=list(map(lambda x: x.get('id', None), _microservice_data['plans'])),
            err_msg=f"plan_id ({plan_id} not in available plans for microservice ({microservice_id})"
        )

        validate_microservice_display_name(
            display_name, _microservice_data['display_names'],
            err_msg=INVALID_MICROSERVICE_DISPLAY_NAME.format(microservice_id=microservice_id, display_name=display_name)
        )

        validate_microservice_name(microservice_name)

        validate_microservice_ports(ports)

        validate_microservice_envs(envs)

        validate_microservice_args(args)

        if command is not None and type(command) is not str:
            raise TypeError("command can only be of type String")

        response = requests.post(
            f"{self._api_auth.app_url}/api/v1/spawnedservices",
            headers={'Content-Type': 'application/json'},
            auth=self._api_auth.get_api_creds(),
            data=json.dumps({
                "microserviceId": microservice_id,
                "dockerImageVersion": {"displayName": display_name.strip()},
                "dataCenterId": datacenter_id,
                "kioskArray": None,
                "planId": plan_id,
                "namespaceId": namespace_id,
                "nodePreference": "NO PREFERENCE",
                "parameters": {
                    "ports": ports,
                    "envs": envs,
                    "args": args,
                    "command": command,
                    "volumePath": None
                },
                "name": microservice_name.strip()
            })
        )

        if response.status_code == 201 and response.json()['success']:
            print(f"Successfully spawned `{microservice_name}`. Please visit: {self._api_auth.app_url}/app/workspace")
            return True
        else:
            api_error(status_code=response.status_code, message=response.text)
