import bcrypt
from bson import ObjectId
from pymongo import MongoClient

from db_interface import DatabaseInterface
from models import *

from utils import calculate_gps_distance

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

DB_TESTS = False

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
        user = self.rentalDb["User"].find_one(
            {"login": login, "password": bcrypt.hashpw(password.encode('utf8'), salt)})
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
                "password": bcrypt.hashpw(password.encode('utf8'), salt),
                "address": address,
                "email": email,
                "pesel": pesel,
                "balance": "0",
                "accountType": "UNKNOWN",
                "activationCode": "",
                "status": "INACTIVE",
                "role": "CLIENT",
                "currentRental": "",
                "reservation": "",
                "creditCards": [],
                "rentalArchive": []
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
        return userStatus["status"]  # TODO: check if this returns value

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

    def setAccountStatus(self, userId: str, status:str):
        """

        :param token:
        :return true if account activated, false if not
        """
        if status not in ["ACTIVE","INACTIVE","DOCUMENTS","PENDING","PAYMENT","LOCKED","DELETED"]:
            return False
        result = self.rentalDb["User"].update_one({"_id": userId}, {'$set': {"status": status}})
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
            {'$set': {"password": bcrypt.hashpw(newPwd.encode('utf8'), salt)}})
        if result.modified_count == 0:
            return False
        return True

    def updateLocation(self, carId, location: tuple[str, str]):  # TODO: check coords?
        result = self.rentalDb["Car"].update_one(
            {"_id": carId},
            {'$set': {"currentLocationLat": location[0], "currentLocationLong": location[1]}})
        return result.modified_count != 0

    def rentalHistory(self, userId, pageIndex, pageLength):
        rentals = []
        for rentalId in self.rentalDb["User"].find_one({"_id": userId})["rentalArchive"]:
            rental = self.rentalDb["RentalArchive"].find_one({"_id": ObjectId(rentalId)})
            if rental is not None:
                rentals.append(Rental.from_dict(rental))
        return rentals[pageIndex:pageIndex + pageLength]

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
        }}}) # TODO: encrypt CC
        return result.modified_count != 0

    def deleteCard(self, userId, cardId):
        result = self.rentalDb["User"].update_one({"_id": userId}, {'$pull': {"CreditCards": {
            "_id": cardId
        }}})
        return result.modified_count != 0

    def browseNearestCars(self, location: tuple[str, str], distance) -> list["Car"]:
        cars = []
        for car in self.rentalDb["Car"].find():
            if calculate_gps_distance((float(location[0]), float(location[1])),
                                      (float(car["currentLocationLat"]),
                                       float(car["currentLocationLong"]))) <= distance:
                cars.append(Car.from_dict(car))
        return cars

    def browseNearestLocations(
            self, location: tuple[str, str], distance
    ) -> list["Location"]:
        locations = []
        for location_ in self.rentalDb["Location"].find():
            if  calculate_gps_distance((float(location[0]), float(location[1])),
                                          (float(location_["locationLat"]),
                                          float(location_["locationLong"]))) <= distance:
                locations.append(Location.from_dict(location_))
        return locations

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
        if reservation is None or reservation["_id"] != ObjectId(reservationId):
            return None
        result = Reservation.from_dict(reservation)
        result.userId = userId
        return result

    def endReservation(self, reservation: Reservation):
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
        if user["status"] != "ACTIVE" or user["currentRental"] != "" or user["reservation"] != "":
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
        car = self.getCar(carId)
        user = self.getUser(userId)
        if car is None:
            return None
        if user is None:
            return None
        # check if car is available or reserved by the user
        if car.status != "ACTIVE":
            if car.status != "RESERVED":
                return None
            if self.getReservation(userId, carId) is None:
                return None
        # check if user is active and they don't have a currentRental
        if user.status != "ACTIVE" or user.currentRental != "":
            return None
        # if they have a reservation, end it
        if user.reservation != "":
            self.endReservation(user.reservation) # TODO: save reservation in user as object
        # add the rental
        if self.patchCar(carId, {'$set': {"status": "INUSE"}}) is None:
            return None
        rentalId = ObjectId()
        if self.patchUser(userId, {'$set': {"currentRental": {
                '_id': rentalId,
                'rentalStart': datetime.utcnow(),
                'mileage': car.mileage,
                'ended': False,
                'car': carId}}}) is None:
            self.patchCar(carId, {'$set': {"status": "ACTIVE"}})
            return None
        return rentalId

    def getRental(self, userId, rentalId):
        user = self.getUser(userId)
        if user is None:
            return None
        if user.currentRental._id == rentalId:
            return Rental.from_dict(user.currentRental)
        rental= self.rentalDb["RentalArchive"].find_one({"$and": [
                    {"_id": rentalId},
                    {"renter": user._id}]})
        if rental is None:
            return None
        rental = Rental.from_dict(rental)
        rental.renter = userId
        return rental

    def endRental(self, rent: Rental):
        user = self.getUser(rent.renter)
        car = self.getCar(rent.carId)
        rental = self.getRental(rent.renter, rent._id)
        if user is None or car is None or rental is None:
            return False
        if rent.ended == True:
            return False
        if user.currentRental == "" or user.currentRental["car"] != rental.carId:
            return False
        # update everything in the rental
        rental.rentalEnd = datetime.utcnow()
        rental.mileage = car.mileage - rental.mileage
        rental.totalCost = (rental.mileage * car.kmCost +
                (rental.rentalEnd - rental.rentalStart).total_seconds() / 60.0)
        rental.ended = True
        # update car
        self.patchCar(car._id, {"$set" : {"lastUsed": rental.rentalEnd, "status": "ACTIVE"}})
        # update user
        self.patchUser(user._id, {"$set": {"currentRental": ""}})
        # move rental to RentalArchive
        self.rentalDb["RentalArchive"].insert_one({
            "_id": rental._id,
            "rentalStart": rental.rentalStart,
            "rentalEnd": rental.rentalEnd,
            "mileage": rental.mileage,
            "roralCost": rental.totalCost,
            "ended": rental.ended,
            "car": rental.carId,
            "renter": rental.renter
        })
        return True

    def getCars(self, pageIndex, pageCount, location: tuple[str, str], distance):
        cars = self.browseNearestCars(location, distance)
        if cars is None:
            return None
        return cars[pageIndex: pageIndex+pageCount]

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

    def endService(self, serviceId):
        pass

    def getService(self, serviceId):
        pass

    def getServicesHistory(self, carId):
        pass


