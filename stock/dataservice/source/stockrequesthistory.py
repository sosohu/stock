#!/usr/bin/env python
# encoding:utf-8

from io import BytesIO
import urllib
import pycurl
import json
from stock.common.utility import *
from stock.common.enum import *
from stock.common.base import *
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
    def __init__(self, iSymbol, iBeginTime, iEndTime):
        self.mSymbol = iSymbol
        self.mCount = gGetDiffDaysFunc(iBeginTime, iEndTime)

        lUrl = gConfigFileWrapper.getStr('xue_qiu', 'history_url')
        lParams = {}
        lParams['symbol'] = iSymbol
        lParams['begin'] = iBeginTime * 1000
        lParams['period'] = 'day'
        lParams['type'] = 'after'
        lParams['count'] = self.mCount
        lParams['indicator'] = 'kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance'
        CStockRequestBase.__init__(self, "stock_history", lUrl, lParams)

    def getResult(self):
        gLogger.debug("Try to get result from warehouse: url {} param {}".format(self.mUrl, self.mParams))
        lResponseJson = CStockRequestBase.performRequest(self)
        if not self.__hValidateResult(lResponseJson):
            return EnumErrorCode.E_Validate_Fail, None

        if len(lResponseJson["data"]["item"]) == 0:
            return EnumErrorCode.E_Warehouse_No_Result, None

        lResultList = []
        for lItem in lResponseJson["data"]["item"]:
            lResultItem = {}
            for i in range(0, len(lColumnName)):
                if lColumnName[i][1]:
                    if lColumnName[i][0] == 'timestamp':
                        lItem[i] = lItem[i] / 1000
                    lResultItem[lColumnName[i][0]] = lItem[i]
            lResultList.append(lResultItem)

        gLogger.debug("Get result from warehouse: result {}".format(lResultList))
        return EnumErrorCode.S_OK, lResultList

    def __hValidateResult(self, iDataJson):
        if iDataJson["error_code"] != 0:
            gLogger.error("Warehouse query stock {} return error code: {}, error description: {}"\
                            .format(self.mSymbol, iDataJson["error_code"], iDataJson["error_description"]))
            return False
        if not iDataJson["data"]:
            gLogger.error("Warehouse query stock {} return no data.".format(self.mSymbol))
            return False

        if iDataJson["data"]["symbol"] != self.mSymbol:
            gLogger.error("Warehouse query stock {} return inconsistant symbol: {}"\
                            .format(self.mSymbol, iDataJson["data"]["symbol"]))
            return False

        if not iDataJson["data"]["column"]:
            gLogger.error("Warehouse query stock {} return ino column".format(self.mSymbol))
            return False
        
        if not iDataJson["data"]["item"]:
            gLogger.error("Warehouse query stock {} return ino item".format(self.mSymbol))
            return False

        for i in range(0, len(lColumnName)):
            if lColumnName[i][1]:
                if iDataJson["data"]["column"][i] != lColumnName[i][0]:
                    gLogger.error("Warehouse query stock {} return column inconsistent {} vs {}"\
                                    .format(self.mSymbol, iDataJson["data"]["column"][i], lColumnName[i][0]))
                    return False
        
        return True
