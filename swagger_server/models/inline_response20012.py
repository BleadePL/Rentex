# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.inline_response20012_cars import InlineResponse20012Cars  # noqa: F401,E501
from swagger_server import util


class InlineResponse20012(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, cars: List[InlineResponse20012Cars] = None):  # noqa: E501
        """InlineResponse20012 - a model defined in Swagger

        :param cars: The cars of this InlineResponse20012.  # noqa: E501
        :type cars: List[InlineResponse20012Cars]
        """
        self.swagger_types = {
            'cars': List[InlineResponse20012Cars]
        }

        self.attribute_map = {
            'cars': 'cars'
        }
        self._cars = cars

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponse20012':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_200_12 of this InlineResponse20012.  # noqa: E501
        :rtype: InlineResponse20012
        """
        return util.deserialize_model(dikt, cls)

    @property
    def cars(self) -> List[InlineResponse20012Cars]:
        """Gets the cars of this InlineResponse20012.


        :return: The cars of this InlineResponse20012.
        :rtype: List[InlineResponse20012Cars]
        """
        return self._cars

    @cars.setter
    def cars(self, cars: List[InlineResponse20012Cars]):
        """Sets the cars of this InlineResponse20012.


        :param cars: The cars of this InlineResponse20012.
        :type cars: List[InlineResponse20012Cars]
        """

        self._cars = cars