from dataclasses import dataclass
from datetime import datetime
import enum
import json
import sqlalchemy as db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.declarative import DeclarativeMeta

TABLE_LICENCES = "license"
TABLE_USERS = "user"
TABLE_ROLES = "role"
TABLE_USER_ROLES = "user_role"
TABLE_MOUNTAIN_RANGES = "mountain_range"
TABLE_WAYPOINTS = "waypoint"
TABLE_PATHS = "path"
TABLE_TRIP_PLANS = "trip_plan"
TABLE_BADGES = "badge"
TABLE_TRIPS = "trip"
TABLE_BADGE_ACQUIREMENTS = "badge_acquirement"
TABLE_BADGE_ACQUIREMENT_REVIEWS = "badge_acquirement_review"
TABLE_PARTICIPATIONS = "participation"
TABLE_GOT_BOOKS = "got_book"
TABLE_PARTICIPATION_REVIEWS = "participation_review"
TABLE_TRIP_SEGMENTS = "trip_segment"

def tablename_to_class_name(string:str):
    return string.replace('_', ' ').title().replace(' ', '')

# declarative base class
Base = declarative_base()
class ColorsEnum(str, enum.Enum):
    red = "red".capitalize()
    green = "green".capitalize()
    blue = "blue".capitalize()
    black = "black".capitalize()
    yellow = "yellow".capitalize()
class PathStatus(str, enum.Enum):
    open = "open".capitalize()
    closed = "closed".capitalize()
class TripDifficulty(str, enum.Enum):
    easy = "easy".capitalize()
    semi_easy = "semi_easy".capitalize()
    medium = "medium".capitalize()
    semi_hard = "semihard".capitalize()
    hard = "hard".capitalize()
class ReviewEnum(str, enum.Enum):
    accepted = "accepted".capitalize()
    rejected = "rejected".capitalize()    
class BadgeAcquirementStatusEnum(str, enum.Enum):
    collecting_points = "collecting_points".capitalize()
    waiting_for_review = "waiting_for_review".capitalize()
    acquired = "acquired".capitalize()
    rejected = "rejected".capitalize()
class ParticipationStatusEnum(str, enum.Enum):
    waiting_for_review = "waiting_for_review".capitalize()
    acquired = "acquired".capitalize()
    rejected = "rejected".capitalize()

trip_guides = db.Table('association', Base.metadata,
    db.Column('guide', db.ForeignKey(TABLE_USERS + '.id'), primary_key=True),
    db.Column('trip', db.ForeignKey(TABLE_TRIPS + '.id'), primary_key=True)
)

@dataclass
class User(Base):
    id:int
    login: str
    password: str
    name: str
    surname: str

    roles: list['UserRole']
    badge_acquirement_reviews: list['BadgeAcquirementReview']
    got_book: list['GotBook']
    participation_reviews: list['ParticipationReview']
    organized_trips: list['Trip']
    guided_trips: list['Trip']
    trip_plans: list['TripPlan']


    __tablename__ = TABLE_USERS

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(30))
    surname = db.Column(db.String(30))
    
    roles = relationship(tablename_to_class_name(TABLE_USER_ROLES), lazy='noload', back_populates="user")
    badge_acquirement_reviews = relationship(tablename_to_class_name(TABLE_BADGE_ACQUIREMENT_REVIEWS), lazy='noload', back_populates="reviewer")
    got_book = relationship(tablename_to_class_name(TABLE_GOT_BOOKS), uselist=False, lazy='noload', back_populates="owner")
    participation_reviews = relationship(tablename_to_class_name(TABLE_PARTICIPATION_REVIEWS), lazy='noload', back_populates="reviewer")
    organized_trips = relationship(tablename_to_class_name(TABLE_TRIPS), lazy='noload', back_populates="organizer")
    guided_trips = relationship(tablename_to_class_name(TABLE_TRIPS), secondary=trip_guides, lazy='noload', back_populates="guides")
    trip_plans = relationship(tablename_to_class_name(TABLE_TRIP_PLANS), lazy='noload', back_populates="creator")  

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.get_id() == other.get_id()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


