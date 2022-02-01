from curses import echo
from sqlite3 import connect
from sqlalchemy import *
import sqlalchemy
from sqlalchemy.orm import Session, sessionmaker
from backend.database_access import DATABASE
from backend.db_interface import DatabaseInterface
from backend.classes import *
from backend.utils import calculate_gps_distance

import bcrypt
salt = b'$2b$12$pzEs7Xy4xlrgcpLSrcN71O'  # Temp

HOSTNAME = "vps.zgrate.ovh"
PORT = "3306"
USERNAME = "polrentex"
PASSWORD = "rentex123"
DB_NAME = "Rentex"

engine = sqlalchemy.create_engine('mysql://' + USERNAME + ':' + PASSWORD + '@' + HOSTNAME + ':' + PORT + '/' + DB_NAME)

class SQLAlchemyInterface(DatabaseInterface):
    
    def __init__(self):
        super().__init__()
        self.startSession: sqlalchemy.orm.sessionmaker = sessionmaker()
        engine.connect()
        self.startSession(bind=engine)

    def createSession(self) -> Session:
        return self.startSession()

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
                                      (float(_location.currentLocationLat),
                                       float(_location.currentLocationLong))) <= int(distance):
                    locations.append(_location)
        return locations

    def getRental(self, userId, rentalId):
        with self.createSession() as session:
            return session.query(Rental).get(rentalId)

    def getCars(self, pageIndex, pageCount, location, distance):
        return self.browseNearestCars(location, distance)[int(pageIndex): int(pageIndex) + int(pageCount)]

    def getUsers(self, pageIndex, pageCount, filter: str): # TODO fuck the filter?
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
            return session.query(Client)\
                .filter(and_(
                    Client.login == login,
                    Client.password == bcrypt.hashpw(password.encode('utf8'), salt)
                    )
                )

    def getRole(self, roleName:str): 
        with self.createSession() as session:
            return session.query(Role).filter(Role.RoleName==roleName).first()

    def registerUser(
            self,
            name: str,
            surname: str,
            login: str,
            password: str,
            address: str,
            email: str,
            pesel: str,
    ):
        with self.createSession() as session:
            session.begin()
            try:
                inserted_user = session\
                    .execute(sql.insert(Client)\
                        .values(
                            name=name,
                            surname=surname,
                            login=login,
                            password=password,
                            address=address,
                            email=email,
                            pesel=pesel,
                            balance= "00.00",
                            accountType= AccountTypeEnum.PERSONAL,
                            activationCode= "",
                            status= AccountStatusEnum.INACTIVE
                        )
                    )
                role_id = self.getRole("Client").roleId

                inserted_role = session\
                    .execute(sql.insert(t_ClientRoles)\
                        .values(
                            user_id=inserted_user.inserted_primary_key[0],
                            role_id=role_id,
                        ))
            except:
                session.rollback()
                return False
            else:
                session.commit()
            return True

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
            session.query(Client).filter(Client.id == userId).update({Client.status: status})
        pass


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
            except:
                session.rollback()
                return False
            else:
                session.commit()
            return True


    def startReservation(self, reservation: Reservation):
        with self.createSession() as session:
            user = session.query().get(reservation.clientId)
            if not user or user.status != AccountStatusEnum.ACTIVE:
                return False
            if session.query(Reservation).filter(and_(
                Reservation.clientId==reservation.clientId,
                Reservation.reservationStart < datetime.datetime.now(),
                Reservation.reservationEnd > datetime.datetime.now()
                )).first():
                return False
            if session.query(Rental).filter(and_(
                Rental.clientId==reservation.clientId,
                Rental.ended
                )).first():
                return False
            session.begin()
            try:
                inserted_reservation = session\
                    .execute(sql.insert(Reservation)\
                        .values(
                            reservationStart=reservation.reservationStart,
                            reservationEnd=reservation.reservationEnd,
                            reservationCost=reservation.reservationCost,
                            clientId=reservation.clientId,
                            carId=reservation.carId,
                        )
                    )
            except:
                session.rollback()
                return False
            else:
                session.commit()
            return True

    def startRental(self, userId, carId):
        with self.createSession() as session:
            car = session.query(Car).get(carId)
            if not car or car.status != CarStatusEnum.ACTIVE:
                return False

            #TODO: check if car is available
            # reservations
            if session.query(Reservation).filter(and_(
                Reservation.carId == carId,
                Reservation.clientId != userId,
                Reservation.reservationStart < datetime.datetime.now(),
                Reservation.reservationEnd > datetime.datetime.now(),
                )):
                return False
            # rentals
            if session.query(Rental).filter(and_(
                Rental.carId == carId,
                not Rental.ended,
                )):
                return False
            
            user = session.query(Client).get(userId)
            if not user or user.status != AccountStatusEnum.ACTIVE:
                return False
            user_reservation = session.query(Reservation).filter(and_(
                Reservation.clientId==userId,
                Reservation.reservationStart < datetime.datetime.now(),
                Reservation.reservationEnd > datetime.datetime.now()
                )).first()

            session.begin()

            if user_reservation:
                if user_reservation.carId != carId:
                    return False
                self.endReservation(user_reservation) # TODO: end reservation here
            try:
                inserted_rental = session\
                    .execute(sql.insert(Rental)\
                        .values(
                            rentalStart=datetime.datetime.now(),
                            mileage=car.mileage,
                            ended=False,
                            carId=carId,
                        )
                    )
            except:
                session.rollback()
                return False
            else:
                session.commit()
            return True


    def endRental(self, rent: Rental):
        with self.createSession() as session:
            rental = session.query(Rental).get(rent.rentalId)
            if not rental or rental.ended:
                return False
            try:
                updated_rental = session\
                    .query(Rental).filter(Rental.rentalId == rent.rentalId)\
                        .update({
                            Rental.rentalEnd: rent.rentalEnd,
                            Rental.mileage: rent.mileage,
                            Rental.cost: rent.cost,
                            Rental.ended: rent.ended,
                        })
            except:
                session.rollback()
                return False
            else:
                session.commit()
            return True


    def deleteCar(self, carId):
        with self.createSession() as session: 
            try:
                updated_car = session\
                    .query(Car).filter(Car.carId == carId)\
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
                updated_car = session\
                    .query(Car).filter(Car.carId == carId)\
                        .update({
                            Car.status: CarStatusEnum.DELETED
                        })
            except:
                session.rollback()
                return False
            else:
                session.commit()
            return True


    def deleteUser(self, userId):
        with self.createSession() as session: 
            try:
                updated_user = session\
                    .query(Client).filter(Client.clientId == userId)\
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
                updated_user = session\
                    .query(Client).filter(Client.clientId == userId)\
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
                inserted_location = session\
                    .add(location)
            except:
                session.rollback()
                return False
            else:
                session.commit()
            return True

    def deleteLocation(self, locationId):
        with self.createSession() as session: 
            try:
                updated_location = session\
                    .query(Location).filter(Location.locationId == locationId)\
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
                updated_location = session\
                    .query(Location).filter(Location.locationId == locationId)\
                        .update(changes)
            except:
                session.rollback()
                return False
            else:
                session.commit()
            return True


    def serviceCar(self, carId, userId, locationId, description="") -> str:
        with self.createSession() as session: 
            try:
                inserted_service = session\
                    .execute(sql.insert(Service)\
                        .values(
                            dateStart=datetime.datetime.now(),
                            clientId=userId,
                            carId=carId,
                            locationId=locationId,
                            description=description
                        )
                    )
            except:
                session.rollback()
                return False
            else:
                session.commit()
            return True

    def endService(self, service: Service):
        with self.createSession() as session: 
            try:
                inserted_service = session\
                    .query(Service).filter(Service.serviceId == service.serviceId)\
                        .update({Service.dateEnd: datetime.datetime.now()})
            except:
                session.rollback()
                return False
            else:
                session.commit()
            return True


    def getServicesHistory(self, carId):
        pass

    def setNewBalance(self, user_id, new_balance) -> bool:
        pass

    def getBalance(self, user_id) -> str:
        pass

    def isUserWithEmailInDB(self, email) -> bool:
        pass

    def isUserWithLoginInDB(self, login) -> bool:
        pass

    def addCar(self, car: 'dict'):
        pass


    def dropCars(self):
        pass

    def dropRentalArchive(self):
        pass

    def dropUsers(self):
        pass

    def dropLocations(self):
        pass

    def userCleanup(self, user_id):
        pass

    def carCleanup(self, car_id):
        pass
