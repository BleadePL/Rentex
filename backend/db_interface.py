from backend.models.user import User


class DatabaseInterface:
    def getCars(self):
        pass

    def getCar(self, carId):
        pass

    def getUser(self, userId):
        pass

    def getUserByLoginOrName(self, filter):
        pass

    def authUser(self, login, password):
        pass

    def registerUser(self, user: 'User'):
        pass
