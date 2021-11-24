from backend.models.car import Car
from backend.models.location import Location
from backend.models.user import User


class DatabaseInterface:

    def authUser(self, login, password):
        pass

    def registerUser(self, name: str, surname: str, gender: str, login: str, password: str, address: str, email: str,
                     pesel: str):
        pass

    def getUserToken(self, userId: str):
        pass

    def getAccountStatus(self, userId: str):
        pass

    def getActivationToken(self, userId: str):
        pass

    def activateAccount(self, userId: str):
        pass

    def getUser(self, userId):
        pass

    def changePassword(self, userId, oldPwd, newPwd):
        pass

    def updateLocation(self, userId, location: tuple[str, str]):
        pass

    def rentalHistory(self, userId, pageIndex, pageLength):
        pass

    def getCards(self, userId):
        pass

    def addCard(self, userId, cardNumber, expirationDate, cardHolder, holderAddress):
        pass

    def deleteCard(self, userId, cardId):
        pass

    def browseNearestCars(self, location: tuple[str, str], distance) -> list['Car']:
        pass

    def browseNearestLocations(self, location: tuple[str, str], distance) -> list['Location']:
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
