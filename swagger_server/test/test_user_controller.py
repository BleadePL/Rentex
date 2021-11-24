# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.credit_card import CreditCard  # noqa: E501
from swagger_server.models.empty import Empty  # noqa: E501
from swagger_server.models.gps_location import GPSLocation  # noqa: E501
from swagger_server.models.inline_response4002 import InlineResponse4002  # noqa: E501
from swagger_server.models.inline_response4003 import InlineResponse4003  # noqa: E501
from swagger_server.models.rental import Rental  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.user_cards_body import UserCardsBody  # noqa: E501
from swagger_server.models.user_changepasswd_body import UserChangepasswdBody  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_user_card_id_get(self):
        """Test case for user_card_id_get

        Info na temat konkretnej karty
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//user/card/{id}'.format(id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_cards_get(self):
        """Test case for user_cards_get

        Lista kart przypisanych do konta
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//user/cards',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_cards_post(self):
        """Test case for user_cards_post

        Dodaj karte do konta
        """
        body = UserCardsBody()
        headers = [('session_token', 56)]
        response = self.client.open(
            '//user/cards',
            method='POST',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_changepasswd_post(self):
        """Test case for user_changepasswd_post

        Zmien haslo
        """
        body = UserChangepasswdBody()
        headers = [('session_token', 56)]
        response = self.client.open(
            '//user/changepasswd',
            method='POST',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_details_get(self):
        """Test case for user_details_get

        Pobiera informacje o uzytkowniku
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//user/details',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_history_get(self):
        """Test case for user_history_get

        Zwraca historie wypozyczen
        """
        query_string = [('pagelength', 1),
                        ('startindex', 0)]
        headers = [('session_token', 56)]
        response = self.client.open(
            '//user/history',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_updatelocation_post(self):
        """Test case for user_updatelocation_post

        Updates user location
        """
        body = GPSLocation()
        headers = [('session_token', 56)]
        response = self.client.open(
            '//user/updatelocation',
            method='POST',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest

    unittest.main()
