import requests
from . import PLAN_TYPE_ORCHESTRATION
from .utils.errors import api_error
from .auth import APIAuth
from .plan import Plan
from .namespace import Namespace
from .base.base_service import ServiceSpawnBase
from .utils.validations import validate_orchestration_name, validate_orchestration_workers
from .utils.error_message import NO_ORCHESTRATIONS, NO_ORCHESTRATION_ID
from typing import List, Dict, Union


class Orchestration(ServiceSpawnBase):
    __slots__ = ['__plan', '__namespace']

    def __init__(self, api_auth: APIAuth):
        super().__init__(api_auth)
        self.__plan = Plan(api_auth=api_auth)
        self.__namespace = Namespace(api_auth=api_auth)

    @staticmethod
    def __print_info(orchestrations: List[Dict], error_message: str = None):
        print("Orchestrations:")
        if len(orchestrations) > 0:
            for idx, data in enumerate(orchestrations):
                print(f"\t{idx + 1}. {data['name']}")
                print(
                    f"\t\tid: {data['id']} | description: {data['description']} | default plan: {data['default_plan']} | added by: {data['added_by']['username']} ({data['added_by']['id']}) | organisation id: {data['organisation_id']} | is_public: {data['is_public']}"
                )
                print(f"\t\tPlans: {', '.join([p['name'] + ' (' + p['id'] + ')' for p in data['plans']])}")
                print()
        else:
            print("No resources available" if error_message is None else error_message)

    def __process_single_element(self, element: Dict) -> Dict:
        e = {
            'id': element.get('_id', None), 'name': element.get('name', None), 'description': element['description'],
            'organisation_id': element['organisationId'], 'is_public': element['isPublic'],
            'added_by': {
                'id': element['addedBy']['_id'], 'name': element['addedBy']['name'],
                'email': element['addedBy']['email'], 'username': element['addedBy']['username']
            },
            'plans': [
                self.__plan.get_filtered_details(plan_id=_plan['_id'], fields_req=['id', 'name']) for _plan in
                element['plans']
            ]
        }

        _default_plan = self.__plan.get_filtered_details(plan_id=element['defaultPlan']['_id'],
                                                         fields_req=['id', 'name'])

        e['default_plan'] = f"{_default_plan['name']} ({_default_plan['id']})"

        return e

    def __process_response(
            self,
            response: requests.Response, return_data: bool = True,
            raise_exception: bool = True, error_message: str = None,
    ) -> Union[List[Dict], Dict, bool, None]:
        orchestration_data = None
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
            orchestration_data = self.__process_single_element(__resp_data)
        elif type(__resp_data) == list:
            orchestration_data = list(map(lambda data: self.__process_single_element(data), __resp_data))

        return orchestration_data

    @staticmethod
    def __basic_id_validation(resource_id: str):
        if type(resource_id) is not str:
            raise TypeError(f'orchestration_id can only be of type String')
        if resource_id.strip() == '':
            raise ValueError(f'orchestration_id cannot empty')

    def __get(
            self, resource_id: str = None, return_data: bool = True,
            raise_exception: bool = True, error_message: str = None,
    ) -> Union[List[Dict], Dict, bool, None]:
        __base_url = f"{self._api_auth.app_url}/api/v1/k8sAddons"

        if resource_id is None:
            response = requests.get(
                __base_url, headers={'Content-Type': 'application/json'},
                auth=self._api_auth.get_api_creds()
            )
        else:
            self.__basic_id_validation(resource_id=resource_id)
            response = requests.get(
                f"{__base_url}/{resource_id.strip()}", headers={'Content-Type': 'application/json'},
                auth=self._api_auth.get_api_creds()
            )

        return self.__process_response(
            response=response, return_data=return_data, raise_exception=raise_exception, error_message=error_message
        )

    def validate_id(self, orchestration_id: str, raise_exception: bool = False):
        if orchestration_id is None or orchestration_id == "":
            if raise_exception:
                raise ValueError("orchestration_id cannot be empty or None")
            return False

        return self.__get(
            resource_id=orchestration_id, return_data=False, raise_exception=raise_exception,
            error_message=NO_ORCHESTRATION_ID.format(orchestration_id=orchestration_id)
        )

    def get_by_id(self, orchestration_id: str, print_stdout: bool = True) -> Dict:
        if orchestration_id is None or orchestration_id == "":
            raise ValueError("orchestration_id cannot be empty or None")

        err_msg = NO_ORCHESTRATION_ID.format(orchestration_id=orchestration_id)

        orchestration_data = self.__get(
            resource_id=orchestration_id, return_data=True,
            raise_exception=True, error_message=err_msg
        )

        if print_stdout:
            self.__print_info(orchestrations=[orchestration_data], error_message=err_msg)

        return orchestration_data

    def get_all(self, print_stdout: bool = True):
        orchestration_data = self.__get(
            resource_id=None, return_data=True,
            raise_exception=True, error_message=NO_ORCHESTRATIONS
        )

        if print_stdout:
            self.__print_info(orchestrations=orchestration_data)

        return orchestration_data

    def spawn(
            self,
            orchestration_id: str, plan_id: str, namespace_id: str,
            orchestration_name: str, min_workers: int, max_workers: int
    ):
        _orchestration_data = self.get_by_id(orchestration_id=orchestration_id, print_stdout=False)  # Get-data

        datacenter_id = self._validate_plan_and_get_datacenter(
            plan_id=plan_id, service_type=PLAN_TYPE_ORCHESTRATION,
            plans=list(map(lambda x: x.get('id', None), _orchestration_data['plans'])),
            err_msg=f"plan_id ({plan_id} not in available plans for orchestration ({orchestration_id})"
        )

        # datacenter_id = self._validate_plan_and_get_datacenter(ai_api_plan_id, PLAN_TYPE_ORCHESTRATION)
        self.__namespace.validate_id(namespace_id=namespace_id, raise_exception=True)
        validate_orchestration_name(orchestration_name=orchestration_name, raise_exception=True)
        validate_orchestration_workers(min_workers=min_workers, max_workers=max_workers, raise_exception=True)

        response = requests.post(
            f"{self._api_auth.app_url}/api/v1/spawnedK8sAddons/", headers={'Content-Type': 'application/json'},
            auth=self._api_auth.get_api_creds(),
            json={
                "orchestrationAddonId": orchestration_id, "planId": plan_id, "name": orchestration_name,
                "dataCenterId": datacenter_id, "namespaceId": namespace_id,
                "minWorkers": min_workers, "maxWorkers": max_workers,
                "kioskArray": None, "nodePreference": "NO PREFERENCE"
            }
        )

        if response.status_code == 201 and response.json()['success']:
            print(f"Successfully spawned `{orchestration_name}`. Please visit: {self._api_auth.app_url}/app/workspace")
            return True
        else:
            api_error(status_code=response.status_code, message=response.text)
