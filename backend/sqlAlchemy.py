import traceback
from typing import Optional

from sqlalchemy import *
import sqlalchemy
import bcrypt
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import Session, sessionmaker

from backend.classes import *
from backend.db_interface import DatabaseInterface
from backend.utils import calculate_gps_distance, row2dict

salt = b'$2b$12$pzEs7Xy4xlrgcpLSrcN71O'  # Temp

HOSTNAME = "vps.zgrate.ovh"
PORT = "3306"
USERNAME = "polrentex"
PASSWORD = "rentex123"
DB_NAME = "Rentex"

engine = sqlalchemy.create_engine('mysql+mysqlconnector://' + USERNAME + ':' + PASSWORD + '@' + HOSTNAME + ':' + PORT + '/' + DB_NAME,
                                  echo=True)

class SQLAlchemyInterface(DatabaseInterface):

    def __init__(self):
        super().__init__()
        self.startSession: sqlalchemy.orm.sessionmaker = sessionmaker()
        engine.connect()
        self.startSession.configure(bind=engine)
        self.seed()

    def seed(self):
        with self.startSession() as session:
            if self.getRole("Client") is None:
                session.add(Role(RoleName="Client", PermissionsLevel=1))
            if self.getRole("Service") is None:
                session.add(Role(RoleName="Service", PermissionsLevel=10))
            if self.getRole("Admin") is None:
                session.add(Role(RoleName="Admin", PermissionsLevel=100))
            session.commit()

    def createSession(self) -> Session:
        sess = self.startSession()
        return sess

    def getUser(self, userId):
        with self.createSession() as session:
            return session.query(Client).get(userId)

    def rentalHistory(self, userId, pageIndex, pageLength):
        with self.createSession() as session:
            return session.query(Rental).offset(pageIndex).limit(pageLength).all()

    def getCards(self, userId):
        with self.createSession() as session:
            return session.query(CreditCard).filter(CreditCard.clientId == userId).all()

    def browseNearestCars(self, location, distance):
        cars = []
        with self.createSession() as session:
            for car in session.query(Car).filter(Car.status == CarStatusEnum.ACTIVE).all():
                if calculate_gps_distance((float(location[0]), float(location[1])),
                                          (float(car.currentLocationLat),
                                           float(car.currentLocationLong))) <= int(distance):
                    cars.append(car)
        return cars

    def browseNearestLocations(self, location, distance):
        locations = []
        with self.createSession() as session:
            for _location in session.query(Location).all():
                if calculate_gps_distance((float(location[0]), float(location[1])),
                                          (float(_location.locationLat),
                                           float(_location.locationLong))) <= int(distance):
                    locations.append(_location)
        return locations

    def getRental(self, userId, rentalId):
        with self.createSession() as session:
            return session.query(Rental).get(rentalId)

    def getCars(self, pageIndex, pageCount, location, distance):
        return self.browseNearestCars(location, distance)[int(pageIndex): int(pageIndex) + int(pageCount)]

    def getUsers(self, pageIndex, pageCount, filter: str):  # TODO fuck the filter?
        with self.createSession() as session:
            return session.query(Rental).offset(pageIndex).limit(pageCount).all()

    def getCard(self, userId, cardId):
        with self.createSession() as session:
            return session.query(CreditCard).get(cardId)

    def getLocations(self, pageIndex, pageCount, location, distance):
        return self.browseNearestLocations(location, distance)[int(pageIndex): int(pageIndex) + int(pageCount)]

    def getService(self, serviceId):
        with self.createSession() as session:
            return session.query(Service).get(serviceId)

    def authUser(self, login, password):
        with self.createSession() as session:
            user = session.query(Client).filter(Client.login == login).first()
            if user is not None and bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')):
                return user
            return None

    def getRole(self, roleName: str):
        with self.createSession() as session:
            return session.query(Role).filter(Role.RoleName == roleName).first()

    def registerUser(
            self,
            name: str,
            surname: str,
            login: str,
            password: str,
            email: str,
            pesel: str,
    ):
        with self.createSession() as session:
            try:

                role = self.getRole("Client")
                user = Client(name=name, surname=surname, login=login,
                              password=bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()),
                              email=email,
                              pesel=pesel,
                              balance="00.00", accountType=AccountTypeEnum.PERSONAL, activationCode=0,
                              status=AccountStatusEnum.INACTIVE, roles=[role])
                session.add(user)
                session.commit()

                session.refresh(user)
                return user.clientId
                # inserted_user = session\
                #     .execute(sql.insert(Client)\
                #         .values(
                #             name=name,
                #             surname=surname,
                #             login=login,
                #             password=password,
                #             address=address,
                #             email=email,
                #             pesel=pesel,
                #             balance= "00.00",
                #             accountType= AccountTypeEnum.PERSONAL,
                #             activationCode= "",
                #             status= AccountStatusEnum.INACTIVE
                #         )
                #     )
                # role_id = self.getRole("Client").roleId
                #
                # inserted_role = session\
                #     .execute(sql.insert(t_ClientRoles)\
                #         .values(
                #             user_id=inserted_user.inserted_primary_key[0],
                #             role_id=role_id,
                #         ))
            except Exception as e:
                print(str(e))
                traceback.print_tb(e.__traceback__)
                session.rollback()
                return None

    def getAccountStatus(self, userId: str):
        user = self.getUser(userId)
        if user is None:
            return None
        return user.status

    def getActivationToken(self, userId: str):
        user = self.getUser(userId)
        if user is None:
            return None
        return user.activationCode

    def setAccountStatus(self, userId: str, status: str):
        with self.createSession() as session:
            session.query(Client).filter(Client.clientId == userId).update({Client.status: status})
            session.commit()
        return True

    def setActivationToken(self, userId: int, token: str) -> bool:
        with self.createSession() as session:
            session.begin()
            try:
                session.query(Client).get(userId).update({Client.activationCode: token})
            except:
                session.rollback()
                return False
            else:
                session.commit()
            return True

    def changePassword(self, userId, newPwd):
        with self.createSession() as session:
            session.begin()
            try:
                session.query(Client).get(userId).update({Client.password: bcrypt.hashpw(newPwd.encode('utf8'), salt)})
            except:
                session.rollback()
                return False
            else:
                session.commit()
            return True

    def updateLocation(self, carId, location):
        with self.createSession() as session:
            session.begin()
            try:
                session.query(Car).get(carId).update({
                    Car.currentLocationLat: location[0],
                    Car.currentLocationLong: location[1]
                })
            except:
                session.rollback()
                return False
            else:
                session.commit()
            return True

    def addCard(self, userId, card: CreditCard):
        with self.createSession() as session:
            session.begin()
            try:
                if self.getUser(userId) is not None:
                    card.clientId = userId
                    session.add(card)
                    session.commit()
                    return True

                # TODO
                # inserted_card = session\
                #     .execute(sql.insert(CreditCard)\
                #         .values(
                #             car=name,
                #             surname=surname,
                #             login=login,
                #             password=password,
                #             address=address,
                #             email=email,
                #             pesel=pesel,
                #             balance= "00.00",
                #             accountType= AccountTypeEnum.PERSONAL,
                #             activationCode= "",
                #             status= AccountStatusEnum.INACTIVE
                #         )
                #     )
                pass
            except Exception as e:
                print(e)
                session.rollback()
                return False

    def startReservation(self, reservation: Reservation):
        with self.createSession() as session:
            user = session.query(Client).get(reservation.clientId)
            if not user or user.status != AccountStatusEnum.ACTIVE:
                return None
            if session.query(Reservation).filter(and_(
                    Reservation.clientId == reservation.clientId,
                    Reservation.reservationStart < datetime.datetime.now(),
                    Reservation.reservationEnd > datetime.datetime.now()
            )).first():
                return None
            if session.query(Rental).filter(and_(
                    Rental.clientId == reservation.clientId,
                    not Rental.ended
            )).first():
                return None
            try:
                session.add(reservation)
                session.commit()
                session.refresh(reservation)
                return reservation.reservationId

            except Exception as e:
                print(e)
                session.rollback()
                return None
            return None

    def endReservation(self, reservation: Reservation) -> bool:
        #        a = self.rentalDb["User"].find_and_modify({"_id": ObjectId(reservation.userId)},{'$unset': {"reservation": ""}})
        # b = self.rentalDb["Car"].find_and_modify({"_id": ObjectId(reservation_["reservation"]["carId"])},{'$set': {"status": "ACTIVE"}})
        session: sqlalchemy.orm.Session
        with self.startSession() as session:
            session.bulk_save_objects([reservation])
            session.query(Car).filter(Car.carId == reservation.carId).update({Car.status: CarStatusEnum.ACTIVE})
            session.commit()
        return True

    def getCar(self, carId) -> Car:
        with self.createSession() as session:
            return session.query(Car).get(carId)

    def startRental(self, userId, carId):
        with self.createSession() as session:
            car = session.query(Car).get(carId)
            if not car or car.status != CarStatusEnum.ACTIVE:
                return None

            # TODO: check if car is available
            # reservations
            # if session.query(Reservation).filter(and_(
            #         Reservation.carId == carId,
            #         Reservation.clientId != userId,
            #         Reservation.reservationEnd is None,
            # )):
            #     return None
            # rentals
            if session.query(Rental).filter(Rental.carId == carId, Rental.ended == 0).count() > 0:
                return None

            user = session.query(Client).get(userId)
            if not user or user.status != AccountStatusEnum.ACTIVE:
                return None
            user_reservation = session.query(Reservation).filter(and_(
                Reservation.clientId == userId,
                Reservation.reservationStart < datetime.datetime.now(),
                Reservation.reservationEnd > datetime.datetime.now()
            )).first()

            if user_reservation:
                if user_reservation.carId != carId:
                    return None
                user_reservation.reservationEnd = datetime.datetime.now()
                session.bulk_save_objects([user_reservation])
            try:
                rental = Rental(rentalStart=datetime.datetime.now(), mileage=0, carId=carId, clientId=userId,
                                ended=False)
                session.add(rental)
                session.commit()
                session.refresh(rental)
                return rental.rentalId
            except Exception as e:
                session.rollback()
                return None

    def endRental(self, rent: Rental):
        with self.createSession() as session:
            rental: Rental = session.query(Rental).get(rent.rentalId)
            if rental is None or rental.clientId != rent.clientId:
                return False
            try:
                session.query(Rental).filter(Rental.rentalId == rent.rentalId).update(row2dict(rent))
                session.commit()
                return True
            except Exception as e:
                print(e)
                session.rollback()
                return False


    def deleteCar(self, carId):
        with self.createSession() as session:
            try:
                updated_car = session \
                    .query(Car).filter(Car.carId == carId) \
                    .update({
                    Car.status: CarStatusEnum.DELETED
                })
            except:
                session.rollback()
                return False
            else:
                session.commit()
            return True

    def patchCar(self, carId, changes: dict):
        with self.createSession() as session:
            try:
                session.query(Car).filter(Car.carId == carId).update(changes)
                session.commit()
                return True
            except Exception as e:
                print(e)
                session.rollback()
                return False

    def deleteUser(self, userId):
        with self.createSession() as session:
            try:
                updated_user = session \
                    .query(Client).filter(Client.clientId == userId) \
                    .update({
                    Client.status: AccountStatusEnum.DELETED
                })
            except:
                session.rollback()
                return False
            else:
                session.commit()
            return True

    def patchUser(self, userId, changes: dict):
        with self.createSession() as session:
            try:
                updated_user = session \
                    .query(Client).filter(Client.clientId == userId) \
                    .update(changes)
            except:
                session.rollback()
                return False
            else:
                session.commit()
            return True

    def addLocation(self, location: Location):
        with self.createSession() as session:
            try:
                session.add(location)
                session.commit()
                session.refresh(location)
                return location.locationId
            except Exception as e:
                print(e)
                session.rollback()
                return None

    def deleteLocation(self, locationId):
        with self.createSession() as session:
            try:
                updated_location = session \
                    .query(Location).filter(Location.locationId == locationId) \
                    .update({Location.status: LocationStatusEnum.DELETED})
            except:
                session.rollback()
                return False
            else:
                session.commit()
            return True

    def patchLocation(self, locationId, changes: dict):
        with self.createSession() as session:
            try:
                updated_location = session \
                    .query(Location).filter(Location.locationId == locationId) \
                    .update(changes)
            except:
                session.rollback()
                return False
            else:
                session.commit()
            return True

    def serviceCar(self, carId, userId, locationId, description="") -> Optional[int]:
        with self.createSession() as session:
            try:
                service = Service(carId=carId, clientId=userId, locationId=locationId, description=description,
                                  dateStart=datetime.datetime.now())
                session.add(service)
                session.commit()
                session.refresh(service)
                return service.serviceId
            except Exception as e:
                print(e)
                session.rollback()
                return None

    def endService(self, service: Service):
        with self.createSession() as session:
            try:
                inserted_service = session \
                    .query(Service).filter(Service.serviceId == service.serviceId) \
                    .update({Service.dateEnd: datetime.datetime.now()})
            except:
                session.rollback()
                return False
            else:
                session.commit()
            return True

    def getServicesHistory(self, carId):
        with self.createSession() as session:
            return session.query(Service).filter(Service.carId == carId).all()

    def setNewBalance(self, user_id, new_balance) -> bool:
        with self.createSession() as session:
            try:
                updated_user = session \
                    .query(Client).filter(Client.clientId == user_id) \
                    .update({Client.balance: new_balance})
            except:
                session.rollback()
                return False
            else:
                session.commit()
            return True

    def getBalance(self, user_id) -> str:
        with self.createSession() as session:
            user = session.query(Client).get(user_id)
            if user:
                return user.balance
            return None

    def isUserWithEmailInDB(self, email) -> bool:
        with self.createSession() as session:
            user = session.query(Client).filter(Client.email == email).count()
            if user > 0:
                return True
            return False

    def isUserWithLoginInDB(self, login) -> bool:
        with self.createSession() as session:
            user = session.query(Client).filter(Client.login == login).count()
            if user > 0:
                return True
            return False

    def addCar(self, car: 'dict'):
        with self.createSession() as session:
            session.begin()
            try:
                car = Car(brand=car["brand"],
                          vin=car["vin"],
                          regNumber=str(car["regNumber"]),
                          modelName=car["model"],
                          passengerNumber=car["seats"],
                          chargeLevel=car["charge"],
                          mileage=car["mileage"],
                          currentLocationLat=car["locationLat"],
                          currentLocationLong=car["locationLong"],
                          status=car["status"],
                          activationCost=car["activationCost"],
                          kmCost=car["kmCost"],
                          timeCost=car["timeCost"],
                          eSimImei=car["esimImei"])
                session.add(car)
            except Exception as e:
                print(e)
                traceback.print_tb(e.__traceback__)
                session.rollback()
                return False
            else:
                session.commit()
            return True

    def dropCars(self):
        session: sqlalchemy.orm.Session
        with self.createSession() as session:
            session.query(Car).delete()
            session.commit()

    def dropRentalArchive(self):
        with self.createSession() as session:
            session.query(Rental).delete()
            session.query(Reservation).delete()
            session.commit()

    def dropUsers(self):
        with self.createSession() as session:
            session.query(Client).delete()
            session.commit()

    def dropLocations(self):
        with self.createSession() as session:
            session.query(Service).delete()
            session.query(Location).delete()
            session.commit()

    def userCleanup(self, user_id):
        with self.createSession() as session:
            session.query(Client).filter(Client.clientId == user_id).update({Client.status: AccountStatusEnum.ACTIVE})
            session.commit()

    # self.rentalDb["User"].update_one({"_id": ObjectId(user._id)},{"$set": {"status": "ACTIVE", "currentRental": "", "rentalArchive": []}})

    def carCleanup(self, car_id):
        with self.createSession() as session:
            session.query(Car).filter(Car.carId == car_id).update({Car.status: CarStatusEnum.ACTIVE})
            session.query(Service).filter(Service.carId == car_id).delete()
            session.commit()

    def getActiveReservation(self, userId) -> Reservation:
        session: sqlalchemy.orm.Session
        with self.createSession() as session:
            return session.query(Reservation).filter(Reservation.clientId == userId,
                                                    Reservation.reservationStart < datetime.datetime.now(),
                                                    Reservation.reservationEnd > datetime.datetime.now()).first()

    def getActiveRentalOfTheUser(self, userId) -> Rental:
        session: sqlalchemy.orm.Session
        with self.createSession() as session:
            a = (session.query(Rental).all())
            return session.query(Rental).filter(Rental.clientId == userId, Rental.ended == 0).first()

    def getReservation(self, userId, reservationId) -> Reservation:
        with self.startSession() as session:
            return session.query(Reservation).filter(Reservation.reservationId == reservationId,
                                                     Reservation.clientId == userId).first()


# car = self.getCar(car_id)
# self.rentalDb["User"].update_one({"_id": ObjectId(car_id)}, {"$set": {"status": "ACTIVE", "currentRental": "", "services": []}})


RENTAL_DB = SQLAlchemyInterface()
