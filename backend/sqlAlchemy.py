from backend.db_interface import DatabaseInterface


class SQLAlchemyInterface(DatabaseInterface):
    
    def __init__(self):
        pass

    def authUser(self, login, password):
        pass

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
        pass

    def getAccountStatus(self, userId: str):
        pass

    def getActivationToken(self, userId: str):
        pass

    def setAccountStatus(self, userId: str, status: str):
        pass

    def getUser(self, userId):
        pass

    def setActivationToken(self, userId: int, token: str) -> bool:
        pass

    def changePassword(self, userId, newPwd):
        pass

    def updateLocation(self, carId, location):
        pass

    def rentalHistory(self, userId, pageIndex, pageLength):
        pass

    def getCards(self, userId):
        pass

    def addCard(self, userId, card: CreditCard):
        pass

    def browseNearestCars(self, location, distance):
        pass

    def browseNearestLocations(self, location, distance):
        pass

    def startReservation(self, reservation: Reservation):
        pass

    def startRental(self, userId, carId):
        pass

    def getRental(self, userId, rentalId):
        pass

    def endRental(self, rent: Rental):
        pass

    def getCars(self, pageIndex, pageCount, location, distance):
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

    def getCard(self, userId, cardId):
        pass

    def addLocation(self, location: Location):
        pass

    def getLocations(self, pageIndex, pageCount, location, distance):
        pass

    def deleteLocation(self, locationId):
        pass

    def patchLocation(self, locationId, changes: dict):
        pass

    def serviceCar(self, carId, userId, locationId, description="") -> str:
        pass

    def endService(self, service: Service):
        pass

    def getService(self, serviceId):
        pass

    def getServicesHistory(self, carId):
        pass

    def setNewBalance(self, user_id, new_balance) -> bool:
        pass

    def getBalance(self, user_id) -> str:
        pass

    def isUserWithEmailInDB(self, email) -> bool:
        pass

    def isUserWithLoginInDB(self, login) -> bool:
        pass

    def addCar(self, car: 'dict'):
        pass


    def dropCars(self):
        pass

    def dropRentalArchive(self):
        pass

    def dropUsers(self):
        pass

    def dropLocations(self):
        pass

    def userCleanup(self, user_id):
        pass

    def carCleanup(self, car_id):
        pass
