import io
from time import sleep

from flask.testing import FlaskClient

from flask_main import app, RENTAL_DB
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

    # @test
    def runLogoutTest(self):
        assert self.session_token != ""
        rv = self.client.post("/login/logout", content_type='application/json',
                              headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"
        self.session_token = ""
        print(rv.data)
        self.runLoginTest()
        assert self.session_token != ""

    # @test
    def runGetUserTest(self):
        assert self.session_token != ""
        rv = self.client.get("/user/details", content_type='application/json',
                             headers={"Session-Token": self.session_token})
        print(rv)
        assert rv.status == "200 OK"
        print(rv.data)

    # @test
    def runStatusTest(self):
        rv = self.client.get("/login/status", content_type='application/json',
                             headers={"Session-Token": self.session_token})
        print(rv.data)
        assert rv.status == "200 OK"

    # @test
    def runRegisterTest(self):
        rv = self.client.post("/login/register", data=json.dumps({"name": "Fryderyk",
                                                                  "surname": "Markowski",
                                                                  "login": "test",
                                                                  "password": "test",
                                                                  "address": "20;Sienkiewicza;60951;Tarnobrzeg;Polska",
                                                                  "email": "FrydMark11@gmail.com",
                                                                  "pesel": "60060535351"}),
                              content_type='application/json')
        print(rv.data)
        assert rv.status == "200 OK"
        j = json.loads(rv.data.decode("utf-8"))
        assert "userId" in j
        rv = self.client.delete("/admin/user/" + j["userId"])
        assert rv.status == "200 OK"

    def runActivationTest(self):
        # NAH
        pass

    # @test
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

    #@test
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
        assert len(j["cards"]) == 1
        card_id = (j["cards"])[0]
        print(card_id)
        rv = self.client.get("/user/card/" + card_id, headers={"Session-Token": self.session_token})
        print(rv)
        # assert rv.status == "200 OK" TODO
        # j = json.loads(rv.data.decode("utf-8"))
        # print(j)
        rv = self.client.post("/user/card/" + card_id + "/charge", data=json.dumps({'amount': 50, 'cvv': 134}),
                              headers={"Session-Token": self.session_token}, content_type='application/json')
        # assert rv.status == "200 OK"
        print(rv)

    # @test
    def testActivateAccount(self):
        rv = self.client.post("/admin/user/61a4e940edf3e07d79a80e39/activate")
        assert rv.status == "200 OK"

    # @test
    def testRentalAndSearch(self):
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

        # Search for this car
        rv = self.client.get("/browse/nearestcars?locationLat=51.111593&locationLong=17.027287",
                             headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"
        j = json.loads(rv.data.decode("utf-8"))
        assert len(j["cars"]) + 1 > length
        car = j["cars"][0]

        # get user ID
        rv = self.client.get("/user/details", content_type='application/json',
                             headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"

        user_id = json.loads(rv.data.decode("utf-8"))["userId"]
        print(user_id)

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
        print(rv)
        assert rv.status == "200 OK"
        j = json.loads(rv.data)
        assert "resId" in j
        resId = j["resId"]
        print(resId)

        # Wait a moment
        print("Let the reservation pass a little bit")
        sleep(5)

        # Get it again

        rv = self.client.get("/rent/reservation/" + resId, headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"

        # Cancel reservation
        rv = self.client.delete("/rent/reservation/" + resId, headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"

        # Get cards
        rv = self.client.get("/user/cards", headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"
        j = json.loads(rv.data.decode("utf-8"))
        assert len(j["cards"]) != 0
        cardId = j["cards"][0]

        # Rent the car
        rv = self.client.post("/rent/rent", data=json.dumps({"carId": car["carId"], "cvv": 123, "paymentType": cardId}),
                              headers={"Session-Token": self.session_token}, content_type='application/json')
        assert rv.status == "200 OK"
        j = json.loads(rv.data.decode("utf-8"))
        assert "rentId" in j
        rental = j["rentId"]
        print(rental)

        # Get Rental
        rv = self.client.get("/rent/rent", headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"

        # Move car a little bit
        rv = self.client.post("/admin/carpos", data=json.dumps({
            "carid": car["carId"],
            "long": '51.107209',
            "lat": '17.033463'
        }), content_type='application/json')
        assert rv.status == "200 OK"

        # Get Cost
        rv = self.client.get("/rent/rent", headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"
        print(rv.data)

        # Gimmie some time!
        print("Drive the CAR")
        sleep(10)

        # Move car some more
        rv = self.client.post("/admin/carpos", data=json.dumps({
            "carid": car["carId"],
            "long": '51.110358',
            "lat": '17.026711'
        }), content_type='application/json')
        assert rv.status == "200 OK"

        # Gimmie some time!
        print("Let the rental have some time")
        sleep(10)

        # Get Cost
        rv = self.client.get("/rent/rent", headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"
        print(rv.data)

        # Finish rental
        rv = self.client.delete("/rent/rent/" + rental, headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"

        # FINISH

    @test
    def serviceCar(self):
        from flask_main import MIDDLE_LAT, MIDDLE_LONG
        rv = self.client.get(
            "/admin/car?locationLat=" + MIDDLE_LAT + "&locationLong=" + MIDDLE_LONG + "&pagelength=100&startindex=0&distance=20000")
        assert rv.status == "200 OK"
        j = json.loads(rv.data.decode("utf-8"))

        if len(j["cars"]) == 0:
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
        car = j["cars"][0]
        print(car)

        rv = self.client.get("/service/car/" + car["_id"], headers={"Session-Token": self.session_token},
                             content_type='application/json')
        print(rv.status)
        assert rv.status == "200 OK" or rv.status == "204 NO CONTENT"

        # service car
        rv = self.client.post("/service", data=json.dumps({"carId": car["_id"]}),
                              headers={"Session-Token": self.session_token}, content_type='application/json')
        assert rv.status == "200 OK"
        j = json.loads(rv.data.decode("utf-8"))
        assert "serviceId" in j
        service = j["serviceId"]

        rv = self.client.get("/service/" + service, headers={"Session-Token": self.session_token},
                             content_type='application/json')
        assert rv.status == "200 OK"

        rv2 = self.client.get("/service/" + car["_id"], headers={"Session-Token": self.session_token})
        assert rv2.status == "200 OK"


        rv = self.client.get("/service/19834jn", headers={"Session-Token": self.session_token})
        assert rv.status == "400 BAD REQUEST"

        rv = self.client.delete("/service/" + service, headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"
