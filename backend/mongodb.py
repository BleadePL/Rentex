from bson import ObjectId
from pymongo import MongoClient

from utils import calculate_gps_distance
from db_interface import DatabaseInterface
from models import *

import bcrypt
salt = b'$2b$12$pzEs7Xy4xlrgcpLSrcN71O' #Temp

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
        user = self.rentalDb["User"].find_one({"login": login, "password": bcrypt.hashpw(password, salt)})
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
            return None
        added = self.rentalDb["User"].insert_one(
            {
                "name": name,
                "surname": surname,
                "login": login,
                "password": bcrypt.hashpw(password, salt),
                "address": address,
                "email": email,
                "pesel": pesel,
                "balance": "0",
                "accountType": "UNKNOWN",
                "activationCode": "",
                "status": "INACTIVE",
                "role": "CLIENT"
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
        return userStatus["status"] # TODO: check if this returns value

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
        return activationToken["activationCode"]

    def activateAccount(self, userId: str):
        """

        :param token:
        :return true if account activated, false if not
        """
        result = self.rentalDb["User"].update_one({"_id": userId}, {'$set': {"status": "ACTIVE"}})
        if result.modified_count == 0:
            return False
        return result.upserted_id

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
        result = self.rentalDb["User"].update_one({"_id": userId}, {'$set': {"activationCode": token}})
        if result.modified_count == 0:
            return False
        return True

    def changePassword(self, userId, newPwd):
        result = self.rentalDb["User"].update_one(
            {"_id": userId},
            {'$set': {"password": bcrypt.hashpw(newPwd, salt)}})
        if result.modified_count == 0:
            return False
        return True

    def updateLocation(self, carId, location: tuple[str, str]): # TODO: check coords?
        result = self.rentalDb["Car"].update_one(
            {"_id": carId},
            {'$set': {"currentLocationLat": location[0], "currentLocationLong": location[1]}})
        return result.modified_count != 0

    def rentalHistory(self, userId, pageIndex, pageLength):
        rentals = []
        for rentalId in self.rentalDb["User"].find_one({"_id": userId}, {"rentalArchive": 1})["rentalArchive"]:
            rental = self.rentalDb["RentalArchive"].find_one({"_id": rentalId})
            if rental is not None:
                rentals.append(Rental.from_dict(rental))
        return rentals[pageIndex:pageIndex+pageLength]

    def getCards(self, userId):
        cards = []
        for card in self.rentalDb["User"].find_one({"_id": userId}, {"CreditCards": 1})["CreditCards"]:
            cards.append(CreditCard.from_dict(card))
        return cards

    def addCard(self, userId, card: CreditCard):
        result = self.rentalDb["User"].update_one({"_id": userId}, {'$push': {"CreditCards": {
            "_id": ObjectId(),
            "cardNumber": card.cardNumber,
            "expirationDate": card.expirationDate,
            "cardHolderName": card.cardHolderName,
            "cardHolderAddress": card.cardHolderAddress
            }}})
        return result.modified_count != 0

    def deleteCard(self, userId, cardId):
        result = self.rentalDb["User"].update_one({"_id": userId}, {'$pull': {"CreditCards": {
            "_id": cardId
            }}})
        return result.modified_count != 0

    def browseNearestCars(self, location: tuple[str, str], distance) -> list["Car"]: 
        def fun():
            return calculate_gps_distance((float(location[0]), float(location[1])),
                                          (float(self.currentLocationLat), float(
                                              self.currentLocationLong))) <= distance
        cars = []
        for car in self.rentalDb["Car"].find(fun()):  # TODO: check if this fuckery works
            cars.append(Car.from_dict(car))
        return cars

    def browseNearestLocations(
            self, location: tuple[str, str], distance
    ) -> list["Location"]:
        pass

    def getCar(self, carId):
        car = self.rentalDb["Car"].find_one({"_id": carId})
        if car is None:
            return None
        return Car.from_dict(car)

    def getLocation(self, locationId):
        location = self.rentalDb["Location"].find_one({"_id": locationId})
        if location is None:
            return None
        return Car.from_dict(location)

    def getReservation(self, userId, reservationId):
        reservation = self.rentalDb["User"].find_one({"_id": userId}, {"reservation": 1})
        if reservation is None or reservation["_id"] != reservationId:
            return None
        result = Reservation.from_dict(reservation)
        result.userId = userId
        return result

    def endReservation(self, reservation:Reservation):
        reservation_ = self.rentalDb["User"].find_one({"_id": reservation.userId}, {"reservation": 1})
        if reservation_ is None or reservation_["_id"] != reservation.carId:
            return False
        self.rentalDb["User"].find_and_modify({"_id": reservation.userId}, {'$unset': {"reservation": ""}})
        self.rentalDb["Car"].find_and_modify({"_id": reservation_["car"]}, {'$set': {"status": "ACTIVE"}})
        return True

    def startReservation(self, reservation: Reservation):
        if self.rentalDb["Car"].find_one({"_id": reservation.carId})["status"] != "ACTIVE": 
            return False
        user = self.rentalDb["User"].find_one({"_id": reservation.userId})
        if user["currentRental"] != "" or user["reservation"] != "":
            return False
        self.rentalDb["User"].find_and_modify({"_id": reservation.userId}, 
                {"$set": {"reservation": {
                    "_id": ObjectId(),
                    "reservationStart": reservation.reservationStart,
                    "reservationsEnd": reservation.reservationEnd,
                    "car": reservation.carId
                }}})
        self.rentalDb["Car"].find_and_modify({"_id": reservation.carId}, {"$set": {"status": "RESRVED"}})
        return True

    def startRental(self, userId, carId):
        pass

    def getRental(self, userId, rentalId):
        pass

    def endRental(self, rent: Rental):
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

    def getUserRentalHistory(self, userId, pageIndex, pageLength):
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

    def getServicesHistory(self, carId):
        pass

RENTAL_DB = MongoDBInterface()
