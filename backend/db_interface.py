from backend.models_old.car import Car
from backend.models_old.location import Location
from backend.models_old.user import User


class DatabaseInterface:

    def authUser(self, login, password):
        """
        :param login:
        :param password:
        :return None if not authorized, user_id if authorized
        """
        pass

    def isUserWithEmailInDB(self, email) -> bool:
        """

        :param email:
        :return True if there is a user with this email, false if not 
        """
        pass

    def isUserWithLoginInDB(self, login) -> bool:
        """
        :return True if there is an user with this login, false if not
        """
        pass

    def registerUser(self, name: str, surname: str, gender: str, login: str, password: str, address: str, email: str,
                     pesel: str) -> str:
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
        pass

    def getUserToken(self, userId: str):
        pass

    def getAccountStatus(self, userId: str) -> str:
        """

        :param userId:
        :return Current status of the account as a str, or None if any error
        """
        pass

    def getActivationToken(self, userId: str) -> str:
        """

        :param userId:
        :return None if there is no token, or token of activation
        """
        pass

    def activateAccount(self, token: str) -> bool:
        """

        :param token:
        :return true if account activated, false if not
        """
        pass

    def getUser(self, userId) -> 'User':
        """

        :param userId:
        :return User, or None if any error
        """
        pass

    def setActivationToken(self, userId: int, token: str) -> bool:
        """

        :param userId:
        :param token: 6 digits pin
        :return true if successful, false if not

        """
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
