from abc import abstractmethod

from ..auth import APIAuth
from .base_zbl import ZBLBase
from typing import Union, List
from ..plan import Plan
from ..namespace import Namespace
from ..utils.error_message import INCOMPATIBLE_SERVICE_PLAN_ID, PLAN_ID_TYPE_UNAVAILABLE, PLAN_ID_DATACENTER_UNAVAILABLE


class ServiceSpawnBase(ZBLBase):
    def __init__(self, api_auth: APIAuth):
        super().__init__(api_auth)
        self._plan = Plan(api_auth)
        self._namespace = Namespace(api_auth)

    @abstractmethod
    def spawn(self, *args, **kwargs):
        pass

    def _validate_plan_and_get_datacenter(
            self, plan_id: str, service_type: Union[str, None], plans: Union[List[str], None] = None,
            err_msg: str = None
    ):
        _data = self._plan.get_filtered_details(plan_id=plan_id, fields_req=['data_center', 'type'])

        if _data.get('type', None) is None:
            raise ValueError(PLAN_ID_TYPE_UNAVAILABLE.format(plan_id=plan_id))

        if _data.get('data_center', None) is None:
            raise ValueError(PLAN_ID_DATACENTER_UNAVAILABLE.format(plan_id=plan_id))

        if service_type is not None and _data['type'] != service_type:
            raise ValueError(INCOMPATIBLE_SERVICE_PLAN_ID.format(
                plan_id=plan_id, service_type_1=_data['type'], service_type_2=service_type
            ))

        if plans is not None and plan_id not in plans:
            raise ValueError(err_msg)

        return _data['data_center']['id']
