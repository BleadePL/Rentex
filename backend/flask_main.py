import secrets
import time

from flask import Flask, Response
from flask_login import LoginManager

from backend.database_access import RENTAL_DB
from backend.models import Rental, Car, Reservation
from backend.utils import calculate_gps_distance, gr_to_pln_gr

app = Flask("Wypozyczalnia Aut BACKEND")
app.secret_key = secrets.token_hex()
login = LoginManager(app)
BAD_REQUEST = {}, 400
EMPTY_OK = {}, 200

MAX_RESERVATION_TIME = 300
# auth = Authorize()
print("Initialized!")

import login_controller
import user_controller
import service_controller
import browse_controller

import schedule


class PendingRental:
    DISTANCE_THRESHOLD = 10

    def __init__(self, rent: Rental, kmCost: str, timeCost: str, activationCost: str, startLong, startLat):
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

    def __eq__(self, other):
        if other is PendingRental:
            super.__eq__(self, other)
        elif other is Rental:
            return self.rent._id == other._id

    def update_distance(self, currentLong, currentLat):
        d = calculate_gps_distance((currentLong, currentLat), (currentLong, currentLat))
        if d > PendingRental.DISTANCE_THRESHOLD:
            self.distance += d

    def calculate_current_cost(self) -> str:

        timeCost = (int(time.time()) - self.rent.rentalStart) * self.timeCost
        return gr_to_pln_gr(int(self.activationCost + timeCost + (self.distance / 1000) * self.kmCost))


class RentalReservationTimerTask:

    def __init__(self):
        self.active_rentals = []
        self.active_reservations = []

    def tick(self):
        for e in self.active_rentals:
            if e.ended:
                self.endRent(e.rent)

        for e in self.active_reservations:
            if time.time() - e.reservationStart > MAX_RESERVATION_TIME or e.ended:
                self.endReservation(e)

    def rent(self, car: Car, user_id) -> bool:
        r = Rental(car_id=car._id, rental_start=int(time.time()), ended=False, client_id=user_id, mileage=0,
                   rental_cost="")
        p = PendingRental(r, car.kmCost, car.timeCost, car.activationCost, car.currentLocationLong,
                          car.currentLocationLat)
        self.active_rentals.append(p)
        return RENTAL_DB.startRental(userId=user_id, rent=r)

    def endRent(self, rent: Rental) -> bool:
        if rent not in self.active_rentals:
            return False
        r: PendingRental = next(x for x in self.active_rentals if x.rent._id == rent._id)
        if r is None:
            return False
        self.active_rentals.remove(r)
        rent.ended = True
        rent.rentalEnd = int(time.time())
        rent.mileage = r.distance
        rent.rentalCost = r.calculate_current_cost()
        return RENTAL_DB.endRental(rent)

    def startReservation(self, car_id, user_id) -> bool:
        r = Reservation(car_id=car_id, user_id=user_id, reservation_start=int(time.time()))
        self.active_reservations.append(r)
        return RENTAL_DB.startReservation(r)

    def endReservation(self, reservation: Reservation):
        reservation.reservationEnd = int(time.time())
        self.active_reservations.remove(reservation)
        return RENTAL_DB.endReservation(reservation)
