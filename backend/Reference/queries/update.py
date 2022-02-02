from sqlalchemy.orm import Session, selectinload, joinedload, noload
from po_api import DATABASE
import po_api.database.orm.models as models
import sqlalchemy as sql
from po_api.database.db import Database


@DATABASE.db_query
def update_path(session: Session, path_id:int, changes: dict):
    session.begin()
    try:
        path_to_update = session.execute(
            sql.update(models.Path)\
                .where(models.Path.id == path_id)\
                .values(changes)
        )
    except:
        session.rollback()
        raise
    else:
        session.commit()
    return path_to_update