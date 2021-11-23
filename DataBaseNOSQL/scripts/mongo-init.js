db.auth('root', 'admin')
db.createUser({
  user: 'root',
  pwd: 'admin',
  roles: [
    {
      role: 'readWrite',
      db: 'mongodb',
    },
  ],
});

db.createCollection( "Car", {
    validator: { $jsonSchema: {
       bsonType: "object",
       required: [ "brand","vin","regCountryCode","regNumber","modelName","passengerNumber","chargeLevel","mileage","currentLocationLat","currentLocationLong","status","activationCost","kmCost","minCost","esimNumber","esimImei" ],
       properties: {
          brand: {
             bsonType : "string",
             maxLength: 30,
          },
          vin: {
            bsonType : "string",
            maxLength: 17,
            unique: true
         },
         regCountryCode: {
            bsonType : "string",
            maxLength: 2,
         },
         regNumber: {
            bsonType : "string",
            maxLength: 10,
         },
         modelName: {
            bsonType : "string",
            maxLength: 50,
         },
         passengerNumber: {
            bsonType : "int",
            minimum: 1,
            maximum: 255,
         },
         lastUsed:{
            bsonType: "date"
         },
         chargeLevel: {
            bsonType : "int",
            minimum: 0,
            maximum: 100,
         },
         mileage: {
            bsonType : "int"
         },
         currentLocationLat: {
            bsonType: "string",
            maxLength: 20
         },
         currentLocationLong: {
            bsonType: "string",
            maxLength: 20
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
            bsonType: "String",
            maxLength: 30
         },
         kmCost: {
            bsonType: "String",
            maxLength: 30
         },
         minCost: {
            bsonType: "String",
            maxLength: 30
         },
         esimNumber: {
            bsonType: "String",
            maxLength: 30,
            unique: true,
         },
         esimImei: {
            bsonType: "String",
            maxLength: 30,
            unique: true,
         },
       }
    } }
 } )

 db.createCollection( "Client", {
   validator: { $jsonSchema: {
      bsonType: "object",
      required: [ "pesel","name","surname","balance","login","password","email","accountType","activationCode","status","role"],
      properties: {
         pesel: {
            bsonType : "string",
            maxLength: 11,
         },
         surname: {
            bsonType : "string",
            maxLength: 30,
         },
         name: {
            bsonType : "string",
            maxLength: 30,
         },
         address: {
            bsonType : "string",
            maxLength: 255,
         },
         driverLicenceNumber: {
                  bsonType: "string",
                  maxLength: 15
         },
         driverLicenceExpirationDate: {
                  bsonType: "date",
         },
         balance: {
            bsonType : "string",
            maxLength: 20,
         },
         login: {
            bsonType : "string",
            maxLength: 20,
         },
         password: {
            bsonType : "string",
            maxLength: 64,
         },
         email: {
            bsonType : "string",
            maxLength: 50,
         },
         accountType: {
            enum: ["PERSONAL", "COMPANY", "ORGANISATION", "UNKNOWN"]
         },
         activationCode: {
            bsonType : "string",
            maxLength: 64,
         },
         status: {
            enum: ["ACTIVE","INACTIVE","DOCUMENTS","PENDING","PAYMENT","ADMIN","LOCKED","DELETED"]
         },
         role:{
            enum: ["SERWISANT", "ADMIN", "CLIENT"]
         }
      }
   } }
} )

db.createCollection( "Location", {
   validator: { $jsonSchema: {
      bsonType: "object",
      required: [ "locationType", "locationName","locationAddress","leaveReward","locationLat","locationLong"],
      properties: {
         locationType: {
            enum: ["STATION","CLEAN","SERVICE","SPECIAL_POINT","UNKNOWN"]
         },
         locationName: {
            bsonType: "string",
            maxLength: 100
         },
         locationAddress: {
            bsonType: "string",
            maxLength: 255
         },
         leaveReward: {
            bsonType: "string",
            maxLength: 20
         },
         locationLat: {
            bsonType: "string",
            maxLength: 20
         },
         locationLong: {
            bsonType: "string",
            maxLength: 20
         },
      }
   } }
} )

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
            bsonType: "string",
            maxLength: 20
         }
      }
   } }
} )

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
            bsonType: "string",
            maxLength: 20
         },
         totalCost: {
            bsonType: "string",
            maxLength: 20
         },
         ended: {
            bsonType: "bool"
         }
      }
   } }
} )
db.createCollection( "creditCard", {
   validator: { $jsonSchema: {
      bsonType: "object",
      required: [ "cardNumber", "expirationDate", "cardHholderName", "cardHolderAddress"],
      properties: {
         cardNumber: {
            bsonType: "string",
            maxLength: 16
         },
         expirationDate: {
            bsonType: "date",
         },
         cardHolderName: {
            bsonType: "string",
            maxLength: 60
         },
         cardHolderAddress: {
            bsonType: "string",
            maxLength: 255
         },
      }
   } }
   
} )