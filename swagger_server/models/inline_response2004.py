# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class InlineResponse2004(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, res_id: int = None):  # noqa: E501
        """InlineResponse2004 - a model defined in Swagger

        :param res_id: The res_id of this InlineResponse2004.  # noqa: E501
        :type res_id: int
        """
        self.swagger_types = {
            'res_id': int
        }

        self.attribute_map = {
            'res_id': 'resId'
        }
        self._res_id = res_id

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponse2004':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_200_4 of this InlineResponse2004.  # noqa: E501
        :rtype: InlineResponse2004
        """
        return util.deserialize_model(dikt, cls)

    @property
    def res_id(self) -> int:
        """Gets the res_id of this InlineResponse2004.

        Id rezerwacji  # noqa: E501

        :return: The res_id of this InlineResponse2004.
        :rtype: int
        """
        return self._res_id

    @res_id.setter
    def res_id(self, res_id: int):
        """Sets the res_id of this InlineResponse2004.

        Id rezerwacji  # noqa: E501

        :param res_id: The res_id of this InlineResponse2004.
        :type res_id: int
        """

        self._res_id = res_id
