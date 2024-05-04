from .utils.errors import api_error
from .base.base_zbl import ZBLBase
from .auth import APIAuth
import requests
from typing import List, Dict, Union
from .utils.error_message import NO_PLAN_ID, NO_PLANS


class Plan(ZBLBase):
    def __int__(self, api_auth: APIAuth):
        super().__init__(api_auth)

    @staticmethod
    def __process_single_element(element: Dict) -> Dict:
        e = {
            'id': element.get('_id', ''), 'name': element.get('planName', ''),
            'type': element.get('type', ''), 'price': element.get('price', ''),
            'currency': element.get('currency', ''), 'resources': element.get('resources', ''),
            'is_public': element.get('isPublic', '')
        }

        if element.get('dataCenterId', False):
            e['data_center'] = {
                'id': element['dataCenterId'].get('_id', ''),
                'name': element['dataCenterId'].get('name', '')
            }
        else:
            e['data_center'] = {'id': '', 'name': ''}

        if element.get('organisationId', False):
            e['organization'] = {
                'id': element['organisationId'].get('_id', ''),
                'name': element['organisationId'].get('name', '')
            }
        else:
            e['organization'] = {'id': '', 'name': ''}

        if element['addedBy'] is not None:
            e['added_by'] = element['addedBy']['username']

        return e

    @staticmethod
    def __print_info(plans: List[Dict], error_message: str = None):
        print("Plans:")
        if len(plans) > 0:
            for idx, data in enumerate(plans):
                print(f"\t{idx + 1}. {data['name']}")
                print(
                    f"\t\tid: {data['id']} | type: {data['type']} | price: {data['currency']} {data['price']} | added_by: {data.get('added_by', None)} | is_public: {data['is_public']}"
                )
                print(
                    f"\t\tResources = CPU: {data['resources']['CPU']} vCPU | #GPUs: {data['resources']['GPU']} | Memory: {data['resources']['memory']} GB | Storage: {data['resources']['storage']} GB"
                )
                print(f"\t\tData Center = id: {data['data_center']['id']} | name: {data['data_center']['name']}")
                print(f"\t\tOrganization = id: {data['organization']['id']} | name: {data['organization']['name']}")
                print()
        else:
            print("No resources available" if error_message is None else error_message)

    @classmethod
    def __process_response(
            cls,
            response: requests.Response, return_data: bool = True,
            raise_exception: bool = True, error_message: str = None,
    ) -> Union[List[Dict], Dict, bool, None]:
        plan_data = []
        data_retrieval_success = response.status_code == 200 and response.json()['success'] and response.json()[
            'totalCount'] > 0

        if not return_data and not raise_exception:
            return data_retrieval_success

        if not data_retrieval_success and raise_exception:
            api_error(
                status_code=response.status_code,
                message=response.text if error_message is None else error_message
            )

        if data_retrieval_success:
            __resp_data = response.json()['data']
            if type(__resp_data) == dict:
                plan_data = cls.__process_single_element(__resp_data)
            elif type(__resp_data) == list:
                plan_data = list(map(lambda data: cls.__process_single_element(data), __resp_data))

        return plan_data

    @staticmethod
    def __basic_id_validation(resource_id: str):
        if type(resource_id) is not str:
            raise TypeError(f'resource_id can only be of type String')
        if resource_id.strip() == '':
            raise ValueError(f'resource_id cannot empty')

    def __get(
            self, resource_id: str = None, return_data: bool = True,
            raise_exception: bool = True, error_message: str = None,
    ) -> Union[List[Dict], Dict, bool, None]:
        __base_url = f"{self._api_auth.app_url}/api/v1/plans"

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

    def validate_id(self, plan_id: str, raise_exception: bool = False):
        if plan_id is None:
            if raise_exception:
                raise ValueError("ai_api_plan_id cannot be None")
            else:
                return False

        return self.__get(
            resource_id=plan_id, return_data=False,
            raise_exception=raise_exception, error_message=NO_PLAN_ID.format(plan_id=plan_id)
        )

    def get_by_id(self, plan_id: str, print_stdout: bool = True) -> Dict:
        if plan_id is None:
            raise ValueError("plan_id cannot be None")

        err_msg = NO_PLAN_ID.format(plan_id=plan_id)

        plan_data = self.__get(
            resource_id=plan_id, return_data=True,
            raise_exception=True, error_message=err_msg
        )

        if print_stdout:
            self.__print_info(plans=[plan_data], error_message=err_msg)

        return plan_data

    def get_filtered_details(self, plan_id: str, fields_req: List[str]) -> Dict:
        """
        - Validates ai_api_plan_id

        :param plan_id:
        :param fields_req: # TODO Mention possible fields
        :return:
        """
        plan_data = self.get_by_id(plan_id=plan_id, print_stdout=False)
        return {key: plan_data.get(key, None) for key in fields_req}

    def get_all(self, print_stdout: bool = True) -> List[Dict]:
        plan_data = self.__get(
            resource_id=None, return_data=True, raise_exception=True, error_message=NO_PLANS
        )

        if print_stdout:
            self.__print_info(plans=plan_data, error_message=NO_PLANS)

        return plan_data
