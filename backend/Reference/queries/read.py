from sqlalchemy.orm import Session, selectinload, joinedload, noload
from po_api import DATABASE
import po_api.database.orm.models as models
import sqlalchemy as sql
from po_api.database.db import Database

@DATABASE.db_query
def get_all_waypoints(session: Session):
    return session\
        .execute(
            sql.select(models.Waypoint)\
            .options(
                joinedload(models.Waypoint.mountain_range)\
                    .options(noload(models.MountainRange.waypoints)),
                joinedload(models.Waypoint.path_starts)
                # noload(models.Waypoint.path_starts)
                )
        ).unique().scalars().all()

@DATABASE.db_query
def get_waypoint_by_name(session: Session, name: str):
    return session\
        .execute(
            sql.select(models.Waypoint)\
            .where(models.Waypoint.name == name)
        ).first()._asdict()

@DATABASE.db_query
def get_path_by_id(session: Session, id: int):
    return session\
        .execute(
            sql.select(models.Path)\
            .where(models.Path.id == id)
        ).first()

@DATABASE.db_query
def get_all_paths(session: Session, include_closed: bool, waypoint_from_id: int=None):
    x = session\
        .execute(
            sql.select(models.Path)\
                .where(sql.and_(sql.or_(
                    waypoint_from_id is None, models.Path.waypoint_a_id == waypoint_from_id
                    ),sql.or_(
                    include_closed, models.Path.status == models.PathStatus.open)
                    )
                )\
                .options(
                    joinedload(models.Path.waypoint_a)\
                        .options(
                            joinedload(models.Waypoint.mountain_range),
                        ),
                    joinedload(models.Path.waypoint_b)\
                        .options(
                            joinedload(models.Waypoint.mountain_range),
                        ))
        ).scalars().all()
    return x

@DATABASE.db_query
def get_trip(session:Session, trip_id: int):
    result = session.execute(
        sql.select(models.Trip).where(models.Trip.id == trip_id).options(
            joinedload(models.Trip.trip_plan)\
                .options(joinedload(models.TripPlan.segments)\
                    .options(joinedload(models.TripSegment.path)\
                        .options(joinedload(models.Path.waypoint_a),
                                joinedload(models.Path.waypoint_b)))),# add ordering
            joinedload(models.Trip.participations)
            .options(
                joinedload(models.Participation.badge_acquirement).options(
                    joinedload(models.BadgeAcquirement.got_book).options(
                        joinedload(models.GotBook.owner)
                    )
                )
            )
        )
    ) 
    result = result.first()
    return result

@DATABASE.db_query
def get_pending_badge_acquirements(session: Session):
    result = session.execute(sql.select(models.BadgeAcquirement)\
        .where(models.BadgeAcquirement.status == models.BadgeAcquirementStatusEnum.waiting_for_review)\
            .options(
                joinedload(models.BadgeAcquirement.badge),
                joinedload(models.BadgeAcquirement.got_book)\
                    .options(
                        joinedload(models.GotBook.owner)
                    ),
                    joinedload(models.BadgeAcquirement.participations)\
                        .options(joinedload(models.Participation.participation_reviews)\
                            .options(joinedload(models.ParticipationReview.reviewer))
                        )
            )
    )
    return result.unique().scalars().all()

@DATABASE.db_query
def auth_user(session: Session, login: str, password:str):
    result = session.execute(sql.select(models.User)\
        .where(models.User.login == login and models.User.password == password))
    return result.first()

@DATABASE.db_query
def get_all_mountain_ranges(session: Session):
    result = session\
        .execute(
            sql.select(models.MountainRange).options(joinedload(models.MountainRange.waypoints))
        ).unique().scalars().all()
    return result