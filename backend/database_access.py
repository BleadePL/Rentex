from db_interface import DatabaseInterface

DATABASE = "mongodb"
RENTAL_DB: DatabaseInterface
if DATABASE == "mongodb":
    from mongodb import RENTAL_DB
