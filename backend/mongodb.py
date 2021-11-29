import bcrypt
from bson import ObjectId
from pymongo import MongoClient
from utils import convertObjectIdsToStr

from db_interface import DatabaseInterface
from models import *

from utils import calculate_gps_distance

salt = b'$2b$12$pzEs7Xy4xlrgcpLSrcN71O'  # Temp

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
        return User.from_dict(convertObjectIdsToStr(user))

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
        return convertObjectIdsToStr(added.inserted_id)

    def getAccountStatus(self, userId: str):
        """

        :param userId:
        :return Current status of the account as a str, or None if any error
        """
        userStatus = self.rentalDb["User"].find_one(
            {"_id": ObjectId(userId)},
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
            {"_id": ObjectId(userId)},
            {"activationCode": 1}
        )
        if activationToken is None:
            return None
        return activationToken["activationCode"]

    def setAccountStatus(self, userId: str, status: str):
        """

        :param token:
        :return true if account activated, false if not
        """
        if status not in ["ACTIVE", "INACTIVE", "DOCUMENTS", "PENDING", "PAYMENT", "LOCKED", "DELETED"]:
            return False
        result = self.rentalDb["User"].update_one({"_id": ObjectId(userId)}, {'$set': {"status": status}})
        if result.modified_count == 0:
            return False
        return convertObjectIdsToStr(result.upserted_id)

    def getUser(self, userId):
        """
        :param userId:
        :return User, or None if any error
        """
        user = self.rentalDb["User"].find_one({"_id": ObjectId(userId)})
        if user is None:
            return None
        return User.from_dict(convertObjectIdsToStr(user))

    def setActivationToken(self, userId: int, token: str) -> bool:
        """

        :param userId:
        :param token: 6 digits pin
        :return true if successful, false if not

        """
        result = self.rentalDb["User"].update_one({"_id": ObjectId(userId)}, {'$set': {"activationCode": token}})
        if result.modified_count == 0:
            return False
        return True

    def changePassword(self, userId, newPwd):
        result = self.rentalDb["User"].update_one(
            {"_id": ObjectId(userId)},
            {'$set': {"password": bcrypt.hashpw(newPwd.encode('utf8'), salt)}})
        if result.modified_count == 0:
            return False
        return True

    def updateLocation(self, carId, location: tuple[str, str]):  # TODO: check coords?
        result = self.rentalDb["Car"].update_one(
            {"_id": ObjectId(carId)},
            {'$set': {"currentLocationLat": location[0], "currentLocationLong": location[1]}})
        return result.modified_count != 0

    def rentalHistory(self, userId, pageIndex, pageLength):
        rentals = []
        for rentalId in self.rentalDb["User"].find_one({"_id": ObjectId(userId)})["rentalArchive"]:
            rental = self.rentalDb["RentalArchive"].find_one({"_id": ObjectId(rentalId)})
            if rental is not None:
                rentals.append(Rental.from_dict(convertObjectIdsToStr(rental)))
        return rentals[pageIndex:pageIndex + pageLength]

    def getCards(self, userId):
        cards = []
        for card in self.rentalDb["User"].find_one({"_id": ObjectId(userId)}, {"CreditCards": 1})["CreditCards"]:
            cards.append(CreditCard.from_dict(convertObjectIdsToStr(card)))
        return cards

    def addCard(self, userId, card: CreditCard):
        result = self.rentalDb["User"].update_one({"_id": ObjectId(userId)}, {'$push': {"CreditCards": {
            "_id": ObjectId(),
            "cardNumber": card.cardNumber,
            "expirationDate": card.expirationDate,
            "cardHolderName": card.cardHolderName,
            "cardHolderAddress": card.cardHolderAddress
        }}})  # TODO: encrypt CC
        return result.modified_count != 0

    def deleteCard(self, userId, cardId):
        result = self.rentalDb["User"].update_one({"_id": ObjectId(userId)}, {'$pull': {"CreditCards": {
            "_id": ObjectId(cardId)
        }}})
        return result.modified_count != 0

    def browseNearestCars(self, location: tuple[str, str], distance) -> list["Car"]:
        cars = []
        for car in self.rentalDb["Car"].find():
            if calculate_gps_distance((float(location[0]), float(location[1])),
                                      (float(car["currentLocationLat"]),
                                       float(car["currentLocationLong"]))) <= int(distance):
                cars.append(Car.from_dict(convertObjectIdsToStr(car)))
        return cars

    def browseNearestLocations(
            self, location: tuple[str, str], distance
    ) -> list["Location"]:
        locations = []
        for location_ in self.rentalDb["Location"].find():
            if calculate_gps_distance((float(location[0]), float(location[1])),
                                      (float(location_["locationLat"]),
                                       float(location_["locationLong"]))) <= distance:
                locations.append(Location.from_dict(convertObjectIdsToStr(location_)))
        return locations

    def getCar(self, carId):
        car = self.rentalDb["Car"].find_one({"_id": ObjectId(carId)})
        if car is None:
            return None
        return Car.from_dict(convertObjectIdsToStr(car))

    def getLocation(self, locationId):
        location = self.rentalDb["Location"].find_one({"_id": ObjectId(locationId)})
        if location is None:
            return None
        return Car.from_dict(convertObjectIdsToStr(location))

    def getReservation(self, userId, reservationId):
        reservation = self.rentalDb["User"].find_one({"_id": ObjectId(userId)}, {"reservation": 1})
        if reservation is None or reservation["_id"] != ObjectId(reservationId):
            return None
        result = Reservation.from_dict(convertObjectIdsToStr(reservation))
        result.userId = userId
        return result

    def endReservation(self, reservation: Reservation):
        reservation_ = self.rentalDb["User"].find_one({"_id": ObjectId(reservation.userId)}, {"reservation": 1})
        if reservation_ is None or reservation_["_id"] != ObjectId(reservation.carId):
            return False
        self.rentalDb["User"].find_and_modify({"_id": ObjectId(reservation.userId)}, {'$unset': {"reservation": ""}})
        self.rentalDb["Car"].find_and_modify({"_id": ObjectId(reservation.carId)}, {'$set': {"status": "ACTIVE"}})
        return True

    def startReservation(self, reservation: Reservation) -> str:
        if self.rentalDb["Car"].find_one({"_id": ObjectId(reservation.carId)})["status"] != "ACTIVE":
            return False
        user = self.rentalDb["User"].find_one({"_id": ObjectId(reservation.userId)})
        if user["status"] != "ACTIVE" or user["currentRental"] != "" or user["reservation"] != "":
            return False
        self.rentalDb["User"].find_and_modify({"_id": ObjectId(reservation.userId)},
                                              {"$set": {"reservation": {
                                                  "_id": ObjectId(),
                                                  "reservationStart": reservation.reservationStart,
                                                  "reservationsEnd": reservation.reservationEnd,
                                                  "car": ObjectId(reservation.carId)
                                              }}})
        self.rentalDb["Car"].find_and_modify({"_id": ObjectId(reservation.carId)}, {"$set": {"status": "RESERVED"}})
        # TODO GET ID HERE
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
            self.endReservation(user.reservation)  # TODO: save reservation in user as object
        # add the rental
        if self.patchCar(carId, {"status": "INUSE"}) is None:
            return None
        rentalId = ObjectId()
        if self.patchUser(userId, {"currentRental": {
            '_id': rentalId,
            'rentalStart': datetime.utcnow(),
            'mileage': car.mileage,
            'ended': False,
            'car': ObjectId(carId)}}) is None:
            self.patchCar(carId, {"status": "ACTIVE"})
            return None
        return convertObjectIdsToStr(rentalId)

    def getRental(self, userId, rentalId):
        user = self.getUser(userId)
        if user is None:
            return None
        if user.currentRental._id == ObjectId(rentalId):
            return Rental.from_dict(convertObjectIdsToStr(user.currentRental))
        rental = self.rentalDb["RentalArchive"].find_one({"$and": [
            {"_id": ObjectId(rentalId)},
            {"renter": ObjectId(user._id)}]})
        if rental is None:
            return None
        rental = Rental.from_dict(convertObjectIdsToStr(rental))
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
        self.patchCar(car._id, {"lastUsed": rental.rentalEnd, "status": "ACTIVE"})
        # update user
        self.patchUser(user._id, {"currentRental": ""})
        # move rental to RentalArchive
        self.rentalDb["RentalArchive"].insert_one({
            "_id": ObjectId(rental._id),
            "rentalStart": rental.rentalStart,
            "rentalEnd": rental.rentalEnd,
            "mileage": rental.mileage,
            "roralCost": rental.totalCost,
            "ended": rental.ended,
            "car": ObjectId(rental.carId),
            "renter": ObjectId(rental.renter)
        })
        return True

    def getCars(self, pageIndex, pageCount, location: tuple[str, str], distance):
        cars = self.browseNearestCars(location, distance)
        if cars is None:
            return None
        return cars[int(pageIndex): int(pageIndex) + int(pageCount)]

    def deleteCar(self, carId):
        result = self.rentalDb["Car"].delete_one({ObjectId(carId)})
        return result.deleted_count != 0

    def patchCar(self, carId, changes: dict):
        if any(change in changes for change in ["chargeLevel", "mileage", "currentLocationLat", "currentLocationLong"]):
            changes["lastUpdateTime"] = datetime.utcnow()
        result = self.rentalDb["Car"].find_one_and_update({"_id": ObjectId(carId)},
                                                          {"$set": changes})  # TODO: REMOVE "$set"
        return result is not None

    def getUsers(self, pageIndex, pageCount, filter: str):
        filter = f".*{filter}.*"
        users = []
        for user in self.rentalDb["User"].find({"$or": [
            {"pesel": {"$regex": filter}},
            {"surname": {"$regex": filter}},
            {"name": {"$regex": filter}},
            {"address": {"$regex": filter}},
            {"driverLicenceNumber": {"$regex": filter}},
            {"login": {"$regex": filter}},
            {"email": {"$regex": filter}},
        ]}).skip(pageIndex).limit(pageCount):
            users.append(User.from_dict(convertObjectIdsToStr(user)))
        return users

    def deleteUser(self, userId):
        result = self.patchUser(userId, {"status": "DELETED"})

    def patchUser(self, userId, changes: dict):
        result = self.rentalDb["User"].find_one_and_update({"_id": ObjectId(userId)}, changes)
        return result is not None

    def getUserRentalHistory(self, userId, pageIndex, pageLength):
        rentals = []
        for rental in self.rentalDb["RentalArchive"].find({"renter": ObjectId(userId)}
                                                          ).skip(pageIndex).limit(pageLength):
            rentals.append(Rental.from_dict(convertObjectIdsToStr(rental)))
        return rentals

    def getCard(self, userId, cardId):
        for card in self.getCards(userId):
            if card._id == cardId:
                return card
        return None

    def addLocation(self, location: Location):
        result = self.rentalDb["Location"].insert_one({
            "locationType": location.locationType,
            "locationName": location.locationName,
            "locationAddress": location.locationAddress,
            "leaveReward": location.leaveReward,
            "locationLat": location.locationLat,
            "locationLong": location.locationLong,
            "status": location.status,
        })
        return convertObjectIdsToStr(result.inserted_id)

    def getLocations(self, pageIndex, pageCount, location: tuple[str, str], distance):
        locations = self.browseNearestLocations(location, distance)
        if locations is None:
            return None
        return locations[pageIndex: pageIndex + pageCount]

    def deleteLocation(self, locationId):
        if len(self.getServicesForLocation(locationId)) != 0:
            return False
        return self.patchLocation(locationId, {"$set": {"status": "DELETED"}})

    def patchLocation(self, locationId, changes: dict):
        result = self.rentalDb["User"].find_one_and_update({"_id": ObjectId(locationId)}, changes)
        return result is not None

    def serviceCar(self, carId, userId, locationId, description=""):  # TODO: remove $set from patch car
        service = {"dateStart": datetime.utcnow(),
                   "leftBy": ObjectId(userId),
                   "location": ObjectId(locationId),
                   "description": description}
        if self.patchCar(ObjectId(carId), {{"$push": {"services": service}},
                                           {"$set": {"status": "SERVICE"}}}):
            service["carId"] = carId
            return Service.from_dict(convertObjectIdsToStr(service))
        return None  # TODO: set client balance

    def endService(self, service: Service):
        service = self.rentalDb["Car"].find_one_and_update(
            {"_id": ObjectId(service.carId), "services._id": ObjectId(service._id)},
            {"$set": {"services.$.dateEnd": datetime.utcnow(), "status": "ACTIVE"}})
        return service is not None

    def getService(self, serviceId):
        car = self.rentalDb["Car"].find_one({"services": {"$elemMatch": {"services._id": ObjectId(serviceId)}}})
        if car is None:
            return None
        for service in car["services"]:
            if service["_id"] == ObjectId(serviceId):
                service = Service.from_dict(convertObjectIdsToStr(service))
                service.carId = car["_id"]
                return service
        return None

    def getServicesHistory(self, carId):
        services = []
        car = self.rentalDb["Car"].find_one({"_id": ObjectId(carId)})
        if car is None:
            return services
        for service in car["services"]:
            service = Service.from_dict(convertObjectIdsToStr(service))
            service.carId = car["_id"]
            services.append(service)
        return services

    def setNewBalance(self, user_id, new_balance) -> bool:
        """
        :param user_id:
        :param new_balance:
        :returns True if success, false if not
        """
        return self.patchUser(user_id, {"$set": {"balance": "new_balance"}})

    def getBalance(self, user_id) -> int:
        """

        :rtype: int
        :returns positive balance if success, -1 if not success
        """
        try:
            balance = self.rentalDb["User"].find_one({"_id": ObjectId(user_id)})["balance"]
        except Exception as _:
            balance = -1
        return balance

    def isUserWithEmailInDB(self, email) -> bool:
        user = self.rentalDb["User"].find_one({"email": email})
        return user is not None

    def isUserWithLoginInDB(self, login) -> bool:
        user = self.rentalDb["User"].find_one({"login": login})
        return user is not None

    def addCar(self, car: 'dict'):
        result = self.rentalDb["Car"].insert_one({
            "brand": car["brand"],
            "vin": car["vin"],
            "regCountryCode": car["regCountryCode"],
            "regNumber": car["regNumber"],
            "modelName": car["model"],
            "seats": car["seats"],
            "lastUsed": datetime.utcnow(),
            "chargeLevel": car["charge"],
            "mileage": car["mileage"],
            "currentLocationLat": car["locationLat"],
            "currentLocationLong": car["locationLong"],
            "lastUpdateTime": datetime.utcnow(),
            "status": car["status"],
            "activationCost": car["activationCost"],
            "kmCost": car["kmCost"],
            "timeCost": car["timeCost"],
            "esimNumber": car["esimNumber"],
            "esimImei": car["esimImei"],
        })
        return convertObjectIdsToStr(result.inserted_id)

    def getServicesForLocation(self, locationId):
        pass

    def getUserToken(self, userId: str):
        pass


