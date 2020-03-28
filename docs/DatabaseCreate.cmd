use stock
show collections

db.stock_info.drop()
db.createCollection("stock_info", {
   validator: {
      $jsonSchema: {
         bsonType: "object",
         required: [ "symbol", "name", "status", "create_time", "update_time" ],
         properties: {
            symbol: {
               bsonType: "string",
               description: "stock code, required"
            },
            name: {
               bsonType: "string",
               description: "name, required"
            },
            status: {
               bsonType: "int",
               description: "status, 1 is valid, required"
            },
            create_time: {
               bsonType: "long",
               description: "create time, required"
            },
            update_time: {
               bsonType: "long",
               description: "update time, required"
            }
          }
      }
   }
})

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
               bsonType: "long",
               description: "information record timestamp(ms), required"
            },
            record: {
               bsonType: "object",
               required: [ "volume","open","high","low","close","chg","percent","turnoverrate","amount","pe","pb","ps","pcf","market_capital"],
               properties: {
                  volume: {
                     bsonType: "long",
                     description: "exchange times"
                  },
                  open: {
                     bsonType: "double",
                     description: "open price"
                  },
                  high: {
                     bsonType: "double",
                     description: "highest price"
                  },
                  low: {
                     bsonType: "double",
                     description: "lowest price"
                  },
                  close: {
                     bsonType: "double",
                     description: "close price"
                  },
                  chg: {
                     bsonType: "double",
                     description: "price change"
                  },
                  percent: {
                     bsonType: "double",
                     description: "price change percent"
                  },
                  turnoverrate: {
                     bsonType: "double",
                     description: "turn over rete"
                  },
                  amount: {
                     bsonType: "long",
                     description: "exchange money"
                  },
                  pe: {
                     bsonType: "double",
                     description: "pe"
                  },
                  pb: {
                     bsonType: "double",
                     description: "pb"
                  },
                  ps: {
                     bsonType: "double",
                     description: "ps"
                  },
                  pcf: {
                     bsonType: "double",
                     description: "pcf"
                  },
                  market_capital: {
                     bsonType: "long",
                     description: "market capital"
                  }
               }
            }
         }
      }
   }
})

