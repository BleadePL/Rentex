# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.empty import Empty  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.models.inline_response4001 import InlineResponse4001  # noqa: E501
from swagger_server.models.login_login_body import LoginLoginBody  # noqa: E501
from swagger_server.models.register_data import RegisterData  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLoginController(BaseTestCase):
    """LoginController integration test stubs"""

    def test_login_activate_post(self):
        """Test case for login_activate_post

        Aktywacja konta
        """
        query_string = [('activation_token', 'activation_token_example')]
        headers = [('session_token', 56)]
        response = self.client.open(
            '//login/activate',
            method='POST',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login_login_post(self):
        """Test case for login_login_post

        Loguje do systemu
        """
        body = LoginLoginBody()
        response = self.client.open(
            '//login/login',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login_logout_post(self):
        """Test case for login_logout_post

        Wyloguj z systemu
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//login/logout',
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login_register_post(self):
        """Test case for login_register_post

        Rejestruje uzytkownika do systemu
        """
        body = RegisterData()
        response = self.client.open(
            '//login/register',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login_send_token_post(self):
        """Test case for login_send_token_post

        Wysyla token aktywacyjny
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//login/sendToken',
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login_status_get(self):
        """Test case for login_status_get

        Pobierz status konta
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//login/status',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login_upload_photos_post(self):
        """Test case for login_upload_photos_post

        Upload images!
        """
        body = Object()
        query_string = [('side', 'side_example')]
        headers = [('session_token', 56)]
        response = self.client.open(
            '//login/uploadPhotos',
            method='POST',
            data=json.dumps(body),
            headers=headers,
            content_type='image/*',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest

    unittest.main()
