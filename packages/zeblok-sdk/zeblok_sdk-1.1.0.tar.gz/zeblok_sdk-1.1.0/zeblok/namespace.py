from .utils.errors import api_error
from .base.base_zbl import ZBLBase
from .auth import APIAuth
import requests
from typing import List, Dict, Union
from .utils.error_message import NO_NAMESPACES, NO_NAMESPACE_ID


class Namespace(ZBLBase):
    def __int__(self, api_auth: APIAuth):
        super().__init__(api_auth)

    @staticmethod
    def __process_single_element(element: Dict) -> Dict:
        return {'name': element.get('name', ''), 'id': element.get('_id', '')}

    @staticmethod
    def __print_info(namespaces: List[Dict], error_message: str = None):
        print("Namespaces:")
        if len(namespaces) > 0:
            for idx, data in enumerate(namespaces):
                print(f"\t{idx + 1}. name: {data['name']} | id: {data['id']}")
        else:
            print("No resources available" if error_message is None else error_message)

    @classmethod
    def __process_response(
            cls,
            response: requests.Response, return_data: bool = True,
            raise_exception: bool = True, error_message: str = None,
    ) -> Union[List[Dict], Dict, bool, None]:

        namespace_data = []
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
                cls.__process_single_element(__resp_data)
                namespace_data = {'name': __resp_data['name'], 'id': __resp_data['_id']}
            elif type(__resp_data) == list:
                namespace_data = list(map(lambda data: cls.__process_single_element(data), __resp_data))

        return namespace_data

    @staticmethod
    def __basic_id_validation(namespace_id: str):
        if type(namespace_id) is not str:
            raise TypeError('namespace_id can only be of type String')
        if namespace_id.strip() == '':
            raise ValueError('namespace_id cannot empty')

    def __get(
            self, resource_id: str = None, return_data: bool = True,
            raise_exception: bool = True, error_message: str = None,
    ) -> Union[List[Dict], Dict, bool, None]:
        __base_url = f"{self._api_auth.app_url}/api/v1/namespaces"

        if resource_id is None:
            response = requests.get(
                __base_url, headers={'Content-Type': 'application/json'},
                auth=self._api_auth.get_api_creds()
            )
        else:
            self.__basic_id_validation(namespace_id=resource_id)
            response = requests.get(
                f"{__base_url}/{resource_id.strip()}", headers={'Content-Type': 'application/json'},
                auth=self._api_auth.get_api_creds()
            )

        return self.__process_response(
            response=response, return_data=return_data, raise_exception=raise_exception, error_message=error_message
        )

    def validate_id(self, namespace_id: str, raise_exception: bool = False):
        if namespace_id is None:
            if raise_exception:
                raise ValueError("namespace_id cannot be None")
            else:
                return False

        return self.__get(
            resource_id=namespace_id, return_data=False,
            raise_exception=raise_exception,
            error_message=NO_NAMESPACE_ID.format(namespace_id=namespace_id)
        )

    def get_by_id(self, namespace_id: str, print_stdout: bool = True) -> Dict:
        if namespace_id is None:
            raise ValueError("namespace_id cannot be None")

        err_msg = NO_NAMESPACE_ID.format(namespace_id=namespace_id)

        namespace_data = self.__get(
            resource_id=namespace_id, return_data=True,
            raise_exception=True, error_message=err_msg
        )

        if print_stdout:
            self.__print_info(namespaces=[namespace_data], error_message=err_msg)

        return namespace_data

    def get_all(self, print_stdout: bool = True) -> List[Dict]:
        namespace_data = self.__get(
            resource_id=None, return_data=True, raise_exception=True, error_message=NO_NAMESPACES
        )

        if print_stdout:
            self.__print_info(namespaces=namespace_data)

        return namespace_data
