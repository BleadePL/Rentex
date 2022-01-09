import flask_sqlalchemy
db = flask_sqlalchemy.SQLAlchemy()

COLLECTION_USERS = "Users"
COLLECTION_CARS = "Cars"
COLLECTION_LOCATIONS = "Locations"
COLLECTION_RENTALS = "Rentals"
COLLECTION_RESERVATIONS = "Reservations"
COLLECTION_CREDIT_CARDS = "CreditCards"
COLLECTION_SERVICES = "Services"
COLLECTION_ROLES = "Roles"

class User(db.Model):
    __tablename__ = COLLECTION_USERS
    id = db.Column(db.Integer, primary_key=True)
    pesel = db.Column(db.String(20), unique=True, nullable=False)
    surname = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(30), unique=True, nullable=False)
    address = db.Column(db.String(255), unique=True, nullable=False)
    driverLicenceNumber = db.Column(db.String(255), unique=True, nullable=False)
    driverLicenceExpirationDate = db.Column(db.DateTime, unique=True, nullable=False)
    balance = db.Column(db.String(20), unique=True, nullable=False)
    login = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    accountType = db.Column(db.String(10), unique=True, nullable=False)
    activationCode = db.Column(db.Integer, unique=True, nullable=False)
    status = db.Column(db.String(10), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    creditCards = db.relationship("CreditCard", backref='user', lazy=True)
    services = db.relationship('Service', backref='user', lazy=True)
    reservations = db.relationship('Reservation', backref='user', lazy=True)
    rentals = db.relationship('Rental', backref='user', lazy=True)

class Car(db.Model):
    __tablename__ = COLLECTION_CARS
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(30), unique=True, nullable=False)
    vin = db.Column(db.String(17), unique=True, nullable=False)
    regCountryCode = db.Column(db.String(2), unique=True, nullable=False)
    regNumber = db.Column(db.String(10), unique=True, nullable=False)
    modelName = db.Column(db.String(50), unique=True, nullable=False)
    seats = db.Column(db.Integer, unique=True, nullable=False)
    lastUsed = db.Column(db.DateTime, unique=True, nullable=False)
    chargeLevel = db.Column(db.Integer, unique=True, nullable=False)
    mileage = db.Column(db.Integer, unique=True, nullable=False)
    currentLocationLat = db.Column(db.Float, unique=True, nullable=False)
    currentLocationLong = db.Column(db.Float, unique=True, nullable=False)
    lastUpdateTime = db.Column(db.DateTime, unique=True, nullable=False)
    status = db.Column(db.String(10), unique=True, nullable=False)
    activationCost = db.Column(db.String(30), unique=True, nullable=False)
    kmCost = db.Column(db.String(30), unique=True, nullable=False)
    timeCost = db.Column(db.String(30), unique=True, nullable=False)
    esimNumber = db.Column(db.Integer, unique=True, nullable=False)
    esimImei = db.Column(db.Integer, unique=True, nullable=False)
    services = db.relationship('Service', backref='car', lazy=True)
    reservaitons = db.relationship('Reservation', backref='car', lazy=True)
    rentals = db.relationship('Rental', backref='car', lazy=True)

class Rental(db.Model):
    __tablename__ = COLLECTION_RENTALS
    id = db.Column(db.Integer, primary_key=True)
    rentalStart = db.Column(db.DateTime, unique=True, nullable=False)
    rentalEnd = db.Column(db.DateTime, unique=True, nullable=True)
    mileage = db.Column(db.Integer, unique=True, nullable=False)
    totalCost = db.Column(db.String(30), unique=True, nullable=False)
    ended = db.Column(db.Boolean, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'),nullable=False)

    
class Reservation(db.Model):
    __tablename__ = COLLECTION_RESERVATIONS
    id = db.Column(db.Integer, primary_key=True)
    reservationStart = db.Column(db.DateTime, unique=True, nullable=False)
    reservationEnd = db.Column(db.DateTime, unique=True, nullable=False)
    reservationStatus = db.Column(db.String(30), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'),nullable=False)


class Service(db.Model):
    __tablename__ = COLLECTION_SERVICES
    id = db.Column(db.Integer, primary_key=True)
    dateStart = db.Column(db.String(20), unique=True, nullable=False)
    dateEnd = db.Column(db.String(30), unique=True, nullable=True)
    description = db.Column(db.String(255), unique=True, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'),nullable=False)

class Location(db.Model):
    __tablename__ = COLLECTION_LOCATIONS
    id = db.Column(db.Integer, primary_key=True)
    locationName = db.Column(db.String(100), unique=True, nullable=False)
    locationAddress = db.Column(db.String(100), unique=True, nullable=False)
    leaveReward = db.Column(db.String(30), unique=True, nullable=False)
    locationLat = db.Column(db.Float, unique=True, nullable=False)
    locationLong = db.Column(db.Float, unique=True, nullable=False)
    services = db.relationship('Service', backref='location', lazy=True)

class CreditCard(db.Model):
    __tablename__ = COLLECTION_CREDIT_CARDS
    id = db.Column(db.Integer, primary_key=True)
    cardNumber = db.Column(db.String(19), unique=True, nullable=False)
    expirationDate = db.Column(db.DateTime, unique=True, nullable=False)
    cardHolderName = db.Column(db.String(30), unique=True, nullable=False)
    cardHolderAddress = db.Column(db.String(30), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Role(db.Model):
    __tablename__ = COLLECTION_ROLES
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), unique=True, nullable=False)
    users = db.relationship("User", backref='user', lazy=True)

