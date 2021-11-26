from bson import ObjectId
from pymongo import MongoClient

from backend.utils import calculate_gps_distance
from db_interface import DatabaseInterface
from backend.models import *

import math

HOSTNAME = "vps.zgrate.ovh"
PORT = "27017"
USERNAME = "backend"
PASSWORD = "backendpwd"
DB_NAME = "rental"

COLLECTION_USER = "User"
COLLECTION_CAR = "Car"
COLLECTION_LOCATION = "Location"
COLLECTION_RENTAL_ARCHIVE = "RentalArchive"


client = MongoClient("mongodb://" + USERNAME + ":" + PASSWORD + "@" + HOSTNAME + ":" + PORT + "/", connect=True)

class MongoDBInterface(DatabaseInterface):

    def __init__(self):
        super().__init__()
        self.rentalDb = client[DB_NAME]


    def authUser(self, login, password):
        """
        :param login:
        :param password:
        :return None if not authorized, user_id if authorized
        """
        user = self.rentalDb["User"].find_one({"login": login, "password": password})
        if user is None:
            return None
        return User.from_dict(user)

    def registerUser(
            self,
            name: str,
            surname: str,
            login: str,
            password: str,
            address: str,
            email: str,
            pesel: str,
    ):

        """
       :param name:
       :param surname:
       :param gender:
       :param login:
       :param password:
       :param address:
       :param email:
       :param pesel:
       :return None if any error, user_id if success
       """
        if self.rentalDb["User"].find_one({"login": login}) is not None:
            raise ValueError("login already in use")
        added = self.rentalDb["User"].insert_one(
            {
                "name": name,
                "surname": surname,
                "login": login,
                "password": password,
                "address": address,
                "email": email,
                "pesel": pesel,
            }
        )
        return added.inserted_id

    def getUserToken(self, userId: str):
        pass

    def getAccountStatus(self, userId: str):
        """

        :param userId:
        :return Current status of the account as a str, or None if any error
        """
        userStatus = self.rentalDb["User"].find_one(
            {"_id": userId},
            {"status": 1}
        )
        if userStatus is None:
            return None
        return userStatus

    def getActivationToken(self, userId: str):
        """

        :param userId:
        :return None if there is no token, or token of activation
        """
        activationToken = self.rentalDb["User"].find_one(
            {"_id": userId},
            {"activationCode": 1}
        )
        if activationToken is None:
            return None
        return activationToken

    def activateAccount(self, userId: str):
        """

        :param token:
        :return true if account activated, false if not
        """
        result = self.rentalDb["User"].update_one({"_id": userId}, {"satus": "ACTIVE"})
        return result.upserted_id  # None, or id of user

    def getUser(self, userId):
        """

        :param userId:
        :return User, or None if any error
        """
        user = self.rentalDb["User"].find_one({"_id": userId})
        if user is None:
            return None
        return User.from_dict(user)

    def setActivationToken(self, userId: int, token: str) -> bool:
        """

        :param userId:
        :param token: 6 digits pin
        :return true if successful, false if not

        """
        pass

    def changePassword(self, userId, newPwd):
        user = self.rentalDb["User"].find_one({"_id": userId, "password": oldPwd})
        if user is None:
            return None

        result = self.rentalDb["User"].update_one({"_id": userId}, {"password": newPwd})
        return result.upserted_id  # None, or id of user

    def updateLocation(self, userId, location: tuple[str, str]):
        pass  # TODO: useless?

    def rentalHistory(self, userId, pageIndex, pageLength):
        rentals = []
        for rental in self.rentalDb["User"].find({"_id": userId}, {"rentals"}):
            rentals.append(Rental.from_dict(rental))
        return rentals

    def getCards(self, userId):
        cards = []
        for card in self.rentalDb["User"].find({"_id": userId}, {"creditCards"}):
            cards.append(CreditCard.from_dict(card))
        return cards

    def addCard(self, userId, card):

        added = self.rentalDb["CreditCard"].insert_one(
            {
                "cardNumber": cardNumber,
                "expirationDate": expirationDate,
                "cardHolderName": cardHolder,
                "holderAddress": holderAddress,
            }
        )
        if added.inserted_id is None: return None  # TODO: add to user

    def deleteCard(self, userId, cardId):
        pass

    def browseNearestCars(self, location: tuple[str, str], distance) -> list["Car"]:
        def fun():
            return calculate_gps_distance((float(location[0]), float(location[1])),
                                          (float(self.currentLocationLat), float(
                                              self.currentLocationLong))) <= distance
            # TODO: To musisz pobrać od Usera, albo w sumie możemy przesyłać jako argument. Do omówienia

        cars = []
        for car in self.rentalDb["Car"].find(fun()):  # TODO: check if this fuckery works
            cars.append(Car.from_dict(car))
        return cars

    def browseNearestLocations(
            self, location: tuple[str, str], distance
    ) -> list["Location"]:
        pass

    def getCar(self, carId):
        pass

    def getLocation(self, locationId):
        pass

    def getReservation(self, userId, reservationId):
        pass

    def endReservation(self, userId, reservationId):
        pass

    def startReservation(self, userId, carId):
        pass

    def startRental(self, userId, carId):
        pass

    def getRental(self, userId, rentalId):
        pass

    def endRental(self, userId, rentalId):
        pass

    def adminActive(self, userId):
        pass

    def acceptDocuments(self):
        pass

    def getCars(self, pageIndex, pageCount, location: tuple[str, str], distance):
        pass

    def addCar(self, car: 'Car'):
        pass

    def deleteCar(self, carId):
        pass

    def patchCar(self, carId, changes: dict):
        pass

    def getUsers(self, pageIndex, pageCount, filter: str):
        pass

    def deleteUser(self, userId):
        pass

    def patchUser(self, userId, changes: dict):
        pass

    def getUserRentalHistory(self, userId):
        pass

    def addLocation(self, location: Location):
        pass

    def getLocations(self, pageIndex, pageCount, location: tuple[str, str], distance):
        pass

    def deleteLocation(self, locationId):
        pass

    def patchLocation(self, locationId, changes: dict):
        pass

    def serviceCar(self, carId):
        pass

    def endService(self, carId, serviceId):
        pass

    def getService(self, cardId, serviceId):
        pass

    def getServices(self, carId):
        pass


RENTAL_DB = MongoDBInterface()