@dataclass
class Role(Base):
    id:int
    name:str
    users: list['UserRole']

    __tablename__ = TABLE_ROLES

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    users = relationship(tablename_to_class_name(TABLE_USER_ROLES), lazy='noload', back_populates="role")

@dataclass
class UserRole(Base):
    user: 'User'
    role: 'Role'
    args: dict

    __tablename__ = TABLE_USER_ROLES

    user_id = db.Column(db.Integer, db.ForeignKey(TABLE_USERS + ".id"), primary_key=True)
    user = relationship(tablename_to_class_name(TABLE_USERS), lazy='noload', back_populates="roles")

    role_id = db.Column(db.Integer, db.ForeignKey(TABLE_ROLES + ".id"), primary_key=True)
    role = relationship(tablename_to_class_name(TABLE_ROLES), lazy='noload', back_populates="users")

    args = db.Column(db.PickleType)


@dataclass
class MountainRange(Base):
    id:int
    name:str
    waypoints:list['Waypoint']


    __tablename__ = TABLE_MOUNTAIN_RANGES

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    waypoints = relationship(tablename_to_class_name(TABLE_WAYPOINTS), lazy='noload', back_populates="mountain_range")

@dataclass
class Waypoint(Base):
    id:int
    name:str
    elevation:int
    longtitude:str
    latitude:str
    description:str
    mountain_range:'MountainRange'
    path_starts: list['Path']

    __tablename__ = TABLE_WAYPOINTS

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    elevation = db.Column(db.Integer)
    longtitude = db.Column(db.String(40))
    latitude = db.Column(db.String(40))
    description = db.Column(db.String(255))

    mountain_range_id = db.Column(db.Integer, db.ForeignKey(TABLE_MOUNTAIN_RANGES + ".id"))
    mountain_range = relationship(tablename_to_class_name(TABLE_MOUNTAIN_RANGES), lazy='noload', back_populates="waypoints")

    path_starts = relationship(tablename_to_class_name(TABLE_PATHS), lazy='noload', back_populates="waypoint_a", foreign_keys='[Path.waypoint_a_id]')
    # path_starts = relationship(tablename_to_class_name(TABLE_PATHS), lazy='noload', back_populates="waypoint_a", foreign_keys='[Path.waypoint_a_id]')

    # path_ends = relationship(tablename_to_class_name(TABLE_PATHS), lazy='noload', back_populates="waypoint_b", foreign_keys='[Path.waypoint_b_id]')

@dataclass
class Path(Base):
    id: int
    color: ColorsEnum
    is_official: bool
    points: int
    distance: int
    status: PathStatus
    waypoint_a: 'Waypoint'
    waypoint_b: 'Waypoint'
    segments: list['TripSegment']

    __tablename__ = TABLE_PATHS

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    color = db.Column(db.Enum(ColorsEnum))
    is_official = db.Column(db.Boolean)
    points = db.Column(db.Integer)
    status = db.Column(db.Enum(PathStatus))
    distance = db.Column(db.Integer)

    waypoint_a_id = db.Column(db.Integer, db.ForeignKey(TABLE_WAYPOINTS + ".id"))
    waypoint_a = relationship(tablename_to_class_name(TABLE_WAYPOINTS), lazy='noload', back_populates="path_starts", foreign_keys='Path.waypoint_a_id')
    waypoint_b_id = db.Column(db.Integer, db.ForeignKey(TABLE_WAYPOINTS + ".id"))
    waypoint_b = relationship(tablename_to_class_name(TABLE_WAYPOINTS), lazy='noload', foreign_keys='Path.waypoint_b_id')

    segments = relationship(tablename_to_class_name(TABLE_TRIP_SEGMENTS), lazy='noload', back_populates="path")

