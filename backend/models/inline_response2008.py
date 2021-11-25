# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.rental import Rental  # noqa: F401,E501
from swagger_server import util


class InlineResponse2008(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, rentals: List[Rental] = None):  # noqa: E501
        """InlineResponse2008 - a model defined in Swagger

        :param rentals: The rentals of this InlineResponse2008.  # noqa: E501
        :type rentals: List[Rental]
        """
        self.swagger_types = {
            'rentals': List[Rental]
        }

        self.attribute_map = {
            'rentals': 'rentals'
        }
        self._rentals = rentals

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponse2008':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_200_8 of this InlineResponse2008.  # noqa: E501
        :rtype: InlineResponse2008
        """
        return util.deserialize_model(dikt, cls)

    @property
    def rentals(self) -> List[Rental]:
        """Gets the rentals of this InlineResponse2008.


        :return: The rentals of this InlineResponse2008.
        :rtype: List[Rental]
        """
        return self._rentals

    @rentals.setter
    def rentals(self, rentals: List[Rental]):
        """Sets the rentals of this InlineResponse2008.


        :param rentals: The rentals of this InlineResponse2008.
        :type rentals: List[Rental]
        """

        self._rentals = rentals