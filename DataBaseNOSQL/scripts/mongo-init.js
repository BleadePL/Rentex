use "admin";

//dev accounts
db.createUser(
    {
        user: "zgrate",
        pwd: "haslo123",
        roles: [
          { role: "userAdminAnyDatabase", db: "admin" },
          { role: "readWriteAnyDatabase", db: "admin" }
        ]
    }
);

db.createUser(
    {
        user: "bleade",
        pwd: "123456",
        roles: [
          { role: "userAdminAnyDatabase", db: "admin" },
          { role: "readWriteAnyDatabase", db: "admin" }
        ]
    }
);

db.createUser(
    {
        user: "konrad",
        pwd: "123456",
        roles: [
          { role: "userAdminAnyDatabase", db: "admin" },
          { role: "readWriteAnyDatabase", db: "admin" }
        ]
    }
)

//Backend account
db.createUser({
  user: 'backend',
  pwd: 'backendpwd',
  roles: [
    {
      role: 'readWrite',
      db: 'rental',
    },
  ],
});
db.auth('backend', 'backendpwd')



use "rental";

db.createCollection( "Car", {
    validator: { $jsonSchema: {
        bsonType: "object",
        required: [ "brand","vin","regCountryCode","regNumber","modelName","seats","chargeLevel","mileage","currentLocationLat","currentLocationLong","status","activationCost","kmCost","timeCost","esimNumber","esimImei" ],
        properties: {
            brand: {
                bsonType : "string",
                description: "must be a string and is required"
            },
            vin: {
                bsonType : "string",
                description: "must be a string and is required"
            },
            regCountryCode: {
                bsonType : "string",
                description: "must be a string and is required"
            },
            regNumber: {
                bsonType : "string",
                description: "must be a string and is required"
            },
            modelName: {
                bsonType : "string",
                description: "must be a string and is required"
            },
            seats: {
                bsonType : "int",
                description: "must be an int and is required"
            },
            lastUsed:{
                bsonType: "date",
                description: "must be a date"
            },
            chargeLevel: {
                bsonType : "int",
                description: "must be an int and is required"
            },
            mileage: {
                bsonType : "int",
                description: "must be an int and is required"
            },
            currentLocationLat: {
                bsonType: "string",
                description: "must be a string and is required"
            },
            currentLocationLong: {
                bsonType: "string",
                description: "must be a string and is required"
            },
            lastUpdateTime: {
                bsonType: "date",
                description: "must be a date"
            },
            lastService: {
                bsonType: "date",
                description: "must be a date"
            },
            status: {
                enum : ['ACTIVE','RESERVED','SERVICE', 'INUSE', 'INACTIVE', 'UNKNOWN'],
                description: "must be ['ACTIVE','RESERVED','SERVICE', 'INUSE', 'INACTIVE', 'UNKNOWN'] and is required"
            },
            activationCost: {
                bsonType: "string",
                description: "must be a string and is required"
            },
            kmCost: {
                bsonType: "string",
                description: "must be a string and is required"
            },
            timeCost: {
                bsonType: "string",
                description: "must be a string and is required"
            },
            esimNumber: {
                bsonType: "string",
                description: "must be a string and is required"
            },
            esimImei: {
                bsonType: "string",
                description: "must be a string and is required"
            },
            services: {
                bsonType: "array",
                items: {
                    bsonType: "object",
                    required: [ "dateStart", "leftBy", "location"],
                    properties: {
                        dateStart: {
                            bsonType: "date",
                            description: "must be a date and is required"
                        },
                        dateEnd: {
                            bsonType: "date",
                            description: "must be a date"
                        },
                        leftBy: {
                            bsonType: "int",
                            description: "must be an int and is required"
                        },
                        location: {
                            bsonType: "int",
                            description: "must be an int and is required"
                        },
                        description: {
                            bsonType: "string",
                            description: "must be an string"
                        }
                    }
                }
            },
            reservation: {
                bsonType: "int",
                description: "must be an int"
            }
        }
    } }
} );

