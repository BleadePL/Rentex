from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from functools import wraps
import typing as t
import sqlalchemy



class Database:
    def __init__(self, url: str) -> None:
        self.engine = sqlalchemy.create_engine(url)
    
    def db_query(self, func) -> t.Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> t.Any:
            try:
                with self.engine.connect() as connection:
                    with Session(bind=connection) as session:
                        result = func(session, *args , **kwargs)
                    return result
            except IntegrityError as int_error:
                return int_error.orig.pgerror
            except SQLAlchemyError as db_error:
                # logging.error(db_error)
                return None
                # raise DBConnectionError()
            except Exception as error:
                # logging.error(error)
                # raise
                return None
        return wrapper

