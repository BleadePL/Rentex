# coding: utf-8
import datetime
import enum
from dataclasses import dataclass

from sqlalchemy import Enum, BigInteger, CHAR, Column, DECIMAL, ForeignKey, Integer, String, Table, create_engine, text, \
    DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# pip install sqlacodegen
# sqlacodegen mysql+mysqldb://polrentex:rentex123@vps.zgrate.ovh:3306/Rentex --outfile classes.py

Base = declarative_base()
metadata = Base.metadata


class CarStatusEnum(str, enum.Enum):
    ACTIVE="ACTIVE"
    RESERVED="RESERVED"
    INACTIVE="INACTIVE"
    SERVICE="SERVICE"
    INUSE="INUSE"
    UNKNOWN="UNKNOWN"

class AccountTypeEnum(str, enum.Enum):
    PERSONAL="PERSONAL"
    COMPANY="COMPANY"
    ORGANISATION="ORGANISATION"
    UNKNOWN="UNKNOWN"

class AccountStatusEnum(str, enum.Enum):
    ACTIVE="ACTIVE"
    INACTIVE="INACTIVE"
    DOCUMENTS="DOCUMENTS"
    PENDING="PENDING"
    PAYMENT="PAYMENT"
    LOCKED="LOCKED"
    DELETED="DELETED"
class LocationTypeEnum(str,enum.Enum):
    STATION="STATION"
    CLEAN="CLEAN"
    SERVICE="SERVICE"
    SPECIAL_POINT="SPECIAL_POINT"
    UNKNOWN="UNKNOWN"
# TODO indexing
@dataclass
class Car(Base):
    carId: int
    brand: str
    vin: str
    regCountryCode: str
    regNumber: str
    modelName: str
    passengerNumber: int
    chargeLevel: int
    mileage: int
    currentLocationLat: str
    currentLocationLong: str
    status: CarStatusEnum
    activationCost: String
    kmCost: String
    timeCost: String
    esimNumber: int
    eSimImei: int
    rentals: list['Rental']
    services: list['Service']


    __tablename__ = 'Cars'

    carId = Column(Integer, primary_key=True, unique=True)
    brand = Column(String(30), nullable=False, comment='Nazwa marki (pełna)')
    vin = Column(String(17), nullable=False, unique=True)
    regCountryCode = Column(String(2), nullable=False)
    regNumber = Column(String(10), nullable=False)
    modelName = Column(String(50), nullable=False)
    passengerNumber = Column(Integer, nullable=False)
    chargeLevel = Column(Integer, nullable=False)
    mileage = Column(Integer, nullable=False)
    currentLocationLat = Column(DECIMAL(10, 8), nullable=False)
    currentLocationLong = Column(DECIMAL(11, 8), nullable=False)
    status = Column(Enum(CarStatusEnum), nullable=False,
                    comment='ACTIVE - aktywny\\nRESERVED - zarezerwowany\\nINACTIVE - wyłączony z użycia\\nSERVICE - Serwisowany\\nINUSE - w uzyciu\\nUNKNOWN - nieznany stan')
    activationCost = Column(String(30), nullable=False)
    kmCost = Column(String(30), nullable=False)
    timeCost = Column(String(30), nullable=False)
    esimNumber = Column(Integer, nullable=False)
    eSimImei = Column(Integer, nullable=False)

    reservations = relationship("Reservation", back_populates="car", lazy='noload')
    rentals = relationship("Rental", back_populates="car", lazy='noload')
    services = relationship("Service", back_populates="car", lazy='noload')

@dataclass
class Client(Base):
    clientId: int
    pesel: str
    surname: str
    name: str
    address: str
    driverLicenceNumber: int 
    driverLicenceExpirationDate: int 
    balance: str
    login: str
    password: str
    email: str
    accountType: AccountTypeEnum
    activationCode: int
    status: AccountStatusEnum
    roles: list['Role']
    creditCards: list['CreditCard']
    rentals: list['Rental']
    reservations: list['Reservation']
    services: list['Service']

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
    accountType = Column(Enum(AccountTypeEnum), nullable=False,
                         comment='PERSONAL - osoba prywatna\\nCOMPANY - firma\\nORGANISATION - organizacja\\nUNKNOWN - Inne')
    activationCode = Column(Integer)
    status = Column(Enum(AccountStatusEnum), nullable=False,
                    comment='ACTIVE - Aktywne konto\\nINACTIVE - nieaktwyne konto\\nDOCUMENTS - Brak dokumentow\\nPENDING - wyslano dokumenty, oczekiwanie na potwierdzenie\\nPAYMENT - Brak srodkow na koncie\\nLOCKED - konto zablokowane\\nDELETED - konto usuniete')

    roles = relationship('Role', secondary='ClientRoles', lazy='noload', cascade="all, delete")
    creditCards = relationship("CreditCard", back_populates="client", lazy='noload')
    rentals = relationship("Rental", back_populates="client", lazy='noload')
    reservations = relationship("Reservation", back_populates="client", lazy='noload')
    services = relationship("Service", back_populates="client", lazy='noload')

