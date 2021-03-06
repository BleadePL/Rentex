# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class CarDetails(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, vin: str = None, last_used: int = None, last_rental: int = None, mileage: int = None,
                 last_service: int = None, last_update: int = None, last_reservation: int = None,
                 esim_phone_number: int = None, e_sim_imei: str = None):  # noqa: E501
        """CarDetails - a model defined in Swagger

        :param vin: The vin of this CarDetails.  # noqa: E501
        :type vin: str
        :param last_used: The last_used of this CarDetails.  # noqa: E501
        :type last_used: int
        :param last_rental: The last_rental of this CarDetails.  # noqa: E501
        :type last_rental: int
        :param mileage: The mileage of this CarDetails.  # noqa: E501
        :type mileage: int
        :param last_service: The last_service of this CarDetails.  # noqa: E501
        :type last_service: int
        :param last_update: The last_update of this CarDetails.  # noqa: E501
        :type last_update: int
        :param last_reservation: The last_reservation of this CarDetails.  # noqa: E501
        :type last_reservation: int
        :param esim_phone_number: The esim_phone_number of this CarDetails.  # noqa: E501
        :type esim_phone_number: int
        :param e_sim_imei: The e_sim_imei of this CarDetails.  # noqa: E501
        :type e_sim_imei: str
        """
        self.swagger_types = {
            'vin': str,
            'last_used': int,
            'last_rental': int,
            'mileage': int,
            'last_service': int,
            'last_update': int,
            'last_reservation': int,
            'esim_phone_number': int,
            'e_sim_imei': str
        }

        self.attribute_map = {
            'vin': 'vin',
            'last_used': 'lastUsed',
            'last_rental': 'lastRental',
            'mileage': 'mileage',
            'last_service': 'lastService',
            'last_update': 'lastUpdate',
            'last_reservation': 'lastReservation',
            'esim_phone_number': 'esimPhoneNumber',
            'e_sim_imei': 'eSimImei'
        }
        self._vin = vin
        self._last_used = last_used
        self._last_rental = last_rental
        self._mileage = mileage
        self._last_service = last_service
        self._last_update = last_update
        self._last_reservation = last_reservation
        self._esim_phone_number = esim_phone_number
        self._e_sim_imei = e_sim_imei

    @classmethod
    def from_dict(cls, dikt) -> 'CarDetails':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The CarDetails of this CarDetails.  # noqa: E501
        :rtype: CarDetails
        """
        return util.deserialize_model(dikt, cls)

    @property
    def vin(self) -> str:
        """Gets the vin of this CarDetails.

        VIN  # noqa: E501

        :return: The vin of this CarDetails.
        :rtype: str
        """
        return self._vin

    @vin.setter
    def vin(self, vin: str):
        """Sets the vin of this CarDetails.

        VIN  # noqa: E501

        :param vin: The vin of this CarDetails.
        :type vin: str
        """

        self._vin = vin

    @property
    def last_used(self) -> int:
        """Gets the last_used of this CarDetails.

        Kiedy zostal ostatnio uzyty? (moze byc takze aktualne uzycie!)  # noqa: E501

        :return: The last_used of this CarDetails.
        :rtype: int
        """
        return self._last_used

    @last_used.setter
    def last_used(self, last_used: int):
        """Sets the last_used of this CarDetails.

        Kiedy zostal ostatnio uzyty? (moze byc takze aktualne uzycie!)  # noqa: E501

        :param last_used: The last_used of this CarDetails.
        :type last_used: int
        """

        self._last_used = last_used

    @property
    def last_rental(self) -> int:
        """Gets the last_rental of this CarDetails.

        Numer ostatniego wynajecia  # noqa: E501

        :return: The last_rental of this CarDetails.
        :rtype: int
        """
        return self._last_rental

    @last_rental.setter
    def last_rental(self, last_rental: int):
        """Sets the last_rental of this CarDetails.

        Numer ostatniego wynajecia  # noqa: E501

        :param last_rental: The last_rental of this CarDetails.
        :type last_rental: int
        """

        self._last_rental = last_rental

    @property
    def mileage(self) -> int:
        """Gets the mileage of this CarDetails.

        Ile ma przejechane w KM  # noqa: E501

        :return: The mileage of this CarDetails.
        :rtype: int
        """
        return self._mileage

    @mileage.setter
    def mileage(self, mileage: int):
        """Sets the mileage of this CarDetails.

        Ile ma przejechane w KM  # noqa: E501

        :param mileage: The mileage of this CarDetails.
        :type mileage: int
        """

        self._mileage = mileage

    @property
    def last_service(self) -> int:
        """Gets the last_service of this CarDetails.

        Ostatni serwis  # noqa: E501

        :return: The last_service of this CarDetails.
        :rtype: int
        """
        return self._last_service

    @last_service.setter
    def last_service(self, last_service: int):
        """Sets the last_service of this CarDetails.

        Ostatni serwis  # noqa: E501

        :param last_service: The last_service of this CarDetails.
        :type last_service: int
        """

        self._last_service = last_service

    @property
    def last_update(self) -> int:
        """Gets the last_update of this CarDetails.

        Ostatni update lokalizacji  # noqa: E501

        :return: The last_update of this CarDetails.
        :rtype: int
        """
        return self._last_update

    @last_update.setter
    def last_update(self, last_update: int):
        """Sets the last_update of this CarDetails.

        Ostatni update lokalizacji  # noqa: E501

        :param last_update: The last_update of this CarDetails.
        :type last_update: int
        """

        self._last_update = last_update

    @property
    def last_reservation(self) -> int:
        """Gets the last_reservation of this CarDetails.

        Numer ostatniej reserwacji (Moze byc aktualnie zarezerwowany!)  # noqa: E501

        :return: The last_reservation of this CarDetails.
        :rtype: int
        """
        return self._last_reservation

    @last_reservation.setter
    def last_reservation(self, last_reservation: int):
        """Sets the last_reservation of this CarDetails.

        Numer ostatniej reserwacji (Moze byc aktualnie zarezerwowany!)  # noqa: E501

        :param last_reservation: The last_reservation of this CarDetails.
        :type last_reservation: int
        """

        self._last_reservation = last_reservation

    @property
    def esim_phone_number(self) -> int:
        """Gets the esim_phone_number of this CarDetails.

        Number telefonu karty sim w samochodzie  # noqa: E501

        :return: The esim_phone_number of this CarDetails.
        :rtype: int
        """
        return self._esim_phone_number

    @esim_phone_number.setter
    def esim_phone_number(self, esim_phone_number: int):
        """Sets the esim_phone_number of this CarDetails.

        Number telefonu karty sim w samochodzie  # noqa: E501

        :param esim_phone_number: The esim_phone_number of this CarDetails.
        :type esim_phone_number: int
        """

        self._esim_phone_number = esim_phone_number

    @property
    def e_sim_imei(self) -> str:
        """Gets the e_sim_imei of this CarDetails.

        IMEI karty sim w samochodzie  # noqa: E501

        :return: The e_sim_imei of this CarDetails.
        :rtype: str
        """
        return self._e_sim_imei

    @e_sim_imei.setter
    def e_sim_imei(self, e_sim_imei: str):
        """Sets the e_sim_imei of this CarDetails.

        IMEI karty sim w samochodzie  # noqa: E501

        :param e_sim_imei: The e_sim_imei of this CarDetails.
        :type e_sim_imei: str
        """

        self._e_sim_imei = e_sim_imei
