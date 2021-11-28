from models import *


class DatabaseInterface:

    def __init__(self, **kwargs):
        """
        Here, we should pass login, password, and stuff like urls
        :param kwargs:
        """
        pass

    def initDatabase(self):
        """
        I add these things, because we need some initializations to do inside
        """
        pass

    def authUser(self, login, password):
        """
        :param login:
        :param password:
        :return None if not authorized, user_id if authorized
        """
        pass

    def registerUser(self, name: str, surname: str, login: str, password: str, address: str, email: str, pesel: str):
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

    def getAccountStatus(self, userId: str):
        """

        :param userId:
        :return Current status of the account as a str, or None if any error
        """
        pass

    def getActivationToken(self, userId: str):
        """

        :param userId:
        :return None if there is no token, or token of activation
        """
        pass

    def setAccountStatus(self, userId: str, status:str):
        """

        :param token:
        :return true if account activated, false if not
        """
        pass

    def getUser(self, userId) -> User:
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

    def changePassword(self, userId, newPwd):
        pass

    def updateLocation(self, carId, location: tuple[str, str]) -> bool:
        """
        :param carId:
        :param location: Tuple in form Latitude, Longitude
        :returns True if success false if not
        """
        pass  # TODO: useless?

    def rentalHistory(self, userId, pageIndex, pageLength):
        pass

    def getCards(self, userId):
        pass

    def addCard(self, userId, card: CreditCard) -> bool:
        """
        :param card Card object
        :returns True if succesfull, false if not
        """
        pass

    def deleteCard(self, userId, cardId):
        pass

    def browseNearestCars(self, location: tuple[str, str], distance) -> list["Car"]:
        """

        :param location: tuple, first location is Longitude, second is Latitude
        :param distance: this is already validated
        :returns list of cards. Can be empty. None if any error occured
        """
        pass

    def browseNearestLocations(
            self, location: tuple[str, str], distance
    ) -> list["Location"]:
        """

        :param location: tuple, first one is lat, second one is long
        :param distance:
        """
        pass

    def getCar(self, carId) -> Car:
        """

        :param carId:
        :return None if car not found, Car if found
        """
        pass

    def getLocation(self, locationId) -> Location:
        """

        :param locationId:
        :returns None if location not found, Location if found
        """
        pass

    def getReservation(self, userId, reservationId) -> Reservation:
        """

        :param userId:
        :param reservationId:
        :returns None if any error or validation error, Reservation if its okey
        """
        pass

    def endReservation(self, reservation: Reservation) -> bool:
        """

        :param reservation: Reservation object, ready to stripped and put into DB
        :return True if success, false if not
        """
        pass

    def startReservation(self, reservation: Reservation) -> str:
        """
        Chek here, if there is no pending reservation
        :param reservation: Reservation object, ready to stripped and put into DB
        :return Reservation id, or None
        """
        pass

    def startRental(self, userId, rent: Rental) -> None:
        """
        Check here, if there is no pending rental
        :param userId: User ID
        :param rent: Already calculated Rental. Only strip down Client_id
        :returns rentalID if success, None if failed
        """
        pass

    def getRental(self, userId, rentalId) -> Rental:
        """

        :param userId:
        :param rentalId:
        :returns Rental if found, None if not
        """
        pass

    def endRental(self, rent: Rental) -> bool:
        """

        :param rent: Already calculated and ready to be archived rental
        :returns True if success, False if not
        """
        pass

    def getCars(self, pageIndex, pageCount, location: tuple[str, str], distance):
        pass

    def addCar(self, carDict: 'dict'):
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

    def getUserRentalHistory(self, userId, pageIndex, pageLength) -> list[Rental]:
        """
        :param userId: id of user
        :param pageIndex: a page number
        :param pageLength: length of the page
        :returns List can be returned empty, if there is no Rental in this category
        """
        pass

    def addLocation(self, location: dict) -> bool:
        pass

    def getLocations(self, pageIndex, pageCount, location: tuple[str, str], distance):
        pass

    def deleteLocation(self, locationId):
        pass

    def patchLocation(self, locationId, changes: dict):
        pass

    def serviceCar(self, carId, userId, locationId, description="") -> str:
        """
        :param carId:
        :param userId:
        :param serviceId:
        :returns ID of the created service, None if any error
        """
        pass

    def endService(self, service:Service) -> bool:
        """

        :param serviceId:
        :returns True if successfull, False if not found or no Service
        """
        pass

    def getService(self, serviceId) -> Service:
        """

        :param serviceId:
        :returns None if error or not found, Service if found
        """
        pass

    def getServicesHistory(self, carId) -> list[Service]:
        """

        :param carId:
        :returns Can be empty
        """
        pass

    def getCard(self, user_id, card_id) -> CreditCard:
        """

        :param user_id:
        :param card_id:
        :returns None if card not found or card is not a user card, CreditCard if it's okey
        """
        pass

    def setNewBalance(self, user_id, new_balance) -> bool:
        """
        :param user_id:
        :param new_balance:
        :returns True if success, false if not
        """
        pass

    def getBalance(self, user_id) -> int:
        """

        :rtype: int
        :returns positive balance if success, -1 if not success
        """
        pass

    def isUserWithEmailInDB(self, email) -> bool:
        pass

    def isUserWithLoginInDB(self, login) -> bool:
        pass
    
    def getServicesForLocation(self, locationId):
        pass
    