@dataclass
class Service(Base):
    serviceId: int
    dateStart: datetime.datetime
    dateEnd: datetime.datetime
    description: str
    location: 'Location'
    car: 'Car'
    client: 'Client'

    __tablename__ = 'Services'
    serviceId = Column(Integer, primary_key=True, unique=True)
    dateStart = Column(DateTime, nullable=False)
    dateEnd = Column(DateTime)
    description = Column(String(255))
    
    locationId = Column(Integer, ForeignKey('Locations.locationId'))
    carId = Column(Integer, ForeignKey('Cars.carId'))
    clientId = Column(Integer, ForeignKey('Clients.clientId'))
    location = relationship("Location", back_populates="services", lazy='noload')
    car = relationship("Car", back_populates="services", lazy='noload')
    client = relationship("Client", back_populates="services", lazy='noload') 

@dataclass
class Location(Base):
    locationId: int
    locationType: LocationTypeEnum
    locationName: str
    locationAddress: str
    leaveReward: str
    locationLat: float
    locationLong: float
    services: list['Service']

    __tablename__ = 'Locations'

    locationId = Column(Integer, primary_key=True, unique=True)
    locationType = Column(Enum(LocationTypeEnum), nullable=False,
                          comment='STATION - Stacja benzynowa\\nCLEAN - stacja czyszczenia\\nSERVICE - Serwis\\nSPECIAL_POINT - Punkt specjalny\\nUNKNOWN - nieznany')
    locationName = Column(String(100), nullable=False)
    locationAddress = Column(String(100))
    leaveReward = Column(String(30), nullable=False)
    locationLat = Column(DECIMAL(10, 8), nullable=False)
    locationLong = Column(DECIMAL(11, 8), nullable=False)
    
    services = relationship("Service", back_populates="location", lazy='noload') 

@dataclass
class Role(Base):
    roleId: int
    RoleName: str
    PermissionsLevel: int 

    __tablename__ = 'Roles'

    roleId = Column(Integer, primary_key=True, unique=True)
    RoleName = Column(String(100))
    PermissionsLevel = Column(Integer)


t_ClientRoles = Table(
    'ClientRoles', metadata,
    Column('clientId', ForeignKey('Clients.clientId'), index=True, primary_key=True),
    Column('roleId', ForeignKey('Roles.roleId'), index=True, primary_key=True)
)

@dataclass
class CreditCard(Base):
    creditCardId: int
    cardNumber: str
    expirationDate: datetime.datetime 
    cardHolderName: str
    cardHolderAddress: str
    client: 'Client' 

    __tablename__ = 'CreditCards'

    creditCardId = Column(Integer, primary_key=True, unique=True)
    cardNumber = Column(String)
    expirationDate = Column(DateTime)
    cardHolderName = Column(String(30))
    cardHolderAddress = Column(String(30))

    clientId = Column(ForeignKey('Clients.clientId'), nullable=False, index=True)
    client = relationship('Client', back_populates="creditCards", lazy="noload")

@dataclass
class Rental(Base):
    rentalId: int
    rentalStart: datetime.datetime
    rentalEnd: datetime.datetime
    mileage: int
    cost: str
    ended: bool
    car: 'Car'
    client: 'Client'

    __tablename__ = 'Rentals'

    rentalId = Column(BigInteger, primary_key=True, unique=True)
    rentalStart = Column(DateTime, nullable=False)
    rentalEnd = Column(DateTime, nullable=True)
    mileage = Column(Integer, nullable=True)
    cost = Column(String(30))
    ended = Column(Boolean, nullable=False)

    carId = Column(ForeignKey('Cars.carId'), nullable=False, index=True)
    clientId = Column(ForeignKey('Clients.clientId'), index=True)
    car = relationship('Car', back_populates="rentals", lazy='noload')
    client = relationship('Client', back_populates="rentals", lazy='noload')

@dataclass
class Reservation(Base):
    reservationId: int
    reservationStart: datetime.datetime
    reservationEnd: datetime.datetime
    reservationCost: str
    car: 'Car'
    client: 'Client'

    __tablename__ = 'Reservations'

    reservationId = Column(Integer, primary_key=True, unique=True)
    reservationStart = Column(DateTime, nullable=False)
    reservationEnd = Column(DateTime)
    reservationCost = Column(String, nullable=False)

    clientId = Column(ForeignKey('Clients.clientId'), index=True)
    carId = Column(ForeignKey('Cars.carId'), nullable=False, index=True)
    car = relationship('Car', back_populates="reservations", lazy='noload')
    client = relationship('Client', back_populates="reservations", lazy='noload')

if __name__ == "__main__":
    url = f'postgresql://postgres:passwd@127.0.0.1:5432'
    engine = create_engine(url, echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
