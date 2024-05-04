import pathlib
import os
import pytest
from zeblok.orchestration import Orchestration
from zeblok.errors import InvalidCredentialsError, AuthenticationError, ServerError, ModelDeploymentError, \
    InvalidModelFolder, FileUploadError
import requests

AUTHENTICATION_MESSAGE = 'User not authenticated. Please check your token or api_access_key or api_access_secret'
TEMP_ERROR_TEXT = 'error_text'
SECRET_KEY = 'some_secret_key'
USERNAME = 'temp_username'
MODEL_FOLDER_PATH = 'temp_model_folder_path'
TEST_TOKEN = 'Bearer temp-token'


@pytest.fixture
def orchestration_data():
    return Orchestration(base_url='temp_base_url')


class MockServerErrorResponse:
    def __init__(self, url, headers):
        self.status_code = 500
        self.text = TEMP_ERROR_TEXT


class MockAuthenticationErrorResponse:
    def __init__(self, url, headers):
        self.status_code = 401
        self.text = ''


class TestGetAllOrchestrations:
    def test_random_error(self, orchestration_data, monkeypatch):
        monkeypatch.setattr(requests, 'get', MockServerErrorResponse)
        with pytest.raises(expected_exception=ServerError, match=TEMP_ERROR_TEXT):
            orchestration_data.get_all_orchestrations(token=TEST_TOKEN)

    def test_invalid_token(self, orchestration_data, monkeypatch):
        monkeypatch.setattr(requests, 'get', MockAuthenticationErrorResponse)
        with pytest.raises(expected_exception=AuthenticationError, match=AUTHENTICATION_MESSAGE):
            orchestration_data.get_all_orchestrations(token=TEST_TOKEN)

    @pytest.mark.skip()
    def test_success_with_print(self, capsys, orchestration_data, monkeypatch):
        class MockResponse:
            def __init__(self, url, headers):
                self.status_code = 200

            @staticmethod
            def json():
                return {
                    "success": True, "totalCount": 2, "data": [
                        {"_id": "plan_id_1", "planName": "plan_1", "price": 10, "currency": "USD",
                         "resources": {"CPU": 1, "GPU": 1, "memory": 1, "storage": 1, "workers": 0},
                         "dataCenterId": {"_id": "data_center_id_1", "name": "data_center_1"},
                         "addedBy": None, "isPublic": True, "type": "Ai-MicroService",
                         "organisationId": {"_id": "organisation_id_1", "name": "organisation_1"},
                         },
                        {"_id": "plan_id_2", "planName": "plan_2", "price": 20, "currency": "USD",
                         "resources": {"CPU": 2, "GPU": 2, "memory": 2, "storage": 2, "workers": 0},
                         "dataCenterId": {"_id": "data_center_id_2", "name": "data_center_2"},
                         "addedBy": {
                             "_id": "username_id_1", "name": "FName LName",
                             "email": "fname.lname@domain.com", "username": "username_1"
                         },
                         "isPublic": False, "type": "Ai-MicroService",
                         "organisationId": {"_id": "organisation_id_2", "name": "organisation_2"},
                         },
                    ]
                }

        monkeypatch.setattr(requests, 'get', MockResponse)

        assert orchestration_data.get_all_orchestrations(token=TEST_TOKEN, print_stdout=True) == [
            {"id": "plan_id_1", "name": "plan_1", "price": 10, "currency": "USD", "is_public": True,
             "resources": {"CPU": 1, "GPU": 1, "memory": 1, "storage": 1, "workers": 0},
             "data_center": {"id": "data_center_id_1", "name": "data_center_1"},
             "type": "Ai-MicroService",
             "organization": {"id": "organisation_id_1", "name": "organisation_1"},
             },
            {"id": "plan_id_2", "name": "plan_2", "price": 20, "currency": "USD", "is_public": False,
             "resources": {"CPU": 2, "GPU": 2, "memory": 2, "storage": 2, "workers": 0},
             "data_center": {"id": "data_center_id_2", "name": "data_center_2"},
             "added_by": "username_1", "type": "Ai-MicroService",
             "organization": {"id": "organisation_id_2", "name": "organisation_2"},
             }
        ]

        captured = capsys.readouterr()
        assert captured.out == "Plans:\n\t1. plan_1\n\t\tid: plan_id_1 | type: Ai-MicroService | price: USD 10 | added_by: None | is_public: True\n\t\tResources = CPU: 1 vCPU | GPU: 1 GB | Memory: 1 GB | Storage: 1 GB | Workers: 0\n\t\tData Center = id: data_center_id_1 | name: data_center_1\n\t\tOrganization = id: organisation_id_1 | name: organisation_1\n\n\t2. plan_2\n\t\tid: plan_id_2 | type: Ai-MicroService | price: USD 20 | added_by: username_1 | is_public: False\n\t\tResources = CPU: 2 vCPU | GPU: 2 GB | Memory: 2 GB | Storage: 2 GB | Workers: 0\n\t\tData Center = id: data_center_id_2 | name: data_center_2\n\t\tOrganization = id: organisation_id_2 | name: organisation_2\n\n"

    def test_success_without_print(self, orchestration_data, monkeypatch):
        class MockResponse:
            def __init__(self, url, headers):
                self.status_code = 200

            @staticmethod
            def json():
                return {
                    "success": True, "totalCount": 2, "data": [
                        {
                            "_id": "orchestration_id_1", "name": "orchestration_1", "description": "description 1",
                            "addedBy": "username_id_1", "isPublic": False, "organisationId": "organisation_id_1",
                            "defaultPlan": "default_plan_1", "plans": ["plan_1", "plan_2"]
                         },
                        {
                            "_id": "orchestration_id_2", "name": "orchestration_2", "description": "description 2",
                            "addedBy": "username_id_2", "isPublic": True, "organisationId": "organisation_id_2",
                            "defaultPlan": "default_plan_2", "plans": ["plan_1", "plan_2", "plan_3"]
                         },
                    ]
                }

        monkeypatch.setattr(requests, 'get', MockResponse)

        assert orchestration_data.get_all_orchestrations(token=TEST_TOKEN, print_stdout=False) == [
            {"id": "plan_id_1", "name": "plan_1", "price": 10, "currency": "USD", "is_public": True,
             "resources": {"CPU": 1, "GPU": 1, "memory": 1, "storage": 1, "workers": 0},
             "data_center": {"id": "data_center_id_1", "name": "data_center_1"},
             "type": "Ai-MicroService",
             "organization": {"id": "organisation_id_1", "name": "organisation_1"},
             },
            {"id": "plan_id_2", "name": "plan_2", "price": 20, "currency": "USD", "is_public": False,
             "resources": {"CPU": 2, "GPU": 2, "memory": 2, "storage": 2, "workers": 0},
             "data_center": {"id": "data_center_id_2", "name": "data_center_2"},
             "added_by": "username_1", "type": "Ai-MicroService",
             "organization": {"id": "organisation_id_2", "name": "organisation_2"},
             }
        ]
