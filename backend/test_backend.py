import io

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
        assert rv.status == "200 OK"
        print(rv.data)

    #  @test
    def runRegisterTest(self):
        rv = self.client.post("/login/register", data=json.dumps({"name": "Fryderyk",
                                                                  "surname": "Markowski",
                                                                  "gender": "M",
                                                                  "login": "test",
                                                                  "password": "test",
                                                                  "address": "20;Sienkiewicza;60951;Tarnobrzeg;Polska",
                                                                  "email": "FrydMark11@gmail.com",
                                                                  "pesel": "60060535351"}),
                              content_type='application/json')
        print(rv.data)
        assert rv.status == "200 OK"
        j = json.load(rv.data.decode("utf-8"))
        assert "userId" in j
        rv = self.client.delete("/admin/deleteaccount", data=json.dumps({"userid": j["userId"]}))
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

    @test
    def testBrowseNearestCar(self):
        rv = self.client.get("/user/")
