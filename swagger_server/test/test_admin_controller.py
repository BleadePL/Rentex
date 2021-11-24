# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.admin_car_body import AdminCarBody  # noqa: E501
from swagger_server.models.admin_location_body import AdminLocationBody  # noqa: E501
from swagger_server.models.car_id_body import CarIdBody  # noqa: E501
from swagger_server.models.empty import Empty  # noqa: E501
from swagger_server.models.inline_response20010 import InlineResponse20010  # noqa: E501
from swagger_server.models.inline_response20011 import InlineResponse20011  # noqa: E501
from swagger_server.models.inline_response20012 import InlineResponse20012  # noqa: E501
from swagger_server.models.inline_response20013 import InlineResponse20013  # noqa: E501
from swagger_server.models.inline_response20014 import InlineResponse20014  # noqa: E501
from swagger_server.models.inline_response2005 import InlineResponse2005  # noqa: E501
from swagger_server.models.inline_response2006 import InlineResponse2006  # noqa: E501
from swagger_server.models.inline_response2007 import InlineResponse2007  # noqa: E501
from swagger_server.models.inline_response2008 import InlineResponse2008  # noqa: E501
from swagger_server.models.inline_response2009 import InlineResponse2009  # noqa: E501
from swagger_server.models.location_id_body import LocationIdBody  # noqa: E501
from swagger_server.models.user_id_body import UserIdBody  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAdminController(BaseTestCase):
    """AdminController integration test stubs"""

    def test_admin_car_get(self):
        """Test case for admin_car_get

        Pobiera liste aut
        """
        query_string = [('location_lat', 'location_lat_example'),
                        ('location_long', 'location_long_example'),
                        ('pagelength', 1),
                        ('startindex', 0),
                        ('distance', 2000),
                        ('details', false)]
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/car',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_car_id_delete(self):
        """Test case for admin_car_id_delete

        Usuwa auto z systemu
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/car/{id}'.format(id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_car_id_get(self):
        """Test case for admin_car_id_get

        Pobiera szczegoly auta
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/car/{id}'.format(id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_car_id_patch(self):
        """Test case for admin_car_id_patch

        Modyfikuje dane auta
        """
        body = CarIdBody()
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/car/{id}'.format(id=56),
            method='PATCH',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_car_id_rentalhistory_get(self):
        """Test case for admin_car_id_rentalhistory_get

        Zwraca historie przejazdow
        """
        query_string = [('startindex', 0),
                        ('pagelength', 1)]
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/car/{id}/rentalhistory'.format(id=56),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_car_id_reservationhistory_get(self):
        """Test case for admin_car_id_reservationhistory_get

        Zwraca historie rezerwacji
        """
        query_string = [('startindex', 0),
                        ('pagelength', 1)]
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/car/{id}/reservationhistory'.format(id=56),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_car_post(self):
        """Test case for admin_car_post

        Dodaje nowe auto
        """
        body = AdminCarBody()
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/car',
            method='POST',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_location_get(self):
        """Test case for admin_location_get

        Pobiera liste lokacji
        """
        query_string = [('location_lat', 'location_lat_example'),
                        ('location_long', 'location_long_example'),
                        ('pagelength', 1),
                        ('startindex', 0),
                        ('distance', 2000)]
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/location',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_location_id_delete(self):
        """Test case for admin_location_id_delete

        Usuwa lokacje z systemu
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/location/{id}'.format(id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_location_id_get(self):
        """Test case for admin_location_id_get

        Pobiera szczegoly lokacji
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/location/{id}'.format(id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_location_id_patch(self):
        """Test case for admin_location_id_patch

        Modyfikuje dane Lokacji
        """
        body = LocationIdBody()
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/location/{id}'.format(id=56),
            method='PATCH',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_location_post(self):
        """Test case for admin_location_post

        Dodaje nową lokację
        """
        body = AdminLocationBody()
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/location',
            method='POST',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_user_get(self):
        """Test case for admin_user_get

        Zwraca liste uzytkownikow
        """
        query_string = [('startindex', 0),
                        ('pagelength', 1),
                        ('details', false),
                        ('filter', '')]
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/user',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_user_id_activate_post(self):
        """Test case for admin_user_id_activate_post

        Aktywuje konto usera
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/user/{id}/activate'.format(id=56),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_user_id_delete(self):
        """Test case for admin_user_id_delete

        Usuwa usera z systemu
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/user/{id}'.format(id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_user_id_documents_delete(self):
        """Test case for admin_user_id_documents_delete

        Odrzuca dokumenty uzytkowniika
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/user/{id}/documents'.format(id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_user_id_documents_get(self):
        """Test case for admin_user_id_documents_get

        Zwraca dokumenty uzytkownika w systemie
        """
        query_string = [('side', 'F')]
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/user/{id}/documents'.format(id=56),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_user_id_documents_put(self):
        """Test case for admin_user_id_documents_put

        Potwierdza dokumety uzytkownika
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/user/{id}/documents'.format(id=56),
            method='PUT',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_user_id_get(self):
        """Test case for admin_user_id_get

        Pobiera szczegoly uzytkownika
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/user/{id}'.format(id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_user_id_patch(self):
        """Test case for admin_user_id_patch

        Modyfikuje dane usera
        """
        body = UserIdBody()
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/user/{id}'.format(id=56),
            method='PATCH',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_user_id_rentalhistory_get(self):
        """Test case for admin_user_id_rentalhistory_get

        Zwraca historie przejazdow
        """
        query_string = [('startindex', 0),
                        ('pagelength', 1)]
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/user/{id}/rentalhistory'.format(id=56),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_user_id_reservationhistory_get(self):
        """Test case for admin_user_id_reservationhistory_get

        Zwraca historie rezerwacji
        """
        query_string = [('startindex', 0),
                        ('pagelength', 1)]
        headers = [('session_token', 56)]
        response = self.client.open(
            '//admin/user/{id}/reservationhistory'.format(id=56),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest

    unittest.main()
