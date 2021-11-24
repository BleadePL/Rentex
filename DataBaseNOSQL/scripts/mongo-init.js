use "admin";

//dev accounts
db.createUser(
    {
        user: "zgrate",
        pwd: "haslo123",
        roles: [ {role:"userAdminAnyDatabase", db: "admin"}]
    }
);

db.createUser(
    {
        user: "bleade",
        pwd: "123456",
        roles: [ {role:"userAdminAnyDatabase", db: "admin"}]
    }
);

db.createUser(
    {
        user: "konrad",
        pwd: "123456",
        roles: [ {role:"userAdminAnyDatabase", db: "admin"}]
    }
)

//Backend account
db.createUser({
  user: 'backend',
  pwd: 'backendpwd',
  roles: [
    {
      role: 'readWrite',
      db: 'mongodb',
    },
  ],
});
db.auth('backend', 'backendpwd')



use "rental";

db.createCollection( "Car", {
    validator: { $jsonSchema: {
            bsonType: "object",
            required: [ "brand","vin","regCountryCode","regNumber","modelName","passengerNumber","chargeLevel","mileage","currentLocationLat","currentLocationLong","status","activationCost","kmCost","minCost","esimNumber","esimImei" ],
            properties: {
                brand: {
                    bsonType : "string"
                },
                vin: {
                    bsonType : "string"
                },
                regCountryCode: {
                    bsonType : "string"
                },
                regNumber: {
                    bsonType : "string"
                },
                modelName: {
                    bsonType : "string"
                },
                passengerNumber: {
                    bsonType : "int"
                },
                lastUsed:{
                    bsonType: "date"
                },
                chargeLevel: {
                    bsonType : "int"
                },
                mileage: {
                    bsonType : "int"
                },
                currentLocationLat: {
                    bsonType: "string"
                },
                currentLocationLong: {
                    bsonType: "string"
                },
                lastUpdateTime: {
                    bsonType: "date"
                },
                lastService: {
                    bsonType: "date"
                },
                status: {
                    enum : ['ACTIVE','RESERVED','SERVICE', 'INUSE', 'INACTIVE', 'UNKNOWN']
                },
                activationCost: {
                    bsonType: "string"
                },
                kmCost: {
                    bsonType: "string"
                },
                minCost: {
                    bsonType: "string"
                },
                esimNumber: {
                    bsonType: "string"
                },
                esimImei: {
                    bsonType: "string"
                },
            }
        } }
} );

db.createCollection( "Client", {
    validator: { $jsonSchema: {
            bsonType: "object",
            required: [ "pesel","name","surname","balance","login","password","email","accountType","activationCode","status","role"],
            properties: {
                pesel: {
                    bsonType : "string"
                },
                surname: {
                    bsonType : "string"
                },
                name: {
                    bsonType : "string"
                },
                address: {
                    bsonType : "string"
                },
                driverLicenceNumber: {
                    bsonType: "string"
                },
                driverLicenceExpirationDate: {
                    bsonType: "date",
                },
                balance: {
                    bsonType : "string"
                },
                login: {
                    bsonType : "string"
                },
                password: {
                    bsonType : "string"
                },
                email: {
                    bsonType : "string"
                },
                accountType: {
                    enum: ["PERSONAL", "COMPANY", "ORGANISATION", "UNKNOWN"]
                },
                activationCode: {
                    bsonType : "string"
                },
                status: {
                    enum: ["ACTIVE","INACTIVE","DOCUMENTS","PENDING","PAYMENT","LOCKED","DELETED"]
                },
                role:{
                    enum: ["SERWISANT", "ADMIN", "CLIENT"]
                }
            }
        } }
} );

db.createCollection( "Location", {
    validator: { $jsonSchema: {
            bsonType: "object",
            required: [ "locationType", "locationName","locationAddress","leaveReward","locationLat","locationLong"],
            properties: {
                locationType: {
                    enum: ["STATION","CLEAN","SERVICE","SPECIAL_POINT","UNKNOWN"]
                },
                locationName: {
                    bsonType: "string"
                },
                locationAddress: {
                    bsonType: "string"
                },
                leaveReward: {
                    bsonType: "string"
                },
                locationLat: {
                    bsonType: "string"
                },
                locationLong: {
                    bsonType: "string"
                },
            }
        } }
} );

db.createCollection( "Reservation", {
    validator: { $jsonSchema: {
            bsonType: "object",
            required: [ "reservationStart", "reservationEnd", "reservationCost"],
            properties: {
                reservationStart: {
                    bsonType: "date"
                },
                reservationEnd: {
                    bsonType: "date"
                },
                reservationCost: {
                    bsonType: "string"
                }
            }
        } }
} );

db.createCollection( "Rental", {
    validator: { $jsonSchema: {
            bsonType: "object",
            required: [ "rentalStart", "rentalEnd", "rentalCost"],
            properties: {
                rentalStart: {
                    bsonType: "date"
                },
                rentalEnd: {
                    bsonType: "date"
                },
                mileage: {
                    bsonType: "string"
                },
                totalCost: {
                    bsonType: "string"
                },
                ended: {
                    bsonType: "bool"
                }
            }
        } }
} );
db.createCollection( "CreditCard", {
    validator: { $jsonSchema: {
            bsonType: "object",
            required: [ "cardNumber", "expirationDate", "cardHholderName", "cardHolderAddress"],
            properties: {
                cardNumber: {
                    bsonType: "string"
                },
                expirationDate: {
                    bsonType: "date",
                },
                cardHolderName: {
                    bsonType: "string"
                },
                cardHolderAddress: {
                    bsonType: "string"
                },
            }
        } }

} );
