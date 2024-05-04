import pathlib
import os
import pytest
from zeblok.namspace import Namespace
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
def namespace_data():
    return Namespace(base_url='temp_base_url')


class MockServerErrorResponse:
    def __init__(self, url, headers):
        self.status_code = 500
        self.text = TEMP_ERROR_TEXT


class MockAuthenticationErrorResponse:
    def __init__(self, url, headers):
        self.status_code = 401
        self.text = ''


class TestGetAllNamespaces:
    def test_random_error(self, namespace_data, monkeypatch):
        monkeypatch.setattr(requests, 'get', MockServerErrorResponse)
        with pytest.raises(expected_exception=ServerError, match=TEMP_ERROR_TEXT):
            namespace_data.get_all_namespaces(token=TEST_TOKEN)

    def test_invalid_token(self, namespace_data, monkeypatch):
        monkeypatch.setattr(requests, 'get', MockAuthenticationErrorResponse)
        with pytest.raises(expected_exception=AuthenticationError, match=AUTHENTICATION_MESSAGE):
            namespace_data.get_all_namespaces(token=TEST_TOKEN)

    def test_success_with_print(self, capsys, namespace_data, monkeypatch):
        class MockResponse:
            def __init__(self, url, headers):
                self.status_code = 200

            @staticmethod
            def json():
                return {'success': True, 'data': [
                    {'_id': 'id_1', 'name': 'namespace1'},
                    {'_id': 'id_2', 'name': 'namespace2'}
                ]}

        monkeypatch.setattr(requests, 'get', MockResponse)

        assert namespace_data.get_all_namespaces(token=TEST_TOKEN) == [{'id': 'id_1', 'name': 'namespace1'},
                                                                  {'id': 'id_2', 'name': 'namespace2'}]

        captured = capsys.readouterr()
        assert captured.out == "Namespaces:\n\t1. name: namespace1 | id: id_1\n\t2. name: namespace2 | id: id_2\n"

    def test_success_without_print(self, namespace_data, monkeypatch):
        class MockResponse:
            def __init__(self, url, headers):
                self.status_code = 200

            @staticmethod
            def json():
                return {'success': True, 'data': [
                    {'_id': 'id_1', 'name': 'namespace1'},
                    {'_id': 'id_2', 'name': 'namespace2'}
                ]}

        monkeypatch.setattr(requests, 'get', MockResponse)
        assert namespace_data.get_all_namespaces(token=TEST_TOKEN, print_stdout=False) == [
            {'id': 'id_1', 'name': 'namespace1'},
            {'id': 'id_2', 'name': 'namespace2'}]
