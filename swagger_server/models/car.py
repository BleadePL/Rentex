# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Car(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, car_id: int = None, brand: str = None, reg_number: str = None, model: str = None,
                 seats: int = None, charge: int = None, distance_left: int = None, activation_cost: str = None,
                 km_cost: str = None, time_cost: str = None, location_lat: str = None, location_long: str = None,
                 status: str = None):  # noqa: E501
        """Car - a model defined in Swagger

        :param car_id: The car_id of this Car.  # noqa: E501
        :type car_id: int
        :param brand: The brand of this Car.  # noqa: E501
        :type brand: str
        :param reg_number: The reg_number of this Car.  # noqa: E501
        :type reg_number: str
        :param model: The model of this Car.  # noqa: E501
        :type model: str
        :param seats: The seats of this Car.  # noqa: E501
        :type seats: int
        :param charge: The charge of this Car.  # noqa: E501
        :type charge: int
        :param distance_left: The distance_left of this Car.  # noqa: E501
        :type distance_left: int
        :param activation_cost: The activation_cost of this Car.  # noqa: E501
        :type activation_cost: str
        :param km_cost: The km_cost of this Car.  # noqa: E501
        :type km_cost: str
        :param time_cost: The time_cost of this Car.  # noqa: E501
        :type time_cost: str
        :param location_lat: The location_lat of this Car.  # noqa: E501
        :type location_lat: str
        :param location_long: The location_long of this Car.  # noqa: E501
        :type location_long: str
        :param status: The status of this Car.  # noqa: E501
        :type status: str
        """
        self.swagger_types = {
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
    def from_dict(cls, dikt) -> 'Car':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Car of this Car.  # noqa: E501
        :rtype: Car
        """
        return util.deserialize_model(dikt, cls)

    @property
    def car_id(self) -> int:
        """Gets the car_id of this Car.

        ID auta  # noqa: E501

        :return: The car_id of this Car.
        :rtype: int
        """
        return self._car_id

    @car_id.setter
    def car_id(self, car_id: int):
        """Sets the car_id of this Car.

        ID auta  # noqa: E501

        :param car_id: The car_id of this Car.
        :type car_id: int
        """

        self._car_id = car_id

    @property
    def brand(self) -> str:
        """Gets the brand of this Car.

        Nazwa marki auta  # noqa: E501

        :return: The brand of this Car.
        :rtype: str
        """
        return self._brand

    @brand.setter
    def brand(self, brand: str):
        """Sets the brand of this Car.

        Nazwa marki auta  # noqa: E501

        :param brand: The brand of this Car.
        :type brand: str
        """

        self._brand = brand

    @property
    def reg_number(self) -> str:
        """Gets the reg_number of this Car.

        Numer rejestracji  # noqa: E501

        :return: The reg_number of this Car.
        :rtype: str
        """
        return self._reg_number

    @reg_number.setter
    def reg_number(self, reg_number: str):
        """Sets the reg_number of this Car.

        Numer rejestracji  # noqa: E501

        :param reg_number: The reg_number of this Car.
        :type reg_number: str
        """

        self._reg_number = reg_number

    @property
    def model(self) -> str:
        """Gets the model of this Car.

        Model auta  # noqa: E501

        :return: The model of this Car.
        :rtype: str
        """
        return self._model

    @model.setter
    def model(self, model: str):
        """Sets the model of this Car.

        Model auta  # noqa: E501

        :param model: The model of this Car.
        :type model: str
        """

        self._model = model

    @property
    def seats(self) -> int:
        """Gets the seats of this Car.

        Max Ilosc osob do przewozu  # noqa: E501

        :return: The seats of this Car.
        :rtype: int
        """
        return self._seats

    @seats.setter
    def seats(self, seats: int):
        """Sets the seats of this Car.

        Max Ilosc osob do przewozu  # noqa: E501

        :param seats: The seats of this Car.
        :type seats: int
        """

        self._seats = seats

    @property
    def charge(self) -> int:
        """Gets the charge of this Car.

        Ile procent naladowania  # noqa: E501

        :return: The charge of this Car.
        :rtype: int
        """
        return self._charge

    @charge.setter
    def charge(self, charge: int):
        """Sets the charge of this Car.

        Ile procent naladowania  # noqa: E501

        :param charge: The charge of this Car.
        :type charge: int
        """

        self._charge = charge

    @property
    def distance_left(self) -> int:
        """Gets the distance_left of this Car.

        Jaki dystans autem jeszcze przejedzie w km?  # noqa: E501

        :return: The distance_left of this Car.
        :rtype: int
        """
        return self._distance_left

    @distance_left.setter
    def distance_left(self, distance_left: int):
        """Sets the distance_left of this Car.

        Jaki dystans autem jeszcze przejedzie w km?  # noqa: E501

        :param distance_left: The distance_left of this Car.
        :type distance_left: int
        """

        self._distance_left = distance_left

    @property
    def activation_cost(self) -> str:
        """Gets the activation_cost of this Car.

        Poczatkowy koszt w PLN w formacie \"PLN.GR\"  # noqa: E501

        :return: The activation_cost of this Car.
        :rtype: str
        """
        return self._activation_cost

    @activation_cost.setter
    def activation_cost(self, activation_cost: str):
        """Sets the activation_cost of this Car.

        Poczatkowy koszt w PLN w formacie \"PLN.GR\"  # noqa: E501

        :param activation_cost: The activation_cost of this Car.
        :type activation_cost: str
        """

        self._activation_cost = activation_cost

    @property
    def km_cost(self) -> str:
        """Gets the km_cost of this Car.

        Koszt jazdy 1 km w formacie 'PLN.GR'  # noqa: E501

        :return: The km_cost of this Car.
        :rtype: str
        """
        return self._km_cost

    @km_cost.setter
    def km_cost(self, km_cost: str):
        """Sets the km_cost of this Car.

        Koszt jazdy 1 km w formacie 'PLN.GR'  # noqa: E501

        :param km_cost: The km_cost of this Car.
        :type km_cost: str
        """

        self._km_cost = km_cost

    @property
    def time_cost(self) -> str:
        """Gets the time_cost of this Car.

        Koszt jazdy 1 minuty w formacie 'PLN.GR'  # noqa: E501

        :return: The time_cost of this Car.
        :rtype: str
        """
        return self._time_cost

    @time_cost.setter
    def time_cost(self, time_cost: str):
        """Sets the time_cost of this Car.

        Koszt jazdy 1 minuty w formacie 'PLN.GR'  # noqa: E501

        :param time_cost: The time_cost of this Car.
        :type time_cost: str
        """

        self._time_cost = time_cost

    @property
    def location_lat(self) -> str:
        """Gets the location_lat of this Car.

        Szerokosc geograficzna auta  # noqa: E501

        :return: The location_lat of this Car.
        :rtype: str
        """
        return self._location_lat

    @location_lat.setter
    def location_lat(self, location_lat: str):
        """Sets the location_lat of this Car.

        Szerokosc geograficzna auta  # noqa: E501

        :param location_lat: The location_lat of this Car.
        :type location_lat: str
        """

        self._location_lat = location_lat

    @property
    def location_long(self) -> str:
        """Gets the location_long of this Car.

        Dlugosc geograficzna auta  # noqa: E501

        :return: The location_long of this Car.
        :rtype: str
        """
        return self._location_long

    @location_long.setter
    def location_long(self, location_long: str):
        """Sets the location_long of this Car.

        Dlugosc geograficzna auta  # noqa: E501

        :param location_long: The location_long of this Car.
        :type location_long: str
        """

        self._location_long = location_long

    @property
    def status(self) -> str:
        """Gets the status of this Car.

        ACTIVE - aktywny, RESERVED - zarezerwowany, INACTIVE - wyłączony z użycia, SERVICE - Serwisowany, INUSE - w uzyciu, UNKNOWN - nieznany stan  # noqa: E501

        :return: The status of this Car.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: str):
        """Sets the status of this Car.

        ACTIVE - aktywny, RESERVED - zarezerwowany, INACTIVE - wyłączony z użycia, SERVICE - Serwisowany, INUSE - w uzyciu, UNKNOWN - nieznany stan  # noqa: E501

        :param status: The status of this Car.
        :type status: str
        """

        self._status = status