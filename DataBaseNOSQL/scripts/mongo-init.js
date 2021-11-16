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
       required: [ "phone" ],
       properties: {
          producerCode: {
             bsonType : "string",
             maxLength: 3,
          },
          vin: {
            bsonType : "string",
            maxLength: 17,
         },
         regCountryCode: {
            bsonType : "string",
            maxLength: 2,
         },
         regNumber: {
            bsonType : "string",
            maxLength: 8,
         },
         modelName: {
            bsonType : "string",
            maxLength: 20,
         },
         regNumber: {
            bsonType : "string",
            maxLength: 8,
         }, 
         passengerNumber: {
            bsonType : "int",
            minimum: 1,
            maximum: 255,
         },
         fuelLevel: {
            bsonType : "int",
            minimum: 0,
            maximum: 100,
         },
         mileage: {
            bsonType : "int"
         },
         currentLocationLatitude: {
            bsonType : "double" 
         },
         currentLocationLongtitude: {
            bsonType : "double" 
         },
         active: {
            bsonType: "bool"
         }
       }
    } }
 } )