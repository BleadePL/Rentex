from backend.models.car import Car
from backend.models.location import Location
from backend.models.user import User
from backend.models.rental import Rental
from backend.models.credit_card import CreditCard
import math
# TODO: TEMP
from pymongo import MongoClient

HOSTNAME = "vps.zgrate.ovh"
PORT = "27017"
USERNAME = "backend"
PASSWORD = "backendpwd"
DB_NAME = "rental"

client = MongoClient(
    "mongodb://" + USERNAME + ":" + PASSWORD + "@" + HOSTNAME + ":" + PORT + "/",
    connect=True,
)
# /TODO: TEMP


class DatabaseInterface:
    def __init__(self):  # TODO: TEMP
        self.rentalDb = client["rental"]

    def __GPSDistance(coord1, coord2):
        
        R = 6372800  # Earth radius in meters
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        
        phi1, phi2 = math.radians(lat1), math.radians(lat2) 
        dphi       = math.radians(lat2 - lat1)
        dlambda    = math.radians(lon2 - lon1)
        
        a = math.sin(dphi/2)**2 + \
            math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        
        return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))


    def authUser(self, login, password):
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
        userStatus = self.rentalDb["User"].find_one(
            {"_id": userId},
            {"status": 1}
        )
        if userStatus is None:
            return None
        return userStatus

    def getActivationToken(self, userId: str):
        activationToken = self.rentalDb["User"].find_one(
            {"_id": userId}, 
            {"activationCode": 1}
        )
        if activationToken is None:
            return None
        return activationToken

    def activateAccount(self, userId: str):
        result = self.rentalDb["User"].update_one({"_id": userId}, {"satus": "ACTIVE"})
        return result.upserted_id  # None, or id of user

    def getUser(self, userId):
        user = self.rentalDb["User"].find_one({"_id": userId})
        if user is None:
            return None
        return User.from_dict(user)

    def changePassword(self, userId, oldPwd, newPwd):
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
        for card in self.rentalDb["User"].find({"_id": userId}, {"creditCards"})
            cards.append(CreditCard.from_dict(card))
        return cards


    def addCard(self, userId, cardNumber, expirationDate, cardHolder, holderAddress):

        added = self.rentalDb["CreditCard"].insert_one(
            {
                "cardNumber": cardNumber,
                "expirationDate": expirationDate,
                "cardHolderName": cardHolder,
                "holderAddress": holderAddress,
            }
        )
        if added.inserted_id is None: return None # TODO: add to user


    def deleteCard(self, userId, cardId):
        pass

    def browseNearestCars(self, location: tuple[str, str], distance) -> list["Car"]:
        def fun():
            return self.__GPSDistance((float(location[0]), float(location[1])), (float(self.currentLocationLat), float(self.currentLocationLong))) <= distance
        cars = []
        for car in self.rentalDb["Car"].find(fun()): #TODO: check if this fuckery works
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

    def addCar(self, car: "Car"):
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
