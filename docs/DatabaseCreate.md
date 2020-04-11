## Start database

cd data
mongod --dbpath db

## Create database
use stock
show collections

db.stock_info.drop();
db.createCollection("stock_info", {
   validator: {
      $jsonSchema: {
         bsonType: "object",
         required: [ "symbol", "name"],
         properties: {
            symbol: {
               bsonType: "string",
               description: "stock code, required"
            },
            name: {
               bsonType: "string",
               description: "name, required"
            }
          }
      }
   }
});

db.stock_history.drop()
db.createCollection("stock_history", {
   validator: {
      $jsonSchema: {
         bsonType: "object",
         required: [ "symbol", "timestamp", "record" ],
         properties: {
            symbol: {
               bsonType: "string",
               description: "stock code, required"
            },
            timestamp: {
               bsonType: "number",
               description: "information record timestamp(ms), required"
            },
            record: {
               bsonType: "object",
               required: [ "volume","open","high","low","close","chg","percent","turnoverrate","amount","pe","pb","ps","pcf","market_capital"],
               properties: {
                  volume: {
                     bsonType: "number",
                     description: "exchange times"
                  },
                  open: {
                     bsonType: "number",
                     description: "open price"
                  },
                  high: {
                     bsonType: "number",
                     description: "highest price"
                  },
                  low: {
                     bsonType: "number",
                     description: "lowest price"
                  },
                  close: {
                     bsonType: "number",
                     description: "close price"
                  },
                  chg: {
                     bsonType: "number",
                     description: "price change"
                  },
                  percent: {
                     bsonType: "number",
                     description: "price change percent"
                  },
                  turnoverrate: {
                     bsonType: "number",
                     description: "turn over rete"
                  },
                  amount: {
                     bsonType: "number",
                     description: "exchange money"
                  },
                  pe: {
                     bsonType: "number",
                     description: "pe"
                  },
                  pb: {
                     bsonType: "number",
                     description: "pb"
                  },
                  ps: {
                     bsonType: "number",
                     description: "ps"
                  },
                  pcf: {
                     bsonType: "number",
                     description: "pcf"
                  },
                  market_capital: {
                     bsonType: "number",
                     description: "market capital"
                  }
               }
            }
         }
      }
   }
});

