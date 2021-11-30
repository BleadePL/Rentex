# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.car import Car  # noqa: F401,E501
from swagger_server import util


class InlineResponse2002(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, cars: List[Car] = None):  # noqa: E501
        """InlineResponse2002 - a model defined in Swagger

        :param cars: The cars of this InlineResponse2002.  # noqa: E501
        :type cars: List[Car]
        """
        self.swagger_types = {
            'cars': List[Car]
        }

        self.attribute_map = {
            'cars': 'cars'
        }
        self._cars = cars

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponse2002':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_200_2 of this InlineResponse2002.  # noqa: E501
        :rtype: InlineResponse2002
        """
        return util.deserialize_model(dikt, cls)

    @property
    def cars(self) -> List[Car]:
        """Gets the cars of this InlineResponse2002.


        :return: The cars of this InlineResponse2002.
        :rtype: List[Car]
        """
        return self._cars

    @cars.setter
    def cars(self, cars: List[Car]):
        """Sets the cars of this InlineResponse2002.


        :param cars: The cars of this InlineResponse2002.
        :type cars: List[Car]
        """

        self._cars = cars
