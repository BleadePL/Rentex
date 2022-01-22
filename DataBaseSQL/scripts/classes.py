# coding: utf-8
from sqlalchemy import BigInteger, CHAR, Column, DECIMAL, ForeignKey, Integer, String, Table, text
from sqlalchemy.dialects.mysql import TIME
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# pip install sqlacodegen
# sqlacodegen mysql+mysqldb://polrentex:rentex123@vps.zgrate.ovh:3306/Rentex --outfile classes.py

Base = declarative_base()
metadata = Base.metadata


class Car(Base):
    __tablename__ = 'Cars'

    carId = Column(Integer, primary_key=True, unique=True)
    brand = Column(String(30), nullable=False, comment='Nazwa marki (pełna)')
    vin = Column(CHAR(17), nullable=False, unique=True)
    regCountryCode = Column(CHAR(2), nullable=False)
    regNumber = Column(String(10), nullable=False)
    modelName = Column(String(50), nullable=False)
    passengerNumber = Column(Integer, nullable=False)
    lastUsed = Column(TIME(fsp=6), nullable=False)
    chargeLevel = Column(Integer, nullable=False)
    mileage = Column(Integer, nullable=False)
    currentLocationLat = Column(DECIMAL(10, 8), nullable=False)
    currentLocationLong = Column(DECIMAL(11, 8), nullable=False)
    lastUpdateTime = Column(TIME(fsp=6), nullable=False)
    lastService = Column(TIME(fsp=6), nullable=False)
    status = Column(String(3), nullable=False,
                    comment='ACTIVE - aktywny\\nRESERVED - zarezerwowany\\nINACTIVE - wyłączony z użycia\\nSERVICE - Serwisowany\\nINUSE - w uzyciu\\nUNKNOWN - nieznany stan')
    activationCost = Column(String(30), nullable=False)
    kmCost = Column(String(30), nullable=False)
    timeCost = Column(String(30), nullable=False)
    esimNumber = Column(Integer, nullable=False)
    eSimImei = Column(Integer, nullable=False)


class Client(Base):
    __tablename__ = 'Clients'

    clientId = Column(Integer, primary_key=True, unique=True)
    pesel = Column(CHAR(20), nullable=False)
    surname = Column(String(30), nullable=False)
    name = Column(String(30), nullable=False)
    address = Column(String(255), nullable=False)
    driverLicenceNumber = Column(Integer)
    driverLicenceExpirationDate = Column(Integer)
    balance = Column(String(20), nullable=False, server_default=text("'0'"))
    login = Column(String(20), nullable=False)
    password = Column(String(64), nullable=False)
    email = Column(String(50), nullable=False)
    accountType = Column(String(10), nullable=False,
                         comment='PERSONAL - osoba prywatna\\nCOMPANY - firma\\nORGANISATION - organizacja\\nUNKNOWN - Inne')
    activationCode = Column(Integer)
    status = Column(String(10), nullable=False,
                    comment='ACTIVE - Aktywne konto\\nINACTIVE - nieaktwyne konto\\nDOCUMENTS - Brak dokumentow\\nPENDING - wyslano dokumenty, oczekiwanie na potwierdzenie\\nPAYMENT - Brak srodkow na koncie\\nLOCKED - konto zablokowane\\nDELETED - konto usuniete')

    Roles = relationship('Role', secondary='ClientRoles')


class Location(Base):
    __tablename__ = 'Locations'

    locationId = Column(Integer, primary_key=True, unique=True)
    locationType = Column(String(10), nullable=False,
                          comment='STATION - Stacja benzynowa\\nCLEAN - stacja czyszczenia\\nSERVICE - Serwis\\nSPECIAL_POINT - Punkt specjalny\\nUNKNOWN - nieznany')
    locationName = Column(String(100), nullable=False)
    locationAddress = Column(String(100))
    leaveReward = Column(String(30), nullable=False)
    locationLat = Column(DECIMAL(10, 8), nullable=False)
    locationLong = Column(DECIMAL(11, 8), nullable=False)


class Role(Base):
    __tablename__ = 'Roles'

    roleId = Column(Integer, primary_key=True, unique=True)
    RoleName = Column(String(100))
    PermissionsLevel = Column(Integer)


t_ClientRoles = Table(
    'ClientRoles', metadata,
    Column('clientId', ForeignKey('Clients.clientId'), nullable=False, index=True),
    Column('roleId', ForeignKey('Roles.roleId'), index=True)
)


class CreditCard(Base):
    __tablename__ = 'CreditCards'

    creditCardId = Column(Integer, primary_key=True, unique=True)
    clientId = Column(ForeignKey('Clients.clientId'), nullable=False, index=True)
    cardNumber = Column(Integer)
    expirationDate = Column(Integer)
    cardHolderName = Column(String(30))
    cardHolderAddress = Column(String(30))

    Client = relationship('Client')


class Rental(Base):
    __tablename__ = 'Rentals'

    rentalId = Column(BigInteger, primary_key=True, unique=True)
    carId = Column(ForeignKey('Cars.carId'), nullable=False, index=True)
    clientId = Column(ForeignKey('Clients.clientId'), index=True)
    rentalStart = Column(TIME(fsp=6), nullable=False)
    rentalEnd = Column(TIME(fsp=6))
    mileage = Column(Integer, nullable=False)
    cost = Column(String(30))
    ended = Column(Integer, nullable=False)

    Car = relationship('Car')
    Client = relationship('Client')


class Reservation(Base):
    __tablename__ = 'Reservations'

    reservationId = Column(Integer, primary_key=True, unique=True)
    carId = Column(ForeignKey('Cars.carId'), nullable=False, index=True)
    clientId = Column(ForeignKey('Clients.clientId'), index=True)
    reservationStart = Column(TIME(fsp=6), nullable=False)
    reservationEnd = Column(TIME(fsp=6))
    reservationCost = Column(Integer, nullable=False)

    Car = relationship('Car')
    Client = relationship('Client')
