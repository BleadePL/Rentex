# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.car import Car  # noqa: F401,E501
from swagger_server.models.car_details import CarDetails  # noqa: F401,E501
from swagger_server import util


class AdminCarBody(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, vin: str = None, last_used: int = None, last_rental: int = None, mileage: int = None,
                 last_service: int = None, last_update: int = None, last_reservation: int = None,
                 esim_phone_number: int = None, e_sim_imei: str = None, car_id: int = None, brand: str = None,
                 reg_number: str = None, model: str = None, seats: int = None, charge: int = None,
                 distance_left: int = None, activation_cost: str = None, km_cost: str = None, time_cost: str = None,
                 location_lat: str = None, location_long: str = None, status: str = None):  # noqa: E501
        """AdminCarBody - a model defined in Swagger

        :param vin: The vin of this AdminCarBody.  # noqa: E501
        :type vin: str
        :param last_used: The last_used of this AdminCarBody.  # noqa: E501
        :type last_used: int
        :param last_rental: The last_rental of this AdminCarBody.  # noqa: E501
        :type last_rental: int
        :param mileage: The mileage of this AdminCarBody.  # noqa: E501
        :type mileage: int
        :param last_service: The last_service of this AdminCarBody.  # noqa: E501
        :type last_service: int
        :param last_update: The last_update of this AdminCarBody.  # noqa: E501
        :type last_update: int
        :param last_reservation: The last_reservation of this AdminCarBody.  # noqa: E501
        :type last_reservation: int
        :param esim_phone_number: The esim_phone_number of this AdminCarBody.  # noqa: E501
        :type esim_phone_number: int
        :param e_sim_imei: The e_sim_imei of this AdminCarBody.  # noqa: E501
        :type e_sim_imei: str
        :param car_id: The car_id of this AdminCarBody.  # noqa: E501
        :type car_id: int
        :param brand: The brand of this AdminCarBody.  # noqa: E501
        :type brand: str
        :param reg_number: The reg_number of this AdminCarBody.  # noqa: E501
        :type reg_number: str
        :param model: The model of this AdminCarBody.  # noqa: E501
        :type model: str
        :param seats: The seats of this AdminCarBody.  # noqa: E501
        :type seats: int
        :param charge: The charge of this AdminCarBody.  # noqa: E501
        :type charge: int
        :param distance_left: The distance_left of this AdminCarBody.  # noqa: E501
        :type distance_left: int
        :param activation_cost: The activation_cost of this AdminCarBody.  # noqa: E501
        :type activation_cost: str
        :param km_cost: The km_cost of this AdminCarBody.  # noqa: E501
        :type km_cost: str
        :param time_cost: The time_cost of this AdminCarBody.  # noqa: E501
        :type time_cost: str
        :param location_lat: The location_lat of this AdminCarBody.  # noqa: E501
        :type location_lat: str
        :param location_long: The location_long of this AdminCarBody.  # noqa: E501
        :type location_long: str
        :param status: The status of this AdminCarBody.  # noqa: E501
        :type status: str
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
            'e_sim_imei': str,
            'car_id': int,
            'brand': str,
            'reg_number': str,
            'model': str,
            'seats': int,
            'charge': int,
            'distance_left': int,
            'activation_cost': str,
            'km_cost': str,
            'time_cost': str,
            'location_lat': str,
            'location_long': str,
            'status': str
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
            'e_sim_imei': 'eSimImei',
            'car_id': 'carId',
            'brand': 'brand',
            'reg_number': 'regNumber',
            'model': 'model',
            'seats': 'seats',
            'charge': 'charge',
            'distance_left': 'distanceLeft',
            'activation_cost': 'activationCost',
            'km_cost': 'kmCost',
            'time_cost': 'timeCost',
            'location_lat': 'locationLat',
            'location_long': 'locationLong',
            'status': 'status'
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
        self._car_id = car_id
        self._brand = brand
        self._reg_number = reg_number
        self._model = model
        self._seats = seats
        self._charge = charge
        self._distance_left = distance_left
        self._activation_cost = activation_cost
        self._km_cost = km_cost
        self._time_cost = time_cost
        self._location_lat = location_lat
        self._location_long = location_long
        self._status = status

    @classmethod
    def from_dict(cls, dikt) -> 'AdminCarBody':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The admin_car_body of this AdminCarBody.  # noqa: E501
        :rtype: AdminCarBody
        """
        return util.deserialize_model(dikt, cls)

    @property
    def vin(self) -> str:
        """Gets the vin of this AdminCarBody.

        VIN  # noqa: E501

        :return: The vin of this AdminCarBody.
        :rtype: str
        """
        return self._vin

    @vin.setter
    def vin(self, vin: str):
        """Sets the vin of this AdminCarBody.

        VIN  # noqa: E501

        :param vin: The vin of this AdminCarBody.
        :type vin: str
        """

        self._vin = vin

    @property
    def last_used(self) -> int:
        """Gets the last_used of this AdminCarBody.

        Kiedy zostal ostatnio uzyty? (moze byc takze aktualne uzycie!)  # noqa: E501

        :return: The last_used of this AdminCarBody.
        :rtype: int
        """
        return self._last_used

    @last_used.setter
    def last_used(self, last_used: int):
        """Sets the last_used of this AdminCarBody.

        Kiedy zostal ostatnio uzyty? (moze byc takze aktualne uzycie!)  # noqa: E501

        :param last_used: The last_used of this AdminCarBody.
        :type last_used: int
        """

        self._last_used = last_used

    @property
    def last_rental(self) -> int:
        """Gets the last_rental of this AdminCarBody.

        Numer ostatniego wynajecia  # noqa: E501

        :return: The last_rental of this AdminCarBody.
        :rtype: int
        """
        return self._last_rental

    @last_rental.setter
    def last_rental(self, last_rental: int):
        """Sets the last_rental of this AdminCarBody.

        Numer ostatniego wynajecia  # noqa: E501

        :param last_rental: The last_rental of this AdminCarBody.
        :type last_rental: int
        """

        self._last_rental = last_rental

    @property
    def mileage(self) -> int:
        """Gets the mileage of this AdminCarBody.

        Ile ma przejechane w KM  # noqa: E501

        :return: The mileage of this AdminCarBody.
        :rtype: int
        """
        return self._mileage

    @mileage.setter
    def mileage(self, mileage: int):
        """Sets the mileage of this AdminCarBody.

        Ile ma przejechane w KM  # noqa: E501

        :param mileage: The mileage of this AdminCarBody.
        :type mileage: int
        """

        self._mileage = mileage

    @property
    def last_service(self) -> int:
        """Gets the last_service of this AdminCarBody.

        Ostatni serwis  # noqa: E501

        :return: The last_service of this AdminCarBody.
        :rtype: int
        """
        return self._last_service

    @last_service.setter
    def last_service(self, last_service: int):
        """Sets the last_service of this AdminCarBody.

        Ostatni serwis  # noqa: E501

        :param last_service: The last_service of this AdminCarBody.
        :type last_service: int
        """

        self._last_service = last_service

    @property
    def last_update(self) -> int:
        """Gets the last_update of this AdminCarBody.

        Ostatni update lokalizacji  # noqa: E501

        :return: The last_update of this AdminCarBody.
        :rtype: int
        """
        return self._last_update

    @last_update.setter
    def last_update(self, last_update: int):
        """Sets the last_update of this AdminCarBody.

        Ostatni update lokalizacji  # noqa: E501

        :param last_update: The last_update of this AdminCarBody.
        :type last_update: int
        """

        self._last_update = last_update

    @property
    def last_reservation(self) -> int:
        """Gets the last_reservation of this AdminCarBody.

        Numer ostatniej reserwacji (Moze byc aktualnie zarezerwowany!)  # noqa: E501

        :return: The last_reservation of this AdminCarBody.
        :rtype: int
        """
        return self._last_reservation

    @last_reservation.setter
    def last_reservation(self, last_reservation: int):
        """Sets the last_reservation of this AdminCarBody.

        Numer ostatniej reserwacji (Moze byc aktualnie zarezerwowany!)  # noqa: E501

        :param last_reservation: The last_reservation of this AdminCarBody.
        :type last_reservation: int
        """

        self._last_reservation = last_reservation

    @property
    def esim_phone_number(self) -> int:
        """Gets the esim_phone_number of this AdminCarBody.

        Number telefonu karty sim w samochodzie  # noqa: E501

        :return: The esim_phone_number of this AdminCarBody.
        :rtype: int
        """
        return self._esim_phone_number

    @esim_phone_number.setter
    def esim_phone_number(self, esim_phone_number: int):
        """Sets the esim_phone_number of this AdminCarBody.

        Number telefonu karty sim w samochodzie  # noqa: E501

        :param esim_phone_number: The esim_phone_number of this AdminCarBody.
        :type esim_phone_number: int
        """

        self._esim_phone_number = esim_phone_number

    @property
    def e_sim_imei(self) -> str:
        """Gets the e_sim_imei of this AdminCarBody.

        IMEI karty sim w samochodzie  # noqa: E501

        :return: The e_sim_imei of this AdminCarBody.
        :rtype: str
        """
        return self._e_sim_imei

    @e_sim_imei.setter
    def e_sim_imei(self, e_sim_imei: str):
        """Sets the e_sim_imei of this AdminCarBody.

        IMEI karty sim w samochodzie  # noqa: E501

        :param e_sim_imei: The e_sim_imei of this AdminCarBody.
        :type e_sim_imei: str
        """

        self._e_sim_imei = e_sim_imei

    @property
    def car_id(self) -> int:
        """Gets the car_id of this AdminCarBody.

        ID auta  # noqa: E501

        :return: The car_id of this AdminCarBody.
        :rtype: int
        """
        return self._car_id

    @car_id.setter
    def car_id(self, car_id: int):
        """Sets the car_id of this AdminCarBody.

        ID auta  # noqa: E501

        :param car_id: The car_id of this AdminCarBody.
        :type car_id: int
        """

        self._car_id = car_id

    @property
    def brand(self) -> str:
        """Gets the brand of this AdminCarBody.

        Nazwa marki auta  # noqa: E501

        :return: The brand of this AdminCarBody.
        :rtype: str
        """
        return self._brand

    @brand.setter
    def brand(self, brand: str):
        """Sets the brand of this AdminCarBody.

        Nazwa marki auta  # noqa: E501

        :param brand: The brand of this AdminCarBody.
        :type brand: str
        """

        self._brand = brand

    @property
    def reg_number(self) -> str:
        """Gets the reg_number of this AdminCarBody.

        Numer rejestracji  # noqa: E501

        :return: The reg_number of this AdminCarBody.
        :rtype: str
        """
        return self._reg_number

    @reg_number.setter
    def reg_number(self, reg_number: str):
        """Sets the reg_number of this AdminCarBody.

        Numer rejestracji  # noqa: E501

        :param reg_number: The reg_number of this AdminCarBody.
        :type reg_number: str
        """

        self._reg_number = reg_number

    @property
    def model(self) -> str:
        """Gets the model of this AdminCarBody.

        Model auta  # noqa: E501

        :return: The model of this AdminCarBody.
        :rtype: str
        """
        return self._model

    @model.setter
    def model(self, model: str):
        """Sets the model of this AdminCarBody.

        Model auta  # noqa: E501

        :param model: The model of this AdminCarBody.
        :type model: str
        """

        self._model = model

    @property
    def seats(self) -> int:
        """Gets the seats of this AdminCarBody.

        Max Ilosc osob do przewozu  # noqa: E501

        :return: The seats of this AdminCarBody.
        :rtype: int
        """
        return self._seats

    @seats.setter
    def seats(self, seats: int):
        """Sets the seats of this AdminCarBody.

        Max Ilosc osob do przewozu  # noqa: E501

        :param seats: The seats of this AdminCarBody.
        :type seats: int
        """

        self._seats = seats

    @property
    def charge(self) -> int:
        """Gets the charge of this AdminCarBody.

        Ile procent naladowania  # noqa: E501

        :return: The charge of this AdminCarBody.
        :rtype: int
        """
        return self._charge

    @charge.setter
    def charge(self, charge: int):
        """Sets the charge of this AdminCarBody.

        Ile procent naladowania  # noqa: E501

        :param charge: The charge of this AdminCarBody.
        :type charge: int
        """

        self._charge = charge

    @property
    def distance_left(self) -> int:
        """Gets the distance_left of this AdminCarBody.

        Jaki dystans autem jeszcze przejedzie w km?  # noqa: E501

        :return: The distance_left of this AdminCarBody.
        :rtype: int
        """
        return self._distance_left

    @distance_left.setter
    def distance_left(self, distance_left: int):
        """Sets the distance_left of this AdminCarBody.

        Jaki dystans autem jeszcze przejedzie w km?  # noqa: E501

        :param distance_left: The distance_left of this AdminCarBody.
        :type distance_left: int
        """

        self._distance_left = distance_left

    @property
    def activation_cost(self) -> str:
        """Gets the activation_cost of this AdminCarBody.

        Poczatkowy koszt w PLN w formacie \"PLN.GR\"  # noqa: E501

        :return: The activation_cost of this AdminCarBody.
        :rtype: str
        """
        return self._activation_cost

    @activation_cost.setter
    def activation_cost(self, activation_cost: str):
        """Sets the activation_cost of this AdminCarBody.

        Poczatkowy koszt w PLN w formacie \"PLN.GR\"  # noqa: E501

        :param activation_cost: The activation_cost of this AdminCarBody.
        :type activation_cost: str
        """

        self._activation_cost = activation_cost

    @property
    def km_cost(self) -> str:
        """Gets the km_cost of this AdminCarBody.

        Koszt jazdy 1 km w formacie 'PLN.GR'  # noqa: E501

        :return: The km_cost of this AdminCarBody.
        :rtype: str
        """
        return self._km_cost

    @km_cost.setter
    def km_cost(self, km_cost: str):
        """Sets the km_cost of this AdminCarBody.

        Koszt jazdy 1 km w formacie 'PLN.GR'  # noqa: E501

        :param km_cost: The km_cost of this AdminCarBody.
        :type km_cost: str
        """

        self._km_cost = km_cost

    @property
    def time_cost(self) -> str:
        """Gets the time_cost of this AdminCarBody.

        Koszt jazdy 1 minuty w formacie 'PLN.GR'  # noqa: E501

        :return: The time_cost of this AdminCarBody.
        :rtype: str
        """
        return self._time_cost

    @time_cost.setter
    def time_cost(self, time_cost: str):
        """Sets the time_cost of this AdminCarBody.

        Koszt jazdy 1 minuty w formacie 'PLN.GR'  # noqa: E501

        :param time_cost: The time_cost of this AdminCarBody.
        :type time_cost: str
        """

        self._time_cost = time_cost

    @property
    def location_lat(self) -> str:
        """Gets the location_lat of this AdminCarBody.

        Szerokosc geograficzna auta  # noqa: E501

        :return: The location_lat of this AdminCarBody.
        :rtype: str
        """
        return self._location_lat

    @location_lat.setter
    def location_lat(self, location_lat: str):
        """Sets the location_lat of this AdminCarBody.

        Szerokosc geograficzna auta  # noqa: E501

        :param location_lat: The location_lat of this AdminCarBody.
        :type location_lat: str
        """

        self._location_lat = location_lat

    @property
    def location_long(self) -> str:
        """Gets the location_long of this AdminCarBody.

        Dlugosc geograficzna auta  # noqa: E501

        :return: The location_long of this AdminCarBody.
        :rtype: str
        """
        return self._location_long

    @location_long.setter
    def location_long(self, location_long: str):
        """Sets the location_long of this AdminCarBody.

        Dlugosc geograficzna auta  # noqa: E501

        :param location_long: The location_long of this AdminCarBody.
        :type location_long: str
        """

        self._location_long = location_long

    @property
    def status(self) -> str:
        """Gets the status of this AdminCarBody.

        ACTIVE - aktywny, RESERVED - zarezerwowany, INACTIVE - wyłączony z użycia, SERVICE - Serwisowany, INUSE - w uzyciu, UNKNOWN - nieznany stan  # noqa: E501

        :return: The status of this AdminCarBody.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: str):
        """Sets the status of this AdminCarBody.

        ACTIVE - aktywny, RESERVED - zarezerwowany, INACTIVE - wyłączony z użycia, SERVICE - Serwisowany, INUSE - w uzyciu, UNKNOWN - nieznany stan  # noqa: E501

        :param status: The status of this AdminCarBody.
        :type status: str
        """

        self._status = status