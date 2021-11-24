# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.empty import Empty  # noqa: E501
from swagger_server.models.inline_response2004 import InlineResponse2004  # noqa: E501
from swagger_server.models.inline_response4004 import InlineResponse4004  # noqa: E501
from swagger_server.models.inline_response4005 import InlineResponse4005  # noqa: E501
from swagger_server.models.rent_rent_body import RentRentBody  # noqa: E501
from swagger_server.models.rental import Rental  # noqa: E501
from swagger_server.models.reservation import Reservation  # noqa: E501
from swagger_server.test import BaseTestCase


class TestRentController(BaseTestCase):
    """RentController integration test stubs"""

    def test_rent_rent_id_delete(self):
        """Test case for rent_rent_id_delete

        Konczy wynajem auta
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//rent/rent/{id}'.format(id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_rent_rent_id_get(self):
        """Test case for rent_rent_id_get

        Pobiera wynajem auta
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//rent/rent/{id}'.format(id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_rent_rent_post(self):
        """Test case for rent_rent_post

        Wynajmuje auto
        """
        body = RentRentBody()
        headers = [('session_token', 56)]
        response = self.client.open(
            '//rent/rent',
            method='POST',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_rent_reservate_post(self):
        """Test case for rent_reservate_post

        Rezerwuje auto
        """
        query_string = [('car_id', 56)]
        headers = [('session_token', 56)]
        response = self.client.open(
            '//rent/reservate',
            method='POST',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_rent_reservation_id_delete(self):
        """Test case for rent_reservation_id_delete

        Zakoncza rezerwacje
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//rent/reservation/{id}'.format(id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_rent_reservation_id_get(self):
        """Test case for rent_reservation_id_get

        Pobiera szczegoly rezerwacji
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//rent/reservation/{id}'.format(id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_card_id_delete(self):
        """Test case for user_card_id_delete

        Usuwa karte z konta
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//user/card/{id}'.format(id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest

    unittest.main()