RENTAL_DB = MongoDBInterface()
if DB_TESTS:
    print(type(RENTAL_DB.registerUser("asd", "asd", "asddddd", "asd", "asd", "asd", "asd")))
    print(type(RENTAL_DB.getUser(ObjectId("61a27e387ba5e03ad3acca39"))._id))
    print("aaa")
    print(RENTAL_DB.getAccountStatus("61a27e387ba5e03ad3acca39"))
    print(RENTAL_DB.setAccountStatus(ObjectId("61a27e387ba5e03ad3acca39"), "ACTIVE"))
    print(RENTAL_DB.getAccountStatus(ObjectId("61a27e387ba5e03ad3acca39")))
    print(RENTAL_DB.getActivationToken(ObjectId("61a27e387ba5e03ad3acca39")))
    print(RENTAL_DB.setActivationToken(ObjectId("61a27e387ba5e03ad3acca39"), "aasdasd"))
    print(RENTAL_DB.getActivationToken(ObjectId("61a27e387ba5e03ad3acca39")))
    print(RENTAL_DB.changePassword(ObjectId("61a27e387ba5e03ad3acca39"), "dsad"))
    print(RENTAL_DB.rentalHistory(ObjectId("61a27e387ba5e03ad3acca39"), 0, 1))
    # print(RENTAL_DB.addCard(ObjectId("61a27e387ba5e03ad3acca39"), CreditCard("123123123", "123123", "2022-11-02","asdasd", "asdasd")))
    for card in RENTAL_DB.getCards(ObjectId("61a27e387ba5e03ad3acca39")):
        print(card._id)
    print(RENTAL_DB.getCard("61a27e387ba5e03ad3acca39", "61a2834a7ba5e03ad3acca43"))
    # print(RENTAL_DB.deleteCard(ObjectId("61a27e387ba5e03ad3acca39")))
    print(RENTAL_DB.browseNearestCars(("51.067883", "16.973298"), 2000))