@dataclass
class TripPlan(Base):
    id: int
    name: str
    description: str
    distance: float
    difficulty: TripDifficulty
    is_public: bool
    creator: 'User'
    segments: list['TripSegment']
    trips: list['Trip']

    __tablename__ = TABLE_TRIP_PLANS

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(255))
    distance = db.Column(db.Float)
    difficulty = db.Column(db.Enum(TripDifficulty))
    is_public = db.Column(db.Boolean)
    
    creator_id = db.Column(db.Integer, db.ForeignKey(TABLE_USERS + ".id"))
    creator = relationship(tablename_to_class_name(TABLE_USERS), lazy='noload', back_populates="trip_plans")
    
    segments = relationship(tablename_to_class_name(TABLE_TRIP_SEGMENTS), lazy='noload', back_populates="trip_plan")
    trips = relationship(tablename_to_class_name(TABLE_TRIPS), lazy='noload', back_populates="trip_plan")

@dataclass
class TripSegment(Base):
    index: int
    trip_plan: 'TripPlan'
    path: 'Path'

    __tablename__ = TABLE_TRIP_SEGMENTS

    index = db.Column(db.Integer, primary_key=True)

    trip_plan_id = db.Column(db.Integer, db.ForeignKey(TABLE_TRIP_PLANS + ".id"), primary_key=True)
    trip_plan = relationship(tablename_to_class_name(TABLE_TRIP_PLANS), lazy='noload', back_populates="segments")

    path_id = db.Column(db.Integer, db.ForeignKey(TABLE_PATHS + ".id"), primary_key=True)
    path = relationship(tablename_to_class_name(TABLE_PATHS), lazy='noload', back_populates="segments")

@dataclass
class Badge(Base):
    id: int
    required_age: int
    required_points: int
    name: str
    acquirements: list['BadgeAcquirement']

    __tablename__ = TABLE_BADGES
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    required_age = db.Column(db.Integer)
    required_points = db.Column(db.Integer)
    acquirements = relationship(tablename_to_class_name(TABLE_BADGE_ACQUIREMENTS), lazy='noload', back_populates="badge")

@dataclass
class BadgeAcquirement(Base):
    id: int
    status: BadgeAcquirementStatusEnum
    badge: 'Badge'
    got_book: 'GotBook'
    participations: list['Participation']
    reviews: list['BadgeAcquirementReview']

    __tablename__ = TABLE_BADGE_ACQUIREMENTS

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Enum(BadgeAcquirementStatusEnum))

    badge_id = db.Column(db.Integer, db.ForeignKey(TABLE_BADGES + ".id"))
    badge = relationship(tablename_to_class_name(TABLE_BADGES), lazy='noload', back_populates="acquirements")

    got_book_id = db.Column(db.Integer, db.ForeignKey(TABLE_GOT_BOOKS + ".id"))
    got_book = relationship(tablename_to_class_name(TABLE_GOT_BOOKS), lazy='noload', back_populates="badge_acquirements")

    participations = relationship(tablename_to_class_name(TABLE_PARTICIPATIONS), lazy='noload', back_populates="badge_acquirement")

    reviews = relationship(tablename_to_class_name(TABLE_BADGE_ACQUIREMENT_REVIEWS), lazy='noload', back_populates="badge_acquirement") 

@dataclass
class BadgeAcquirementReview(Base):
    badge_acquirement: 'BadgeAcquirement'
    reviewer: 'User'
    review_date: datetime
    required_points: int
    earned_points: int
    review: ReviewEnum

    __tablename__ = TABLE_BADGE_ACQUIREMENT_REVIEWS

    badge_acquirement_id = db.Column(db.Integer, db.ForeignKey(TABLE_BADGE_ACQUIREMENTS + ".id"), primary_key=True)
    badge_acquirement = relationship(tablename_to_class_name(TABLE_BADGE_ACQUIREMENTS), lazy='noload', back_populates="reviews")

    reviewer_id = db.Column(db.Integer, db.ForeignKey(TABLE_USERS + ".id"), primary_key=True)
    reviewer = relationship(tablename_to_class_name(TABLE_USERS), lazy='noload', back_populates="badge_acquirement_reviews")
    
    review_date = db.Column(db.DateTime)
    required_points = db.Column(db.Integer)
    earned_points = db.Column(db.Integer)
    review = db.Column(db.Enum(ReviewEnum))

