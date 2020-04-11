
## Stock info
Request exmaple:
```
https://xueqiu.com/stock/cata/stocklist.json?page=1&size=100&order=desc&orderby=percent&type=11
```

Response example:
```
{
   "count":{
      "count":4981
   },
   "success":"true",
   "stocks":[
      {
         "symbol":"SZ000673",
         "code":"000673",
         "name":"当代东方",
         "current":"5.13",
         "percent":"10.09",
         "change":"0.47",
         "high":"5.13",
         "low":"4.58",
         "high52w":"7.48",
         "low52w":"2.63",
         "marketcapital":"4.06065376746E9",
         "amount":"4.51903229E8",
         "type":"11",
         "pettm":"22.79",
         "volume":"92230235",
         "hasexist":"false"
      }
   ]
}
```

## Stock history
Request exmaple:
```
https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SH601318&begin=1584280231249&period=day&type=before&count=-1&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance
```

Response example:
```
{
"data":{
    "symbol":"SH601318",
    "column":[
        "timestamp",
        "volume",
        "open",
        "high",
        "low",
        "close",
        "chg",
        "percent",
        "turnoverrate",
        "amount",
        "volume_post",
        "amount_post",
        "pe",
        "pb",
        "ps",
        "pcf",
        "market_capital",
        "balance",
        "hold_volume_cn",
        "hold_ratio_cn",
        "net_volume_cn",
        "hold_volume_hk",
        "hold_ratio_hk",
        "net_volume_hk"
    ],
    "item":[
        [
        1584028800000,
        116615744,
        72.14,
        75.98,
        72.1,
        74.71,
        -1.94,
        -2.53,
        1.08,
        8.615758935E9,
        null,
        null,
        9.141,
        2.029,
        1.168410807851535,
        5.47502189156327,
        1.365716835741E12,
        2.516187324845E10,
        756862382,
        6.98,
        -13934206,
        null,
        null,
        null
        ]
    ]
},
"error_code":0,
"error_description":""
}
```