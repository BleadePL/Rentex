# coding: utf-8
import json

CHARGE_LEVEL_DISTANCE = 5  # TODO: Circa 5Km on 1% charge

from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401


class Reservation:
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, reservation_id: int = None, reservation_start: int = None,
                 car_id: int = None, reservation_end=None, user_id=None):  # noqa: E501
        """Reservation - a model defined in Swagger

        :param reservation_id: The reservation_id of this Reservation.  # noqa: E501
        :type reservation_id: int
        :param reservation_start: The reservation_start of this Reservation.  # noqa: E501
        :type reservation_start: int
        :param duration: The duration of this Reservation.  # noqa: E501
        :type duration: int
        :param car_id: The card_id of this Reservation.  # noqa: E501
        :type car_id: int
        """
        self._id = reservation_id
        self.userId = user_id
        self.reservationStart = reservation_start
        self.reservationEnd = reservation_end
        self.carId = car_id

    @classmethod
    def from_dict(cls, dikt) -> 'Reservation':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Reservation of this Reservation.  # noqa: E501
        :rtype: Reservation
        """
        u = Reservation()
        u.__dict__.update(dikt)
        return u

    def __eq__(self, other):
        if other is not Reservation:
            return False
        return self._id == other._id


class Car:
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, car_id: str = None, brand: str = None, reg_number: str = None, model: str = None,
                 seats: int = None, charge: int = None, activation_cost: str = None,
                 km_cost: str = None, time_cost: str = None, location_lat: str = None, location_long: str = None,
                 status: str = None, esimImei: str = None, esimNumber: str = None, mileage: int = 0,
                 vin: str = None, currentReservation: Reservation = None, reg_country_code=None,
                 last_used=None, last_updateTime=None, services_ids=None):  # noqa: E501
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
        self._id = car_id
        self.vin = vin
        self.brand = brand
        self.regCountryCode = reg_country_code
        self.regNumber = reg_number
        self.modelName = model
        self.seats = seats
        self.chargeLevel = charge
        self.activationCost = activation_cost
        self.kmCost = km_cost
        self.timeCost = time_cost
        self.currentLocationLat = location_lat
        self.currentLocationLong = location_long
        self.status = status
        self.esimImei = esimImei
        self.esimNumber = esimNumber
        self.mileage = mileage
        self.currentReservation = currentReservation
        self.lastUsed = last_used
        self.lastUpdateTime = last_updateTime
        self.servicesIds = services_ids

    @classmethod
    def from_dict(cls, dikt) -> 'Car':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The User of this User.  # noqa: E501
        :rtype: Car
        """
        u = Car()
        u.__dict__.update(dikt)
        return u

    def to_dict_with_less_details(self):
        return {
            'carId': self._id,
            'brand': self.brand,
            'regNumber': self.regCountryCode + self.regNumber,
            'model': self.modelName,
            'seats': self.seats,
            'charge': self.chargeLevel,
            'distanceLeft': self.chargeLevel * CHARGE_LEVEL_DISTANCE,
            'activationCost': self.activationCost,
            'kmCost': self.kmCost,
            'timeCost': self.timeCost,
            'locationLat': self.currentLocationLat,
            'locationLong': self.currentLocationLong

        }


