import datetime
from sqlalchemy.orm import Session
from po_api import DATABASE
import po_api.database.orm.models as models
import sqlalchemy as sql
from po_api.database.db import Database


@DATABASE.db_query
def create_user(session:Session, user: dict):
    session.begin()
    try:
        inserted_user = session\
            .execute(sql.insert(models.User)\
                .values(
                    user
                )
            )
        inserted_role = session\
            .execute(sql.insert(models.UserRole)\
                .values(
                    user_id=inserted_user.inserted_primary_key[0],
                    role_id=sql\
                        .select(models.Role.id)\
                            .where(models.Role.name == "Tourist").scalar_subquery(),
                    args=user["args"]
                ))
    except:
        session.rollback()
        raise
    else:
        session.commit()
    return inserted_user

@DATABASE.db_query
def review_badge_acquirement(session: Session, badge_acquirement_review: dict):
    session.begin()
    try:
        inserted_review = session\
            .execute(sql.insert(models.BadgeAcquirementReview)\
                .values(
                    badge_acquirement_review
                )
            )
        badge_acquirement_status =\
             models.BadgeAcquirementStatusEnum.acquired\
                  if badge_acquirement_review["review"]==models.ReviewEnum.accepted\
                  else models.BadgeAcquirementStatusEnum.rejected 
        updated_badge_acquirement = session\
            .execute(sql.update(models.BadgeAcquirement)\
                .where(
                    models.BadgeAcquirement.id == badge_acquirement_review["badge_acquirement_id"])\
                .values(status=badge_acquirement_status)
            )
    except:
        session.rollback()
        raise
    else:
        session.commit()
    return inserted_review

@DATABASE.db_query
def review_participation(session: Session, participation_review:dict):
    session.begin()
    try:
        inserted_review = session\
            .execute(sql.insert(models.ParticipationReview)\
                .values(
                    participation_review
                )
            )
        participation_status =\
             models.ParticipationStatusEnum.acquired\
                  if participation_review["review"]==models.ReviewEnum.accepted\
                  else models.ParticipationStatusEnum.rejected 
        updated_participation = session\
            .execute(sql.update(models.Participation)\
                .where(models.Participation.id == participation_review["participation_id"])\
                .values(status=participation_status)
            )
    except:
        session.rollback()
        raise
    else:
        session.commit()
    return inserted_review

@DATABASE.db_query
def create_trip_plan(session:Session, trip_plan: dict):
    session.begin()
    try:
        # insert trip_plan
        inserted_trip_plan = session\
                .execute(sql.insert(models.TripPlan)\
                    .values(
                        name=trip_plan["name"],
                        description = trip_plan["description"],
                        distance=trip_plan["distance"],
                        difficulty=trip_plan["difficulty"],
                        is_public=trip_plan["is_public"],
                        creator_id=trip_plan["creator_id"]
                    )
                )
        # insert trip_segments
        for i, _path_id in enumerate(trip_plan["path_ids"]):
            inserted_trip_segment = session\
                .execute(sql.insert(models.TripSegment)\
                    .values(
                        index=i,
                        trip_plan_id = inserted_trip_plan.inserted_primary_key[0],
                        path_id=_path_id
                    )
                )
        pass
    except:
        session.rollback()
        raise
    else:
        session.commit()
    return inserted_trip_plan

@DATABASE.db_query
def create_path(session:Session, path: dict):
    session.begin()
    try:
        inserted_path = session\
            .execute(sql.insert(models.Path)\
                .values(path)
            )
    except Exception as e:
        session.rollback()
        raise
    else:
        session.commit()
    return inserted_path

@DATABASE.db_query
def create_waypoint(session:Session, waypoint: dict):
    session.begin()
    try:
        inserted_path = session\
            .execute(sql.insert(models.Waypoint)\
                .values(waypoint)
            )
    except:
        session.rollback()
        raise
    else:
        session.commit()
    return inserted_path
