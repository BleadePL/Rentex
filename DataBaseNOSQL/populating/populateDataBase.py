import random
import string
import datetime
from cryptography.fernet import Fernet
from datetime import timedelta

key = b'OuEWaMtiLkNuedzPZQsMnnOwhXm4KDoNm-FkWscoNkA='
cipher_suite = Fernet(key)

def generateCars(howMany:int):
    retList = []
    brands = ['Mercedes', 'BMW', 'Volkswagen', 'KIA', 'Hyundai', 'FIAT', 'Porsche']
    modelNames = ['Passat', 'golf', 'i30', 'i20', 'focus', 'fiesta', 'kangoo', '330i', '520d', 'sls', 'sla', 'cls', 'optima', '911', 'cayman', 'punto', '500']
    status = ['ACTIVE']*5 + ['RESERVED','SERVICE', 'INUSE', 'INACTIVE', 'UNKNOWN']
    for _ in range(howMany):
        retList.append({
            'brand': brands[random.randint(0, len(brands)-1)],
            'vin': ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(17)),
            'regCountryCode': 'PL',
            'regNumber': ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)),
            'modelName': modelNames[random.randint(0, len(modelNames)-1)],
            'seats': random.randint(0, 5),
            'chargeLevel': random.randint(10, 100),
            'mileage': random.randint(0, 300000),
            'currentLocationLat':str(round(random.uniform(51.067883, 51.149147), 6)),
            'currentLocationLong':str(round(random.uniform(16.973298, 17.106507), 6)),
            'status':status[random.randint(0, len(status)-1)],
            'activationCost':str(round(random.uniform(1.00, 4.50), 2)),
            'kmCost':str(round(random.uniform(0.70, 2.50), 2)),
            'timeCost':str(round(random.uniform(0.70, 2.50), 2)),
            'esimNumber':''.join(random.choice(string.digits) for _ in range(10)),
            'esimImei':''.join(random.choice(string.digits) for _ in range(10)),
        })
    return retList



def generateUsers(howMany:int):
    retList = []
    balances = ['0.00', '2.59']
    accountTypes = ["PERSONAL", "COMPANY", "ORGANISATION", "UNKNOWN"]
    statuses = ["ACTIVE"]*8 +["INACTIVE","DOCUMENTS","PENDING","PAYMENT","LOCKED","DELETED"]
    roles = ["SERWISANT", "ADMIN"] + ["CLIENT"]*10
    for _ in range(howMany):
        retList.append({
            'pesel': ''.join(random.choice(string.digits) for _ in range(11)),
            'name': ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(5, 30))),
            'surname': ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(5, 30))),
            'addres': ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(5, 255))),
            'driverLicenceNumber': ''.join(random.choice(string.digits) for _ in range(11)),
            'driverLicenceExpirationDate':  datetime.datetime.now() + timedelta(days=random.randint(1, 10)*365),
            'balance': balances[random.randint(0, len(balances)-1)],
            'login': ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(5, 20))),
            'password': cipher_suite.encrypt(bytes(''.join(random.choice(string.ascii_letters + string.punctuation + string.ascii_lowercase) for _ in range(random.randint(5, 40))), encoding='utf8')),
            'email': '256349@student.pwr.edu.pl',
            'accountType': accountTypes[random.randint(0, len(accountTypes)-1)],
            'status':  statuses[random.randint(0, len(statuses)-1)],
            'role':  roles[random.randint(0, len(roles)-1)],
        })
    return retList

def generateCreditCards(howMany:int):
    retList = []
    for _ in range(howMany):
        retList.append({
            'cardNumber': ''.join(random.choice(string.digits) for _ in range(11)),
            'expirationDate': datetime.datetime.now() + timedelta(days=random.randint(1, 10)*365),
            'cardHolderName': ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(5, 30))) + " " + ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(5, 30))),
            "cardHolderAddress":''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(5, 255))),
        })
    return retList

def generateLocations(howMany:int):
    retList = []
    locationTypes = ["STATION","CLEAN","SERVICE","SPECIAL_POINT","UNKNOWN"]
    for _ in range(howMany):
        retList.append({
            'locationType':locationTypes[random.randint(0, len(locationTypes)-1)],
            'locationAddress':''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(5, 255))),
            'leaveReward':str(round(random.uniform(20.00, 50.00), 2)),
            'locationLat':str(round(random.uniform(51.067883, 51.149147), 6)),
            'locationLong':str(round(random.uniform(16.973298, 17.106507), 6)),
        })
    return retList

def populateDataBase(howManyCars, howManyUsers, howManyCreditCards, howManyLocations):
    from pymongo import MongoClient
    client = MongoClient(port=27017)
    db=client.mongodb

    cars = generateCars(howManyCars)
    users = generateUsers(howManyUsers)
    creditCards = generateCreditCards(howManyCreditCards)
    locations = generateLocations(howManyLocations)

    print(cars)
    print(users)
    print(creditCards)
    print(locations)
    for car in cars:
        db.Car.insert_one(car)
    for user in users:
        db.User.insert_one(user)
    for cc in creditCards:
        db.CreditCard.insert_one(cc)
    for location in locations:
        db.Location.insert_one(location)
