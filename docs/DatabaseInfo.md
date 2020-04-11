
# Datase
stock

# Collections
## stock_info

### struct
```
{
  symbol: "string", # SH601318
  name: "string", # 中国平安
}
```


## stock_history

<
中国平安(SH:601318)
¥69.00+1.19 +1.75%
最高：69.40	今开：68.71	涨停：74.59	成交量：88.73万手
最低：67.35	昨收：67.81	跌停：61.03	成交额：60.81亿
量比：0.86	换手：0.82%	市盈率(动)：8.44	市盈率(TTM)：8.44
委比：26.06%	振幅：3.02%	市盈率(静)：8.44	市净率：1.87
每股收益：8.17	股息(TTM)：2.05	总股本：182.80亿	总市值：1.26万亿
每股净资产：36.82	股息率(TTM)：2.97%	流通股：108.33亿	流通值：7474.54亿
52周最高：92.50	52周最低：66.32	货币单位：CNY

### struct

```
{ 
  symbol: "string",  # SH601318
  timestamp: "timestamp",   # 1584633600000
  record: { 
          volume: "long", # 88726935, 成交量：88.73万手
          open: "double", # 68.71, 今开：68.71元
          high: "double", # 69.4, 最高：69.40元
          low: "double", # 67.35, 最低：67.35元
          close: "double", # 69.0, 收盘: 69.0元
          chg: "double", # 1.19, 涨跌: +1.19元
          percent: "double", # 1.75, 涨跌幅: +1.75%
          turnoverrate: "double", # 0.82, 换手：0.82%
          amount: "long", # 6.081161074E9, 成交额：60.81亿
          pe: "double", # 8.4423, 市盈率(动)：8.44
          pb: "double", # 1.8738, 市净率：1.87
          ps: "double", # 1.0791 , 市销率
          pcf: "double", # 5.0566, 市现率
          market_capital: "long", # 1.26133665729E12, 总市值：1.26万亿
        }
}
```
