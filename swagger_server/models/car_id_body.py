# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.all_ofcar_id_body_patch import AllOfcarIdBodyPatch  # noqa: F401,E501
from swagger_server import util


class CarIdBody(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, patch: AllOfcarIdBodyPatch = None):  # noqa: E501
        """CarIdBody - a model defined in Swagger

        :param patch: The patch of this CarIdBody.  # noqa: E501
        :type patch: AllOfcarIdBodyPatch
        """
        self.swagger_types = {
            'patch': AllOfcarIdBodyPatch
        }

        self.attribute_map = {
            'patch': 'patch'
        }
        self._patch = patch

    @classmethod
    def from_dict(cls, dikt) -> 'CarIdBody':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The car_id_body of this CarIdBody.  # noqa: E501
        :rtype: CarIdBody
        """
        return util.deserialize_model(dikt, cls)

    @property
    def patch(self) -> AllOfcarIdBodyPatch:
        """Gets the patch of this CarIdBody.

        Co zmienic? Tylko te wartosci, ktore chcesz zmienic (oczywiskie niektorych rzeczy sie nie da, np modyfikowanie ID)  # noqa: E501

        :return: The patch of this CarIdBody.
        :rtype: AllOfcarIdBodyPatch
        """
        return self._patch

    @patch.setter
    def patch(self, patch: AllOfcarIdBodyPatch):
        """Sets the patch of this CarIdBody.

        Co zmienic? Tylko te wartosci, ktore chcesz zmienic (oczywiskie niektorych rzeczy sie nie da, np modyfikowanie ID)  # noqa: E501

        :param patch: The patch of this CarIdBody.
        :type patch: AllOfcarIdBodyPatch
        """

        self._patch = patch
