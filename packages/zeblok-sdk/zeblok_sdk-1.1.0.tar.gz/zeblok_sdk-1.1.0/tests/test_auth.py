import pytest
from zeblok.auth import Auth
from zeblok.errors import InvalidCredentialsError, AuthenticationError, ServerError, InvalidURL


@pytest.fixture()
def auth_data():
    return {'username': 'temp_username', 'password': 'temp_password', 'base_url': 'app.zbl-aws.zeblok.com'}


class TestAuthInstanceCreation:
    def test_invalid_int_username(self, auth_data):
        with pytest.raises(expected_exception=InvalidCredentialsError, match='username can only be of type String'):
            auth_data.pop('username')
            Auth(username=1, **auth_data)

    def test_invalid_int_password(self, auth_data):
        with pytest.raises(expected_exception=InvalidCredentialsError, match='password can only be of type String'):
            auth_data.pop('password')
            Auth(password=1, **auth_data)

    def test_invalid_int_base_url(self, auth_data):
        with pytest.raises(expected_exception=InvalidURL, match='base_url can only be of type String'):
            auth_data.pop('base_url')
            Auth(base_url=1, **auth_data)

    def test_invalid_empty_username(self, auth_data):
        with pytest.raises(expected_exception=InvalidCredentialsError, match='username cannot empty'):
            auth_data.pop('username')
            Auth(username='', **auth_data)

    def test_invalid_empty_password(self, auth_data):
        with pytest.raises(expected_exception=InvalidCredentialsError, match='password cannot empty'):
            auth_data.pop('password')
            Auth(password='', **auth_data)

    def test_invalid_empty_base_url(self, auth_data):
        with pytest.raises(expected_exception=InvalidURL, match='base_url cannot empty'):
            auth_data.pop('base_url')
            Auth(base_url='', **auth_data)


class TestBasicMemberFunctions:
    def test_get_username(self, auth_data):
        assert Auth(**auth_data).get_username() == auth_data['username']

    def test_get_password(self, auth_data):
        assert Auth(**auth_data).get_password() == auth_data['password']


class TestTokenMechanism:
    def test_get_token_from_local(self, auth_data, monkeypatch):
        temp_token = 'temp_token'
        temp_auth_obj = Auth(**auth_data)
        monkeypatch.setattr(temp_auth_obj, '_Auth__token', temp_token)
        assert temp_auth_obj.get_token() == temp_token

    def test_get_token_from_server(self, auth_data, monkeypatch):
        import requests
        temp_token = 'temp_token'

        class MockResponse:
            def __init__(self, url, headers, data):
                self.status_code = 200

            @staticmethod
            def json():
                return {'data': temp_token}

        monkeypatch.setattr(requests, 'post', MockResponse)
        assert Auth(**auth_data).get_token() == "Bearer " + temp_token

    def test_get_token_wrong_credentials(self, auth_data, monkeypatch):
        import requests
        error_message = 'wrong_credentials'

        class MockResponse:
            def __init__(self, url, headers, data):
                self.status_code = 401

            @staticmethod
            def json():
                return {'message': error_message}

        monkeypatch.setattr(requests, 'post', MockResponse)
        with pytest.raises(expected_exception=AuthenticationError, match=error_message):
            Auth(**auth_data).get_token()

    def test_get_token_unknown_error(self, auth_data, monkeypatch):
        import requests

        class MockResponse:
            def __init__(self, url, headers, data):
                self.status_code = 500

        monkeypatch.setattr(requests, 'post', MockResponse)
        with pytest.raises(expected_exception=ServerError,
                           match=f"Status code = {MockResponse('', '', '').status_code}"):
            Auth(**auth_data).get_token()