db.createCollection( "User", {
    validator: { $jsonSchema: {
        bsonType: "object",
        required: [ "pesel","name","surname","address","balance","login","password","email","accountType","status"],
        properties: {
            pesel: {
                bsonType : "string",
                description: "must be a string and is required"
            },
            surname: {
                bsonType : "string",
                description: "must be a string and is required"
            },
            name: {
                bsonType : "string",
                description: "must be a string and is required"
            },
            address: {
                bsonType : "string",
                description: "must be a string and is required"
            },
            driverLicenceNumber: {
                bsonType: "string",
                description: "must be a string"
            },
            driverLicenceExpirationDate: {
                bsonType: "date",
                description: "must be a string"
            },
            balance: {
                bsonType : "string",
                description: "must be a string and is required"
            },
            login: {
                bsonType : "string",
                description: "must be a string and is required"
            },
            password: {
                bsonType : "string",
                description: "must be a string and is required"
            },
            email: {
                bsonType : "string",
                description: "must be a string and is required"
            },
            accountType: {
                enum: ["PERSONAL", "COMPANY", "ORGANISATION", "UNKNOWN"],
                description: "must be [PERSONAL, COMPANY, ORGANISATION, UNKNOWN] and is required"
            },
            activationCode: {
                bsonType : "string",
                description: "must be a string"
            },
            status: {
                enum: ["ACTIVE","INACTIVE","DOCUMENTS","PENDING","PAYMENT","LOCKED","DELETED"],
                description: 'must be ["ACTIVE","INACTIVE","DOCUMENTS","PENDING","PAYMENT","LOCKED","DELETED"] and is required'
            },
            role:{
                enum: ["SERWISANT", "ADMIN", "CLIENT"],
                description: 'must be ["SERWISANT", "ADMIN", "CLIENT"] string'
            },
            rentals: {
                bsonType: "array",
                uniqueItems: true,
                items: {
                    bsonType: "object",
                    required: [ "rentalStart", "car", "ended"],
                    properties: {
                        rentalStart: {
                            bsonType: "date",
                            description: "must be a date and is required"
                        },
                        rentalEnd: {
                            bsonType: "date",
                            description: "must be a date"
                        },
                        mileage: {
                            bsonType: "int",
                            description: "must be an int"
                        },
                        totalCost: {
                            bsonType: "string",
                            description: "must be a string"
                        },
                        ended: {
                            bsonType: "bool",
                            description: "must be a bool"
                        },
                        car: {
                            bsonType: "int"
                        }
                    }
                }
            },
            reservation: {
                bsonType: "object",
                required: [ "reservationStart", "reservationEnd", "reservationCost"],
                properties: {
                    reservationStart: {
                        bsonType: "date",
                        description: "must be a string and is required"
                    },
                    reservationEnd: {
                        bsonType: "date",
                        description: "must be a string and is required"
                    },
                    reservationCost: {
                        bsonType: "string",
                        description: "must be a string and is required"
                    },
                    car: {
                        bsonType: "int"
                    }
                }
            },
            creditCards: {
                bsonType: "array",
                items: {
                    bsonType: "object",
                    required: [ "cardNumber", "expirationDate", "cardHolderName", "cardHolderAddress", "cardHolder"],
                    properties: {
                        cardNumber: {
                            bsonType: "string",
                            description: "must be a string and is required"
                        },
                        expirationDate: {
                            bsonType: "date",
                            description: "must be a string and is required"
                        },
                        cardHolderName: {
                            bsonType: "string",
                            description: "must be a string and is required"
                        },
                        cardHolderAddress: {
                            bsonType: "string",
                            description: "must be a string and is required"
                        }
                    }
                }
            },
            services: {
                bsonType: "array",
                uniqueItems: true,
                items: {
                    bsonType: "int",
                }
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
                enum: ["STATION","CLEAN","SERVICE","SPECIAL_POINT","UNKNOWN"],
                description: 'must be ["STATION","CLEAN","SERVICE","SPECIAL_POINT","UNKNOWN"] and is required'
            },
            locationName: {
                bsonType: "string",
                description: "must be a string and is required"
            },
            locationAddress: {
                bsonType: "string",
                description: "must be a string and is required"
            },
            leaveReward: {
                bsonType: "string",
                description: "must be a string and is required"
            },
            locationLat: {
                bsonType: "string",
                description: "must be a string and is required"
            },
            locationLong: {
                bsonType: "string",
                description: "must be a string and is required"
            },
            services: {
                bsonType: "array",
                items: {
                    bsonType: "int"
                }
            }
        }
    } }
} );

db.createCollection( "RentalArchive", {
    validator: { $jsonSchema: {
        bsonType: "object",
        required: [ "rentalStart", "rentalEnd", "totalCost", "car", "ended", "renter"],
        properties: {
            rentalStart: {
                bsonType: "date",
                description: "must be a date and is required"
            },
            rentalEnd: {
                bsonType: "date",
                description: "must be a date"
            },
            mileage: {
                bsonType: "int",
                description: "must be an int"
            },
            totalCost: {
                bsonType: "string",
                description: "must be a string"
            },
            ended: {
                bsonType: "bool",
                description: "must be a bool"
            },
            car: {
                bsonType: "object",
                required: ["brand","vin","regCountryCode","regNumber","modelName","mileage","activationCost","kmCost","timeCost"],
                properties: {
                    brand: {
                        bsonType : "string",
                        description: "must be a string and is required"
                    },
                    vin: {
                        bsonType : "string",
                        description: "must be a string and is required"
                    },
                    regCountryCode: {
                        bsonType : "string",
                        description: "must be a string and is required"
                    },
                    regNumber: {
                        bsonType : "string",
                        description: "must be a string and is required"
                    },
                    modelName: {
                        bsonType : "string",
                        description: "must be a string and is required"
                    },
                    mileage: {
                        bsonType : "int",
                        description: "must be an int and is required"
                    },
                    activationCost: {
                        bsonType: "string",
                        description: "must be a string and is required"
                    },
                    kmCost: {
                        bsonType: "string",
                        description: "must be a string and is required"
                    },
                    timeCost: {
                        bsonType: "string",
                        description: "must be a string and is required"
                    },
                },
            },
            renter: {
                bsonType: "object",
                required: [ "pesel","name","surname","address","email","accountType"],
                properties: {
                    pesel: {
                        bsonType : "string",
                        description: "must be a string and is required"
                    },
                    surname: {
                        bsonType : "string",
                        description: "must be a string and is required"
                    },
                    name: {
                        bsonType : "string",
                        description: "must be a string and is required"
                    },
                    address: {
                        bsonType : "string",
                        description: "must be a string and is required"
                    },
                    driverLicenceNumber: {
                        bsonType: "string",
                        description: "must be a string"
                    },
                    driverLicenceExpirationDate: {
                        bsonType: "date",
                        description: "must be a string"
                    },
                    email: {
                        bsonType : "string",
                        description: "must be a string and is required"
                    },
                    accountType: {
                        enum: ["PERSONAL", "COMPANY", "ORGANISATION", "UNKNOWN"],
                        description: "must be [PERSONAL, COMPANY, ORGANISATION, UNKNOWN] and is required"
                    },
                }
            }
        
        }   
}}} );