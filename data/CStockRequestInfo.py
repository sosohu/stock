#!/usr/bin/env python
# encoding:utf-8

from io import BytesIO
import urllib
import pycurl
import json
from CStockRequestBase import *
from Common import *
from DataCommon import *

'''
Input:
    iPage ->  int, page number, each page include 100 results.
Output:
    oInfo ->  list, stock info, [ { symbol, name} ]
'''
class CStockRequestInfo(CStockRequestBase):
    def __init__(self, iPage):
        lUrl = gConfigFileWrapper.getStr('xue_qiu', 'info_url')
        lParams = {}
        lParams['page'] = iPage
        lParams['size'] = '99'
        lParams['order'] = 'desc'
        lParams['orderby'] = 'percent'
        lParams['type'] = '11,12'
        CStockRequestBase.__init__(self, "stock_info", lUrl, lParams)

    '''
    Request exmaple:
        https://xueqiu.com/stock/cata/stocklist.json?page=1&size=100&order=desc&orderby=percent&type=11
    Response example:
        {
            "count":{"count":4981},
            "success":"true",
            "stocks":
                [
                    {
                        "symbol":"SZ000673","code":"000673","name":"dddf","current":"5.13","percent":"10.09",
                        "change":"0.47","high":"5.13","low":"4.58","high52w":"7.48","low52w":"2.63",
                        "marketcapital":"4.06065376746E9","amount":"4.51903229E8","type":"11","pettm":"22.79",
                        "volume":"92230235","hasexist":"false"
                    },
                    ...
                ]
        }
    '''
    def getResult(self):
        lResponseJson = CStockRequestBase.performRequest(self)
        if lResponseJson['success']:
            lResultList = []
            gLogger.info("{}: {}".format(gGetCurrentFunctionName(), lResponseJson))
            for lItem in lResponseJson['stocks']:
                lResultList.append({ 'symbol': lItem['symbol'], 'name': lItem['name'] })
            return EnumErrorCode.S_OK, lResultList
        else:
            gLogger.error("{}: {}".format(gGetCurrentFunctionName(), lResponseJson))
            return EnumErrorCode.S_OK
