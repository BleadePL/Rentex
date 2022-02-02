from db_interface import DatabaseInterface

DATABASE = "sql"
RENTAL_DB: DatabaseInterface
if DATABASE == "mongodb":
    from mongodb import RENTAL_DB
elif DATABASE == "sql":
    from sqlAlchemy import RENTAL_DB