class Rental:
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, rental_id: int = None, car_id: int = None, rental_start: int = None, rental_end: int = None,
                 rental_cost: str = None, mileage: int = None, ended: bool = None, client_id=None):  # noqa: E501
        """Rental - a model defined in Swagger

        :param rental_id: The rental_id of this Rental.  # noqa: E501
        :type rental_id: int
        :param car_id: The car_id of this Rental.  # noqa: E501
        :type car_id: int
        :param rental_start: The rental_start of this Rental.  # noqa: E501
        :type rental_start: int
        :param rental_end: The rental_end of this Rental.  # noqa: E501
        :type rental_end: int
        :param rental_cost: The rental_cost of this Rental.  # noqa: E501
        :type rental_cost: str
        :param mileage: The mileage of this Rental.  # noqa: E501
        :type mileage: int
        :param ended: The ended of this Rental.  # noqa: E501
        :type ended: bool
        """
        self._id = rental_id
        self.renter = client_id
        self.carId = car_id
        self.rentalStart = rental_start
        self.rentalEnd = rental_end
        self.totalCost = rental_cost
        self.mileage = mileage
        self.ended = ended

    @classmethod
    def from_dict(cls, dikt) -> 'Rental':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The User of this User.  # noqa: E501
        :rtype: User
        """
        u = Rental()
        u.__dict__.update(dikt)
        return u

    def __eq__(self, other):
        if other is not Rental:
            return False
        return self._id == other._id

class User:
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, userId: str = None, login: str = None, password: str = None, email: str = None, name: str = None,
                 surname: str = None,
                 account_type: str = None, status: str = None, balance: str = None, pesel: str = None,
                 driver_licence_number: str = None, driver_licence_expiration_date: str = None,
                 last_rental: int = None, reservation: int = None, role: str = None,
                 current_rental: Rental = None, cards=None, activationCode=None,
                 rental_history_ids=None):  # noqa: E501
        """User - a model defined in Swagger

        :param login: The login of this User.  # noqa: E501
        :type login: str
        :param email: The email of this User.  # noqa: E501
        :type email: str
        :param name: The name of this User.  # noqa: E501
        :type name: str
        :param surname: The surname of this User.  # noqa: E501
        :type surname: str
        :param account_type: The account_type of this User.  # noqa: E501
        :type account_type: str
        :param status: The status of this User.  # noqa: E501
        :type status: str
        :param balance: The balance of this User.  # noqa: E501
        :type balance: str
        :param pesel: The pesel of this UserDetails.  # noqa: E501
        :type pesel: str
        :param driver_licence_number: The driver_licence_number of this UserDetails.  # noqa: E501
        :type driver_licence_number: str
        :param driver_licence_expiration_date: The driver_licence_expiration_date of this UserDetails.  # noqa: E501
        :type driver_licence_expiration_date: str
        :param last_rental: The last_rental of this UserDetails.  # noqa: E501
        :type last_rental: int
        :param current_reservation: The last_reservation of this UserDetails.  # noqa: E501
        :type current_reservation: int
        :param role: The role of this UserDetails.  # noqa: E501
        :type role: str
        """

        self._id = userId
        self.login = login
        self.password = password
        self.email = email
        self.name = name
        self.surname = surname
        self.accountType = account_type
        self.status = status
        self.balance = balance
        self.pesel = pesel
        self.driverLicenceNumber = driver_licence_number
        self.driverLicenceExpirationDate = driver_licence_expiration_date
        self.rentalHistoryIds = rental_history_ids
        self.currentRental = current_rental
        self.reservation = reservation
        self.role = role
        self.cards = cards
        self.activationCode = activationCode

    @classmethod
    def from_dict(cls, dikt) -> 'User':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The User of this User.  # noqa: E501
        :rtype: User
        """
        u = User()
        u.__dict__.update(dikt)
        return u


class Location:
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, location_id: str = None, name: str = None, location_lat: str = None, location_long: str = None,
                 location_type: str = None, location_reward: str = None, location_address=None, status: str = None):  # noqa: E501
        """Location - a model defined in Swagger

        :param location_id: The location_id of this Location.  # noqa: E501
        :type location_id: str
        :param name: The name of this Location.  # noqa: E501
        :type name: str
        :param location_lat: The location_lat of this Location.  # noqa: E501
        :type location_lat: str
        :param location_long: The location_long of this Location.  # noqa: E501
        :type location_long: str
        :param location_type: The location_type of this Location.  # noqa: E501
        :type location_type: str
        :param location_reward: The location_reward of this Location.  # noqa: E501
        :type location_reward: str
        """

        self._id = location_id
        self.locationName = name
        self.locationLat = location_lat
        self.locationLong = location_long
        self.locationType = location_type
        self.leaveReward = location_reward
        self.locationAddress = location_address
        self.status = status

    @classmethod
    def from_dict(cls, dikt) -> 'Location':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The User of this User.  # noqa: E501
        :rtype: User
        """
        u = Location()
        u.__dict__.update(dikt)
        return u


class Service:
    def __init__(self, service_id: str = None, car_id: str = None, user_id: str = None, service_start: datetime = None,
                 service_end: datetime = None, description=None):
        self._id = service_id
        self.carId = car_id
        self.leftBy = user_id
        self.dateStart = service_start
        self.dateEnd = service_end
        self.description = description

    @classmethod
    def from_dict(cls, dikt) -> 'Service':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The User of this User.  # noqa: E501
        :rtype: User
        """
        u = Service()
        u.__dict__.update(dikt)
        return u


class CreditCard:
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, card_id: str = None, number: int = None, expiration: str = None,
                 holder_name: str = None, holder_address: str = None):  # noqa: E501
        """CreditCard - a model defined in Swagger

        :param lastdigits: The lastdigits of this CreditCard.  # noqa: E501
        :type lastdigits: int
        :param expiration: The expiration of this CreditCard.  # noqa: E501
        :type expiration: str
        :param holder_name: The holder_name of this CreditCard.  # noqa: E501
        :type holder_name: str
        """

        self._id = card_id
        self.cardNumber = number
        self.expirationDate = expiration
        self.cardHolderName = holder_name
        self.cardHolderAddress = holder_address

    @classmethod
    def from_dict(cls, dikt) -> 'CreditCard':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The User of this User.  # noqa: E501
        :rtype: User
        """
        u = CreditCard()
        u.__dict__.update(dikt)
        return u
