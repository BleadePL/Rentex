DATABASE = "mongodb"
if DATABASE == "mongodb":
    from mongodb import RENTAL_DB

print(RENTAL_DB.getCars()[0].__dict__)
print(RENTAL_DB.getCar("619e306804dd4b629ad3c87c"))
