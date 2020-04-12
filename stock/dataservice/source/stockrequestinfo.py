#!/usr/bin/env python
# encoding:utf-8

from io import BytesIO
import urllib
import pycurl
import json
from stock.common.utility import *
from stock.common.base import *
from stock.common.enum import *
from stock.dataservice.source.stockrequestbase import *

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

    def getResult(self):
        gLogger.debug("Try to get result from warehouse: url {} param {}".format(self.mUrl, self.mParams))
        lResponseJson = CStockRequestBase.performRequest(self)
        if lResponseJson['success']:
            lResultList = []
            for lItem in lResponseJson['stocks']:
                lResultList.append({ 'symbol': lItem['symbol'], 'name': lItem['name'] })
            gLogger.debug("Get result from warehouse: result {}".format(lResultList))
            return EnumErrorCode.S_OK, lResultList
        else:
            gLogger.error("Get result from warehouse: result {}".format(lResponseJson))
            return EnumErrorCode.E_Warehouse_No_Result