@dataclass
class Participation(Base):
    id: int
    # images: TODO
    status: ParticipationStatusEnum
    trip: 'Trip'
    badge_acquirement: 'BadgeAcquirement'
    participation_reviews: list['ParticipationReview']

    __tablename__ = TABLE_PARTICIPATIONS

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    images = db.Column(db.LargeBinary)
    status = db.Column(db.Enum(ParticipationStatusEnum))

    trip_id = db.Column(db.Integer, db.ForeignKey(TABLE_TRIPS + ".id"))
    trip = relationship(tablename_to_class_name(TABLE_TRIPS), lazy='noload', back_populates="participations")

    badge_acquirement_id = db.Column(db.Integer, db.ForeignKey(TABLE_BADGE_ACQUIREMENTS + ".id"))
    badge_acquirement = relationship(tablename_to_class_name(TABLE_BADGE_ACQUIREMENTS), lazy='noload', back_populates="participations")

    participation_reviews = relationship(tablename_to_class_name(TABLE_PARTICIPATION_REVIEWS), lazy='noload', back_populates="participation")

@dataclass
class GotBook(Base):
    id: int
    issue_date: datetime
    badge_acquirements: list['BadgeAcquirement']
    owner: 'User'

    __tablename__ = TABLE_GOT_BOOKS

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    issue_date = db.Column(db.DateTime)

    badge_acquirements = relationship(tablename_to_class_name(TABLE_BADGE_ACQUIREMENTS), lazy='noload', back_populates="got_book")

    owner_id = db.Column(db.Integer, db.ForeignKey(TABLE_USERS + ".id"))
    owner = relationship(tablename_to_class_name(TABLE_USERS), lazy='noload', back_populates="got_book")

@dataclass
class ParticipationReview(Base):
    id: int
    review: ReviewEnum
    participation: 'Participation'
    reviewer: 'User'
    review_date: datetime
    earned_points: int

    __tablename__ = TABLE_PARTICIPATION_REVIEWS

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    review = db.Column(db.Enum(ReviewEnum))

    participation_id = db.Column(db.Integer, db.ForeignKey(TABLE_PARTICIPATIONS  + ".id"))
    participation = relationship(tablename_to_class_name(TABLE_PARTICIPATIONS), lazy='noload', back_populates="participation_reviews")

    reviewer_id = db.Column(db.Integer, db.ForeignKey(TABLE_USERS  + ".id"))
    reviewer = relationship(tablename_to_class_name(TABLE_USERS), lazy='noload', back_populates="participation_reviews")

    review_date = db.Column(db.DateTime)
    earned_points = db.Column(db.Integer)

@dataclass
class Trip(Base):
    id: int
    date: datetime
    name: str
    description: str
    is_public: bool
    participations: list['Participation']
    organizer: 'User'
    guides: list['User']
    trip_plan: 'TripPlan'

    __tablename__ = TABLE_TRIPS

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    date = db.Column(db.DateTime)
    name = db.Column(db.String(30))
    description = db.Column(db.String(255))
    is_public = db.Column(db.Boolean)

    participations = relationship(tablename_to_class_name(TABLE_PARTICIPATIONS), lazy='noload', back_populates="trip")

    organizer_id = db.Column(db.Integer, db.ForeignKey(TABLE_USERS + ".id"))
    organizer = relationship(tablename_to_class_name(TABLE_USERS), lazy='noload', back_populates="organized_trips")

    guides = relationship(tablename_to_class_name(TABLE_USERS), secondary=trip_guides, lazy='noload', back_populates="guided_trips")

    trip_plan_id = db.Column(db.Integer, db.ForeignKey(TABLE_TRIP_PLANS  + ".id"))
    trip_plan = relationship(tablename_to_class_name(TABLE_TRIP_PLANS), lazy='noload', back_populates="trips")

if __name__ == "__main__":
    url = 
    engine = db.create_engine(url, echo=True)
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
