import secrets
import threading
import time

from flask import Flask, Response
from flask_login import LoginManager

from backend.database_access import RENTAL_DB
from backend.models import Rental, Car, Reservation, CreditCard
from flask_cors import CORS
import schedule

TESTS = True


class LoggedInUser:
    def __init__(self, user_id, session_token):
        self.id = user_id
        self.session_token = session_token
        self.activation_token_time = None

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def retrieve_user_from_db(self):
        return RENTAL_DB.getUser(userId=self.id)


class PendingRental:
    DISTANCE_THRESHOLD = 10

    def __init__(self, rent: Rental, kmCost: str, timeCost: str, activationCost: str, startLong, startLat,
                 paymentType: str, cvv: int, card: CreditCard, overtime: bool):
        self.rent = rent
        s = kmCost.split(".")
        self.kmCost = int(s[1]) + int(s[0]) * 100
        s = timeCost.split(".")
        self.timeCost = int(s[1]) + int(s[0]) * 100
        s = activationCost.split(".")
        self.activationCost = int(s[1]) + int(s[0]) * 100
        self.distance = 0
        self.lastLong = startLong
        self.lastLat = startLat
        self.paymentType = paymentType
        self.cvv = cvv
        self.card = card
        self.overtime = overtime

    def __eq__(self, other):
        if other is PendingRental:
            super.__eq__(self, other)
        elif other is Rental:
            return self.rent._id == other._id

    def update_distance(self, currentLat, currentLong):
        from backend.utils import calculate_gps_distance
        d = calculate_gps_distance((float(self.lastLat), float(self.lastLong)), (float(currentLat), float(currentLong)))
        if d > PendingRental.DISTANCE_THRESHOLD:
            self.distance += d
        self.lastLat = currentLat
        self.lastLong = currentLong

    def calculate_current_cost(self) -> int:
        timeCost = (int(time.time()) - self.rent.rentalStart) * self.timeCost
        return int(int(self.activationCost + timeCost + (
                self.distance / 1000) * self.kmCost)) + (TOO_LONG_RENTAL_PUNISHMENT if self.overtime else 0)


class RentalReservationTimerTask:

    def __init__(self):
        self.active_rentals = []
        self.active_reservations = []

    def tick(self):
        for e in self.active_rentals:
            if e.rent.ended:
                self.endRent(e.rent)
            elif not e.overtime and time.time() - e.rent.rentalStart > MAX_RENTAL_TIME:
                e.overtime = True

        for e in self.active_reservations:
            if time.time() - e.reservationStart > MAX_RESERVATION_TIME or e.reservationEnd is not None:
                self.endReservation(e)

    def rent(self, car: Car, user_id, payment_method, cvv: int = None, card: CreditCard = None) -> [None, str]:
        r = Rental(car_id=car._id, rental_start=int(time.time()), ended=False, client_id=user_id, mileage=0,
                   rental_cost="")
        p = PendingRental(rent=r, kmCost=car.kmCost, timeCost=car.timeCost, activationCost=car.activationCost,
                          startLong=car.currentLocationLong,
                          startLat=car.currentLocationLat, paymentType=payment_method, cvv=cvv, card=card,
                          overtime=False)
        if payment_method == "PP":
            if RENTAL_DB.getBalance(user_id) < MINIMAL_BALANCE:
                return None
        rentalId = RENTAL_DB.startRental(userId=user_id, carId=car._id)
        if rentalId is not None:
            p.rent._id = rentalId
            self.active_rentals.append(p)
            return rentalId
        return None

    def endRent(self, r_id) -> bool:
        r: PendingRental = next((x for x in self.active_rentals if x.rent._id == r_id), None)
        if r is None:
            return False
        cost = r.calculate_current_cost()
        from backend.utils import charge_card, gr_to_pln_gr
        if not charge_card(cost, r.paymentType == "PP", r.card, r.cvv, r.rent.renter):
            return False
        self.active_rentals.remove(r)
        r.rent.ended = True
        r.rent.rentalEnd = int(time.time())
        r.rent.mileage = r.distance
        r.rent.totalCost = gr_to_pln_gr(cost)
        if RENTAL_DB.endRental(r.rent):
            l = RENTAL_DB.browseNearestLocations((r.lastLat, r.lastLong), 200)
            if len(l) > 0:
                l.sort(key=lambda d: calculate_gps_distance((r.lastLat, r.lastLong), (d.locationLat, d.locationLong)))
                loc: Location = l[0]
                user = RENTAL_DB.getUser(userId=r.rent.renter)
                if user is None:
                    return False
                if RENTAL_DB.setNewBalance(user._id, user.balance + loc.leaveReward):
                    return True
                return False
            else:
                return True


    def startReservation(self, car_id, user_id) -> str:
        r = Reservation(car_id=car_id, user_id=user_id, reservation_start=int(time.time()))
        res_id = RENTAL_DB.startReservation(r)
        if res_id is None:
            return None
        r._id = res_id
        self.active_reservations.append(r)
        return res_id

    def endReservation(self, res_id: str):
        res = next((x for x in self.active_reservations if x._id == res_id), None)
        if res is None:
            return False
        res.reservationEnd = int(time.time())
        self.active_reservations.remove(res)
        return RENTAL_DB.endReservation(res)

    def getRental(self, rent_id) -> PendingRental:
        return next((x for x in self.active_rentals if x.rent._id == rent_id), None)

    def updateDistance(self, car_id, lat, long):
        res = next((x for x in self.active_rentals if x.rent.carId == car_id), None)
        if res is not None:
            res: PendingRental
            res.update_distance(lat, long)


app: Flask
login: LoginManager
BAD_REQUEST: tuple
EMPTY_OK: tuple
rental_timer_task: RentalReservationTimerTask
MAX_RESERVATION_TIME = 300
MINIMAL_BALANCE = 10
TOO_LONG_RENTAL_PUNISHMENT = 200
MAX_RENTAL_TIME = 3600 * 24
PHOTOS_TARGET: str

MIDDLE_LAT = "51.107737"
MIDDLE_LONG = "17.038717"
MAX_DISTANCE = 10000


def runTests():
    from test_backend import Tests, TEST_FUNCTIONS
    with app.test_client() as client:
        t = Tests(client)


        # attrs = (getattr(t, name) for name in dir(t))
        # import inspect
        # methods = filter(inspect.ismethod, attrs)
        for method in TEST_FUNCTIONS:
            try:
                print("-----TESTING: " + method.__name__ + "-----")
                print()
                if method.__name__ != "__init__":
                    method(t)
                print("-----TEST COMPLETE-----")
                print()
            except AssertionError as ex:
                assert False
                # Can't handle methods with required arguments.
                pass


if __name__ == "flask_main":
    app = Flask("Wypozyczalnia Aut BACKEND")
    app.secret_key = secrets.token_hex()
    login = LoginManager(app)
    cors = CORS(app)
    BAD_REQUEST = {}, 400
    EMPTY_OK = {}, 200
    PHOTOS_TARGET = "licences"
    rental_timer_task = RentalReservationTimerTask()
    schedule.every().second.do(rental_timer_task.tick)

    from login_controller import *
    from user_controller import *
    from service_controller import *
    from browse_controller import *
    from rent_controller import *
    from admin_controller import *


    def loop():
        while True:
            schedule.run_pending()
            time.sleep(1)


    t = threading.Thread(target=loop)
    t.setDaemon(True)
    t.start()
    if TESTS:
        print("Welcome to Testing system. Hold your fingers now!")
        print()
        runTests()
        print()
        print("Test complete! Everything is okey! Thanks for testing with Z-Grate solutions!")
        exit(0)
