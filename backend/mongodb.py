import traceback

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
                "balance": "00.00",
                "accountType": "PRIVATE",
                "activationCode": "",
                "status": "INACTIVE",
                "role": "CLIENT",
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
        try: 
            return userStatus["status"]
        except:
            return None

    def getActivationToken(self, userId: str):
        """

        :param userId:
        :return None if there is no token, or token of activation
        """
        activationToken = self.rentalDb["User"].find_one(
            {"_id": ObjectId(userId)},
            {"activationCode": 1}
        )
        try: 
            return activationToken["activationCode"]
        except:
            return None

    def setAccountStatus(self, userId: str, status: str):
        """

        :param token:
        :return true if account activated, false if not
        """
        if status not in ["ACTIVE", "INACTIVE", "DOCUMENTS", "PENDING", "PAYMENT", "LOCKED", "DELETED"]:
            return False
        result = self.rentalDb["User"].update_one({"_id": ObjectId(userId)}, {'$set': {"status": status}})
        return result.modified_count == 1

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
        return result.modified_count != 0

    def changePassword(self, userId, newPwd):
        result = self.rentalDb["User"].update_one(
            {"_id": ObjectId(userId)},
            {'$set': {"password": bcrypt.hashpw(newPwd.encode('utf8'), salt)}})
        return result.modified_count != 0

    def updateLocation(self, carId, location):
        result = self.rentalDb["Car"].update_one(
            {"_id": ObjectId(carId)},
            {'$set': {"currentLocationLat": location[0], "currentLocationLong": location[1]}})
        return result.modified_count != 0

    def rentalHistory(self, userId, pageIndex, pageLength):
        rentals = []
        try:
            for rentalId in self.rentalDb["User"].find_one({"_id": ObjectId(userId)})["rentalArchive"]:
                rental = self.rentalDb["RentalArchive"].find_one({"_id": ObjectId(rentalId)})
                if rental is not None:
                    rentals.append(Rental.from_dict(convertObjectIdsToStr(rental)))
        except:
            return rentals
        return rentals[pageIndex:pageIndex + pageLength]

    def getCards(self, userId):
        cards = []
        try:
            for card in self.rentalDb["User"].find_one({"_id": ObjectId(userId)}, {"creditCards": 1})["creditCards"]:
                cards.append(CreditCard.from_dict(convertObjectIdsToStr(card)))
        except:
            return cards
        return cards

    def addCard(self, userId, card: CreditCard):
        result = self.rentalDb["User"].update_one({"_id": ObjectId(userId)}, {'$push': {"creditCards": {
            "_id": ObjectId(),
            "cardNumber": card.cardNumber,
            "expirationDate": card.expirationDate,
            "cardHolderName": card.cardHolderName,
            "cardHolderAddress": card.cardHolderAddress
        }}})  # TODO: encrypt CC
        return result.modified_count != 0

    def deleteCard(self, userId, cardId):
        result = self.rentalDb["User"].update_one({"_id": ObjectId(userId)}, {'$pull': {"creditCards": {
            "_id": ObjectId(cardId)
        }}})
        return result.modified_count != 0

    def browseNearestCars(self, location, distance):
        cars = []
        for car in self.rentalDb["Car"].find({"status": {"$nin": ["DELETED"]}}):
            if calculate_gps_distance((float(location[0]), float(location[1])),
                                      (float(car["currentLocationLat"]),
                                       float(car["currentLocationLong"]))) <= int(distance):
                cars.append(Car.from_dict(convertObjectIdsToStr(car)))
        return cars

    def browseNearestLocations(
            self, location, distance
    ):
        locations = []
        for location_ in self.rentalDb["Location"].find({"status": {"$nin": ["DELETED"]}}):
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
        if reservation is None or "reservation" not in reservation or reservation["reservation"]["_id"] != ObjectId(
                reservationId):
            return None
        result = Reservation.from_dict(convertObjectIdsToStr(reservation["reservation"]))
        result.userId = userId
        return result

    def endReservation(self, reservation: Reservation):
        reservation_ = self.rentalDb["User"].find_one({"_id": ObjectId(reservation.userId)}, {"reservation": 1})
        if reservation_ is None or reservation_["reservation"]["_id"] != ObjectId(reservation._id):
            return False
        a = self.rentalDb["User"].find_and_modify({"_id": ObjectId(reservation.userId)},
                                                  {'$unset': {"reservation": ""}})
        b = self.rentalDb["Car"].find_and_modify({"_id": ObjectId(reservation_["reservation"]["carId"])},
                                                 {'$set': {"status": "ACTIVE"}})
        return True

    def startReservation(self, reservation: Reservation):
        try:
            if self.rentalDb["Car"].find_one({"_id": ObjectId(reservation.carId)})["status"] != "ACTIVE":
                return None
        except:
            return None
        user = self.rentalDb["User"].find_one({"_id": ObjectId(reservation.userId)})
        if ("status" in user and user["status"] != "ACTIVE") or (
                "currentRental" in user and user["currentRental"] != "") or (
                "reservation" in user and user["reservation"] != ""):
            return None
        id = ObjectId()
        self.rentalDb["User"].find_and_modify({"_id": ObjectId(reservation.userId)},
                                              {"$set": {"reservation": {
                                                  "_id": id,
                                                  "reservationStart": reservation.reservationStart,
                                                  "reservationsEnd": reservation.reservationEnd,
                                                  "carId": ObjectId(reservation.carId)
                                              }}})
        self.rentalDb["Car"].find_and_modify({"_id": ObjectId(reservation.carId)},
                {"$set": {"status": "RESRVED"}})
        return convertObjectIdsToStr(id)

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
        if user.status != "ACTIVE" or (user.currentRental is not None and user.currentRental != ""):
            return None
        # if they have a reservation, end it
        if user.reservation is not None and user.reservation != "":
            self.endReservation(user.reservation)  # TODO: save reservation in user as object
        # add the rental

        rentalId = ObjectId()
        if self.rentalDb["User"].find_one_and_update({"_id": ObjectId(userId)}, {"$set": {"currentRental": {
            '_id': rentalId,
            'rentalStart': datetime.utcnow(),
            'mileage': car.mileage,
            'ended': False,
            'carId': ObjectId(carId)}}}) is None:
            return None
        self.rentalDb["Car"].find_one_and_update({"_id": ObjectId(carId)},
                {"$set": {"status": "INUSE"}})
        return convertObjectIdsToStr(rentalId)

    def getRental(self, userId, rentalId):
        user: User = self.getUser(userId)
        if user is None:
            return None
        if user.currentRental is not None and user.currentRental != "":
            try:
                if user.currentRental["_id"] == rentalId:
                    rental = Rental.from_dict(convertObjectIdsToStr(user.currentRental))
                    rental.renter = userId
                    return rental
            except:
                pass
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
        try:
            if user.currentRental["carId"] != rental.carId:
                return False
        except Exception as ex:
            traceback.print_tb(ex.__traceback__)
            return False
        # update everything in the rental
        rent.rentalEnd = datetime.utcnow()
        # rental.mileage = car.mileage - rental.mileage
        # rental.totalCost = (rental.mileage * car.kmCost +
        #                     (rental.rentalEnd - rental.rentalStart).total_seconds() / 60.0)
        # rental.ended = True
        # update car
        self.rentalDb["Car"].find_one_and_update({"_id": ObjectId(car._id)},
                {"$set": {"lastUsed": rental.rentalEnd, "status": "ACTIVE"}})
        # update user
        self.rentalDb["User"].find_one_and_update({"_id": ObjectId(user._id)},
                {"$set": {"currentRental": ""}})
        # move rental to RentalArchive
        self.rentalDb["RentalArchive"].insert_one({
            "_id": ObjectId(rent._id),
            "rentalStart": rent.rentalStart,
            "rentalEnd": rent.rentalEnd,
            "mileage": rent.mileage,
            "totalCost": rent.totalCost,
            "ended": rent.ended,
            "carId": ObjectId(rent.carId),
            "renter": ObjectId(rent.renter)
        })
        return True

    def getCars(self, pageIndex, pageCount, location, distance):
        cars = self.browseNearestCars(location, distance)
        if cars is None:
            return None
        return cars[int(pageIndex): int(pageIndex) + int(pageCount)]

    def deleteCar(self, carId):
        result = self.rentalDb["Car"].find_one_and_update({"_id": ObjectId(carId)},
                {"$set": {"status": "DELETED"}})
        return result is not None

    def patchCar(self, carId, changes: dict):
        if any(change in changes for change in ["chargeLevel", "mileage", "currentLocationLat", "currentLocationLong"]):
            changes["lastUpdateTime"] = datetime.utcnow()
        result = self.rentalDb["Car"].find_one_and_update({"_id": ObjectId(carId)}, {"$set": changes}, upsert=True)
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
            {"email": {"$regex": filter}}]}).skip(pageIndex).limit(pageCount):
            users.append(User.from_dict(convertObjectIdsToStr(user)))
        return users

    def deleteUser(self, userId):
        result = self.rentalDb["User"].find_one_and_update({"_id": ObjectId(userId)},
                                                           {"$set": {"status": "DELETED"}})
        return result is not None

    def patchUser(self, userId, changes: dict):
        result = self.rentalDb["User"].find_one_and_update({"_id": ObjectId(userId)}, {"$set": {changes}})
        return result is not None

    def getUserRentalHistory(self, userId, pageIndex, pageLength):
        rentals = []
        for rental in self.rentalDb["RentalArchive"].find({"renter": ObjectId(userId)}
                                                          ).skip(int(pageIndex)).limit(int(pageLength)):
            rentals.append(Rental.from_dict(convertObjectIdsToStr(rental)))
        return rentals # convert to using users rental hisstory ? 

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

    def getLocations(self, pageIndex, pageCount, location, distance):
        locations = self.browseNearestLocations(location, distance)
        if locations is None:
            return None
        return locations[int(pageIndex): int(pageIndex) + int(pageCount)]

    def deleteLocation(self, locationId):
        return self.rentalDb["Location"].find_one_and_update({"_id": ObjectId(locationId)},
                                                             {"$set": {"status": "DELETED"}}) is not None

    def patchLocation(self, locationId, changes: dict):
        result = self.rentalDb["User"].find_one_and_update({"_id": ObjectId(locationId)}, {"$set": changes})
        return result is not None

    def serviceCar(self, carId, userId, locationId, description="") -> str:
        serviceId = ObjectId()
        service = {
            "_id": serviceId,
            "dateStart": datetime.utcnow(),
            "leftBy": ObjectId(userId),
            "location": ObjectId(locationId),
            "description": description}
        if self.rentalDb["Car"].find_one_and_update({"_id": ObjectId(carId)}, {
            "$push": {"services": service},
            "$set": {"status": "SERVICE"}}) is None:
            return None
        service["carId"] = carId
        return convertObjectIdsToStr(serviceId)

    def endService(self, service: Service):
        service = self.rentalDb["Car"].find_one_and_update(
            {"_id": ObjectId(service.carId), "services._id": ObjectId(service._id)},
            {"$set": {"services.$.dateEnd": datetime.utcnow(), "status": "ACTIVE"}})
        return service is not None # TODO: czy to dziala? (czy nie modyfikuje kazdego servicu)

    def getService(self, serviceId):
        try:
            car = self.rentalDb["Car"].find_one({"services": {"$elemMatch": {"_id": ObjectId(serviceId)}}})
            if car is None:
                return None
            for service in car["services"]:
                if service["_id"] == ObjectId(serviceId):
                    service = Service.from_dict(convertObjectIdsToStr(service))
                    service.carId = convertObjectIdsToStr(car["_id"])
                    return service
            return None
        except Exception as ex:
            print("Exception occured " + str(ex))
            return None

    def getServicesHistory(self, carId):
        services = []
        car = self.rentalDb["Car"].find_one({"_id": ObjectId(carId)})
        if car is None:
            return services
        if "services" not in car:
            return services
        for service in car["services"]:
            service = Service.from_dict(convertObjectIdsToStr(service))
            service.carId = convertObjectIdsToStr(car["_id"])
            services.append(service)
        return services

    def setNewBalance(self, user_id, new_balance) -> bool:
        """
        :param user_id:
        :param new_balance:
        :returns True if success, false if not
        """
        return self.rentalDb["User"].find_one_and_update({"_id": ObjectId(user_id)},
                {"$set": {"balance": new_balance}}) is not None

    def getBalance(self, user_id) -> str:
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
            "chargeLevel": car["charge"],
            "mileage": car["mileage"],
            "currentLocationLat": car["locationLat"],
            "currentLocationLong": car["locationLong"],
            "status": car["status"],
            "activationCost": car["activationCost"],
            "kmCost": car["kmCost"],
            "timeCost": car["timeCost"],
            "esimNumber": car["esimNumber"],
            "esimImei": car["esimImei"]
        })
        return convertObjectIdsToStr(result.inserted_id)

    def getServicesForLocation(self, locationId):
        pass

    def getUserToken(self, userId: str):
        pass

    def dropCars(self):
        self.rentalDb["Car"].delete_many({})

    def dropRentalArchive(self):
        self.rentalDb["RentalArchive"].delete_many({})

    def dropUsers(self):
        self.rentalDb["User"].delete_many({})

    def dropLocations(self):
        self.rentalDb["Loation"].delete_many({})

    def userCleanup(self, user_id):
        user = self.getUser(user_id)
        self.rentalDb["User"].update_one({"_id": ObjectId(user._id)},
                                         {"$set": {"status": "ACTIVE", "currentRental": "", "rentalArchive": []}})

    def carCleanup(self, car_id):
        car = self.getCar(car_id)
        self.rentalDb["User"].update_one({"_id": ObjectId(car_id)},
                                         {"$set": {"status": "ACTIVE", "currentRental": "", "services": []}})


RENTAL_DB = MongoDBInterface()

print(RENTAL_DB.getService('61a6056023ca31a582edd581'))
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
