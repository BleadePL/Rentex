import io
from time import sleep

from flask.testing import FlaskClient

from backend.models import Location
from backend.utils import pln_gr_to_gr
from flask_main import app, RENTAL_DB, MIDDLE_LAT, MIDDLE_LONG
import json

TEST_FUNCTIONS = []


def test(args):
    TEST_FUNCTIONS.append(args)
    return args
    pass


class Tests:
    def __init__(self, client):
        self.client: FlaskClient = client
        self.session_token = ""
        self.prepareDatabases()

    @test
    def prepareDatabases(self):
        RENTAL_DB.dropRentalArchive()
        RENTAL_DB.dropCars()
        RENTAL_DB.dropLocations()
        RENTAL_DB.dropUsers()

        user_id = RENTAL_DB.registerUser(name="Fryderyk", surname="Markowski", login="test", password="test",
                                         address="21 października 3020", email="mateusz@gmail.com", pesel="60060535351")
        assert user_id is not None
        assert RENTAL_DB.setAccountStatus(user_id, "ACTIVE")
        assert RENTAL_DB.getUser(user_id).status == "ACTIVE"

        locationId = RENTAL_DB.addLocation(
            Location(name="ORLEN", location_lat=MIDDLE_LAT, location_long=MIDDLE_LONG, location_type="STATION",
                     location_reward="10.30", location_address="17 stycznia", status="ACTIVE"))
        assert locationId is not None

    @test
    def runLoginTest(self):
        rv = (self.client.post("/login/login", data=json.dumps({
            "login": "test",
            "password": "test"
        }), content_type='application/json'))
        assert rv.status == "200 OK"
        j = json.loads((rv.data).decode("utf-8"))
        assert "token" in j
        self.session_token = j["token"]

    @test
    def runLogoutTest(self):
        assert self.session_token != ""
        rv = self.client.post("/login/logout", content_type='application/json',
                              headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"
        self.session_token = ""
        print(rv.data)
        self.runLoginTest()
        assert self.session_token != ""

    @test
    def runGetUserTest(self):
        assert self.session_token != ""
        rv = self.client.get("/user/details", content_type='application/json',
                             headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"

    @test
    def runStatusTest(self):
        rv = self.client.get("/login/status", content_type='application/json',
                             headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"
        print(json.loads(rv.data.decode("utf-8")))

    @test
    def runRegisterTest(self):
        rv = self.client.post("/login/register", data=json.dumps({"name": "Imie",
                                                                  "surname": "Nazwisko",
                                                                  "login": "Nowy_login",
                                                                  "password": "test",
                                                                  "address": "Dziwny adres",
                                                                  "email": "innymmail@gmail.com",
                                                                  "pesel": "45236346334"}),
                              content_type='application/json')
        print(rv.data)
        assert rv.status == "200 OK"
        j = json.loads(rv.data.decode("utf-8"))
        assert "userId" in j
        rv = self.client.post("/admin/user/" + j["userId"] + "/activate")
        assert rv.status == "200 OK"
        rv = self.client.delete("/admin/user/" + j["userId"])
        assert rv.status == "200 OK"

    def runActivationTest(self):
        # NAH
        pass

    @test
    def runPhotoUploadTest(self):
        rv = self.client.post("/login/uploadphotos", content_type='multipart/form-data',
                              headers={"Session-Token": self.session_token})
        assert rv.status == "400 BAD REQUEST"
        rv = self.client.post("/login/uploadphotos",
                              data={"front": (open("test_images/front.png", mode="rb"), "front.png"),
                                    "back": (open("test_images/back.png", mode="rb"), "back.png")},
                              content_type='multipart/form-data',
                              headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"

    def runChangePassword(self):
        # NAH
        pass

    @test
    def runCardTest(self):
        rv = self.client.get("/user/cards", headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"
        j = json.loads(rv.data.decode("utf-8"))

        if len(j["cards"]) != 0:
            for c in j["cards"]:
                rv = self.client.delete("/user/card/" + c, headers={"Session-Token": self.session_token})
                assert rv.status == "200 OK"
        rv = self.client.post("/user/cards", data=json.dumps({
            "cardNumber": 4716489133074932,
            "expirationDate": "10/22",
            "cardHolder": "Jan Kowalski",
            "cvv": 123,
            "holderAddress": "17 stycznia 24, 10-100 Warszawa, Polska"
        }),
                              content_type='application/json',
                              headers={"Session-Token": self.session_token})

        assert rv.status == "200 OK"

        rv = self.client.get("/user/cards", headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"
        j = json.loads(rv.data.decode("utf-8"))
        assert len(j["cards"]) > 0
        card_id = (j["cards"])[0]
        print(card_id)
        rv = self.client.get("/user/card/" + card_id, headers={"Session-Token": self.session_token})
        print(rv)
        assert rv.status == "200 OK"
        j = json.loads(rv.data.decode("utf-8"))
        print(j)
        rv = self.client.post("/user/card/" + card_id + "/charge", data=json.dumps({'amount': 50, 'cvv': 134}),
                              headers={"Session-Token": self.session_token}, content_type='application/json')
        assert rv.status == "200 OK"
        print(rv)

    @test
    def testRentalAndSearch(self):
        # get user ID
        rv = self.client.get("/user/details", content_type='application/json',
                             headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"
        j = json.loads(rv.data.decode("utf-8"))
        user_id = j["userId"]

        print("Rental test as user " + j["login"])

        # Remove all cars from system and drop archive
        RENTAL_DB.dropCars()
        RENTAL_DB.dropRentalArchive()
        RENTAL_DB.userCleanup(user_id)

        # Search for cars
        rv = self.client.get("/browse/nearestcars?locationLat=51.111593&locationLong=17.027287",
                             headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"
        j = json.loads(rv.data.decode("utf-8"))
        length = len(j["cars"])

        exists = False
        for c in j["cars"]:
            if c["regNumber"] == "DW112233":
                rv = self.client.delete("/admin/car/" + c["carId"])
                assert rv.status == "200 OK"
                break

        # Add car
        if not exists:
            rv = self.client.post("/admin/car", data=json.dumps({
                "brand": "Toyota",
                "regNumber": "DW112233",
                "regCountryCode": "PL",
                "model": "Yaris 1.0",
                "seats": 5,
                "charge": 100,
                "activationCost": "10.30",
                "kmCost": "1.30",
                "timeCost": "0.30",
                "locationLat": "51.111493",
                "locationLong": "17.027187",
                "status": "ACTIVE",
                "vin": "ASDSGFA123123123",
                "mileage": 125123123,
                "esimNumber": 125123123,
                "esimImei": "125123123"
            }), content_type='application/json')
            assert rv.status == "200 OK"
            print("CAR ADDED")

        # Search for this car
        rv = self.client.get("/browse/nearestcars?locationLat=51.111593&locationLong=17.027287",
                             headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"
        j = json.loads(rv.data.decode("utf-8"))
        assert len(j["cars"]) + 1 > length
        car = j["cars"][0]

        print("Using car " + car["brand"] + " " + car["model"] + " -> " + car["carId"])


        # check if client has not reservation
        rv = self.client.get("/rent/reservate", headers={"Session-Token": self.session_token})
        if rv.status == "200 OK":
            rv = self.client.delete(
                "/admin/forcecleanreservation/" + json.loads(rv.data.decode("utf-8"))["reservation"][
                    "_id"] + "/" + user_id, headers={"Session-Token": self.session_token})
            assert rv.status == "200 OK"

        # Check if there is no rental
        rv = self.client.get("/rent/rent", headers={"Session-Token": self.session_token})
        if rv.status == "200 OK":
            print(rv.data)
            j = (json.loads(rv.data.decode("utf-8")))["rental"]
            rv = self.client.delete("/admin/forcecleanrental/" + j["_id"] + "/" + user_id,
                                    headers={"Session-Token": self.session_token})
            assert rv.status == "200 OK"

        # Reservate car
        rv = self.client.post("/rent/reservate", data=json.dumps({"carId": car["carId"]}),
                              headers={"Session-Token": self.session_token}, content_type='application/json')
        assert rv.status == "200 OK"
        j = json.loads(rv.data)
        assert "resId" in j
        resId = j["resId"]
        print("Reservation of car " + car["carId"] + " success!")

        # Wait a moment
        print("Let the reservation pass a little bit")
        sleep(3)

        # Get it again
        rv = self.client.get("/rent/reservation/" + resId, headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"
        print("Reservation still active....")

        # Cancel reservation
        rv = self.client.delete("/rent/reservation/" + resId, headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"
        print("Reservation ended!")

        rv = self.client.get("/rent/reservation/" + resId, headers={"Session-Token": self.session_token})
        assert rv.status == "400 BAD REQUEST"
        assert RENTAL_DB.getCar(car["carId"]).status == "ACTIVE"
        print("Yep, reservation don't exists now")

        # Get cards
        rv = self.client.get("/user/cards", headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"
        j = json.loads(rv.data.decode("utf-8"))
        assert len(j["cards"]) != 0
        cardId = j["cards"][0]

        print("Paying for rental with a card " + cardId)

        # Rent the car
        rv = self.client.post("/rent/rent", data=json.dumps({"carId": car["carId"], "cvv": 123, "paymentType": cardId}),
                              headers={"Session-Token": self.session_token}, content_type='application/json')
        assert rv.status == "200 OK"
        j = json.loads(rv.data.decode("utf-8"))
        assert "rentId" in j
        rental = j["rentId"]

        print("Wynajem udał się! " + rental)

        # Get Rental
        rv = self.client.get("/rent/rent", headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"

        # Move car a little bit
        rv = self.client.post("/admin/carpos", data=json.dumps({
            "carid": car["carId"],
            "lat": '51.107209',
            "long": '17.033463'
        }), content_type='application/json')
        assert rv.status == "200 OK"

        # Get Cost
        rv = self.client.get("/rent/rent", headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"
        j = json.loads(rv.data.decode("utf-8"))

        print("Current cost of rental: " + j["rental"]["totalCost"])
        # Gimmie some time!
        print("Drive the CAR")
        sleep(3)

        # Move car some more
        rv = self.client.post("/admin/carpos", data=json.dumps({
            "carid": car["carId"],
            "lat": '51.110358',
            "long": '17.026711'
        }), content_type='application/json')
        assert rv.status == "200 OK"

        # Gimmie some time!
        print("Let the rental have some time")
        sleep(3)

        # Get Cost
        rv = self.client.get("/rent/rent", headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"

        j = json.loads(rv.data.decode("utf-8"))
        print("Current cost of rental: " + j["rental"]["totalCost"])

        print(rental)
        # Finish rental
        rv = self.client.delete("/rent/rent/" + rental, headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"

        # Get it from the archive
        rv = self.client.get("/rent/rent/" + rental, headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"
        j = json.loads(rv.data.decode("utf-8"))
        assert pln_gr_to_gr(j["rental"]["totalCost"]) > 0
        print("Final cost of rental: " + str(j["rental"]["totalCost"]) + "\nDriven " + str(
            float(j["rental"]["mileage"]) / 1000) + " hm")

        # FINISH

    def addCar(self):
        # Add car
        rv = self.client.post("/admin/car", data=json.dumps({
            "brand": "Toyota",
            "regNumber": "DW112233",
            "regCountryCode": "PL",
            "model": "Yaris 1.0",
            "seats": 5,
            "charge": 100,
            "activationCost": "10.30",
            "kmCost": "1.30",
            "timeCost": "0.30",
            "locationLat": "51.111493",
            "locationLong": "17.027187",
            "status": "ACTIVE",
            "vin": "ASDSGFA123123123",
            "mileage": 125123123,
            "esimNumber": 125123123,
            "esimImei": "125123123"
        }), content_type='application/json')
        assert rv.status == "200 OK"
        rv = self.client.get(
            "/admin/car?locationLat=" + MIDDLE_LAT + "&locationLong=" + MIDDLE_LONG + "&pagelength=100&startindex=0&distance=20000")
        assert rv.status == "200 OK"
        j = json.loads(rv.data.decode("utf-8"))
        assert len(j["cars"]) > 0
        return j["cars"][0]

    @test
    def serviceCar(self):
        print("Preparing for Service....")
        rv = self.client.get(
            "/admin/car?locationLat=" + MIDDLE_LAT + "&locationLong=" + MIDDLE_LONG + "&pagelength=100&startindex=0&distance=20000")
        assert rv.status == "200 OK"
        j = json.loads(rv.data.decode("utf-8"))
        assert len(j["cars"]) > 0
        car = j["cars"][0]
        print("Servicing car " + car["brand"] + " " + car["modelName"])

        RENTAL_DB.carCleanup(car["_id"])
        print("Car cleaned up!")

        rv = self.client.get("/service/car/" + car["_id"], headers={"Session-Token": self.session_token},
                             content_type='application/json')
        assert rv.status == "200 OK" or rv.status == "204 NO CONTENT"
        # j = json.loads(rv.data.decode("utf-8"))

        # service car
        print("Startin car service....")
        rv = self.client.post("/service", data=json.dumps({"carId": car["_id"]}),
                              headers={"Session-Token": self.session_token}, content_type='application/json')
        assert rv.status == "200 OK"
        j = json.loads(rv.data.decode("utf-8"))
        assert "serviceId" in j
        service = j["serviceId"]

        rv = self.client.get("/service/" + service, headers={"Session-Token": self.session_token},
                             content_type='application/json')
        assert rv.status == "200 OK"
        print("Car service started!")

        rv2 = self.client.get("/service/car/" + car["_id"], headers={"Session-Token": self.session_token})
        assert rv2.status == "200 OK"
        print("Service in car found!")

        rv = self.client.get("/service/19834jn", headers={"Session-Token": self.session_token})
        assert rv.status == "204 NO CONTENT"
        print("Invalid service not exists!")

        rv = self.client.delete("/service/" + service, headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"
        print("Service end!")
        rv = self.client.get("/service/" + service, headers={"Session-Token": self.session_token},
                             content_type='application/json')
        assert rv.status == "200 OK"
        j = json.loads(rv.data.decode("utf-8"))
        assert j["service"]["dateEnd"] is not None
        print("SERVICE FINISHED")
