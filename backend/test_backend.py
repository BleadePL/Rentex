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

    def runGetUserTest(self):
        assert self.session_token != ""
        rv = self.client.get("/user/details", content_type='application/json',
                             headers={"Session-Token": self.session_token})
        print(rv)
        assert rv.status == "200 OK"
        print(rv.data)

    @test
    def runStatusTest(self):
        rv = self.client.get("/login/status", content_type='application/json',
                             headers={"Session-Token": self.session_token})
        assert rv.status == "200 OK"
        print(rv.data)

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
        assert rv.status == "200 OK"
        j = json.load(rv.data.decode("utf-8"))
        assert "userId" in j
        rv = self.client.delete("/admin/deleteaccount", data=json.dumps({"userid": j["userId"]}))
        assert rv.status == "200 OK"