RENTAL_DB = MongoDBInterface()
if DB_TESTS:
    print(RENTAL_DB.registerUser("asd", "asd", "asdddd", "asd", "asd", "asd", "asd"))
    print(RENTAL_DB.getUser(ObjectId("61a27e387ba5e03ad3acca39"))._id)
    print(RENTAL_DB.getAccountStatus(ObjectId("61a27e387ba5e03ad3acca39")))
    print(RENTAL_DB.activateAccount(ObjectId("61a27e387ba5e03ad3acca39")))
    print(RENTAL_DB.getAccountStatus(ObjectId("61a27e387ba5e03ad3acca39")))
    print(RENTAL_DB.getActivationToken(ObjectId("61a27e387ba5e03ad3acca39")))
    print(RENTAL_DB.setActivationToken(ObjectId("61a27e387ba5e03ad3acca39"), "aasdasd"))
    print(RENTAL_DB.getActivationToken(ObjectId("61a27e387ba5e03ad3acca39")))
    print(RENTAL_DB.changePassword(ObjectId("61a27e387ba5e03ad3acca39"), "dsad"))
    print(RENTAL_DB.rentalHistory(ObjectId("61a27e387ba5e03ad3acca39"), 0, 1))
    # print(RENTAL_DB.addCard(ObjectId("61a27e387ba5e03ad3acca39"), CreditCard("123123123", "123123", "2022-11-02","asdasd", "asdasd")))
    print(RENTAL_DB.getCards(ObjectId("61a27e387ba5e03ad3acca39")))
    # print(RENTAL_DB.deleteCard(ObjectId("61a27e387ba5e03ad3acca39")))
    print(RENTAL_DB.browseNearestCars(("51.067883", "16.973298"), 2000))
