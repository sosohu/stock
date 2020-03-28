#!/usr/bin/env python
# encoding:utf-8

from io import BytesIO
import urllib
import pycurl
import json
from stock.common.utility import *
from stock.common.enum import *
from stock.dataservice.source.init import *
from stock.dataservice.source.stockrequestbase import *

lColumnName = [ \
        ["timestamp", True], \
        ["volume", True], \
        ["open", True], \
        ["high", True], \
        ["low", True], \
        ["close", True], \
        ["chg", True], \
        ["percent", True], \
        ["turnoverrate", True], \
        ["amount", True], \
        ["volume_post", False], \
        ["amount_post", False], \
        ["pe", True], \
        ["pb", True], \
        ["ps", True], \
        ["pcf", True], \
        ["market_capital", True], \
        ["balance", False], \
        ["hold_volume_cn", False], \
        ["hold_ratio_cn", False], \
        ["net_volume_cn", False], \
        ["hold_volume_hk", False], \
        ["hold_ratio_hk", False], \
        ["net_volume_hk", False]
    ]

'''
Input:
    iSymbol ->  string, stock symbol
    iBeginTime -> long, last day timestamp
    iCount -> int, count of days before iBeginTime
Output:
    oInfo ->  list, stock info, [ { symbol, name} ]
'''
class CStockRequestHistory(CStockRequestBase):
    def __init__(self, iSymbol, iBeginTime, iCount):
        self.mSymbol = iSymbol
        self.mCount = iCount

        lUrl = gConfigFileWrapper.getStr('xue_qiu', 'history_url')
        lParams = {}
        lParams['symbol'] = iSymbol
        lParams['begin'] = iBeginTime
        lParams['period'] = 'day'
        lParams['type'] = 'before'
        lParams['count'] = -iCount
        lParams['indicator'] = 'kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance'
        CStockRequestBase.__init__(self, "stock_history", lUrl, lParams)

    def getResult(self):
        lResponseJson = CStockRequestBase.performRequest(self)
        print lResponseJson
        if not self.__hValidateResult(lResponseJson):
            return EnumErrorCode.E_Validate_Fail

        for lItem in lResponseJson["data"]["item"]:
            print lItem
        return EnumErrorCode.S_OK

    def __hValidateResult(self, iDataJson):
        if iDataJson["error_code"] != 0:
            gLogger.error("{} {} Query return error code: {}, error description: {}"\
                            .format(gGetCurrentFunctionName(), self.mSymbol, iDataJson["error_code"], iDataJson["error_description"]))
            return False
        if not iDataJson["data"]:
            gLogger.error("{} {} Query return no data.".format(gGetCurrentFunctionName(), self.mSymbol))
            return False

        if iDataJson["data"]["symbol"] != self.mSymbol:
            gLogger.error("{} {} Query return inconsistant symbol: {}"\
                            .format(gGetCurrentFunctionName(), self.mSymbol, iDataJson["data"]["symbol"]))
            return False

        if not iDataJson["data"]["column"]:
            gLogger.error("{} {} Query return ino column".format(gGetCurrentFunctionName(), self.mSymbol))
            return False
        
        if not iDataJson["data"]["item"]:
            gLogger.error("{} {} Query return ino item".format(gGetCurrentFunctionName(), self.mSymbol))
            return False

        for i in range(0, len(lColumnName)):
            if lColumnName[i][1]:
                if iDataJson["data"]["column"][i] != lColumnName[i][0]:
                    gLogger.error("{} {} Query return column inconsistent {} vs {}"\
                                    .format(gGetCurrentFunctionName(), self.mSymbol, iDataJson["data"]["column"][i], lColumnName[i][0]))
                    return False
        
        return True
