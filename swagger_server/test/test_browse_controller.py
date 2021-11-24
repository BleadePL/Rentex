# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.car import Car  # noqa: E501
from swagger_server.models.empty import Empty  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from swagger_server.models.location import Location  # noqa: E501
from swagger_server.test import BaseTestCase


class TestBrowseController(BaseTestCase):
    """BrowseController integration test stubs"""

    def test_browse_car_id_get(self):
        """Test case for browse_car_id_get

        Zwraca konkretne auto po ID
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//browse/car/{id}'.format(id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_browse_location_id_get(self):
        """Test case for browse_location_id_get

        Zwraca konkretna lokalizacje po ID
        """
        headers = [('session_token', 56)]
        response = self.client.open(
            '//browse/location/{id}'.format(id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_browse_nearestcars_get(self):
        """Test case for browse_nearestcars_get

        Zwraca lokalizacje najblizszych aut
        """
        query_string = [('location_lat', 'location_lat_example'),
                        ('location_long', 'location_long_example'),
                        ('distance', 2000)]
        headers = [('session_token', 56)]
        response = self.client.open(
            '//browse/nearestcars',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_browse_nearestlocations_get(self):
        """Test case for browse_nearestlocations_get

        Zwraca liste najblizszych lokalizacji
        """
        query_string = [('location_lat', 'location_lat_example'),
                        ('location_long', 'location_long_example'),
                        ('distance', 2000)]
        headers = [('session_token', 56)]
        response = self.client.open(
            '//browse/nearestlocations',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest

    unittest.main()
