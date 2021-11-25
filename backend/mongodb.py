from bson import ObjectId
from pymongo import MongoClient
from db_interface import DatabaseInterface
from backend.models.car import Car

HOSTNAME = "vps.zgrate.ovh"
PORT = "27017"
USERNAME = "backend"
PASSWORD = "backendpwd"
DB_NAME = "rental"

client = MongoClient("mongodb://" + USERNAME + ":" + PASSWORD + "@" + HOSTNAME + ":" + PORT + "/", connect=True)


class MongoDBInterface(DatabaseInterface):

    def __init__(self):
        self.rentalDb = client["rental"]

    def getCar(self, carId):
        carDict = self.rentalDb["Car"].find_one({'_id': ObjectId(carId)})
        if carDict is None:
            return None
        return Car.from_dict(carDict)

    def getCars(self, pageIndex, pageCount, location: tuple[str, str], distance):
        cars = []
        for c in self.rentalDb["Car"].find():
            cars.append(Car.from_dict(c))
        return cars


RENTAL_DB = MongoDBInterface()
