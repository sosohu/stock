#!/usr/bin/env python
# encoding:utf-8

from pymongo import MongoClient

from stock.common.utility import *
from stock.common.enum import *
from stock.dataservice.source.init import *
from stock.dataservice.source.stockrequestbase import gCreateCookieFunc
from stock.dataservice.source.stockrequesthistory import *
from stock.dataservice.source.stockrequestinfo import *
from stock.dataservice.source.databaseservice import *

class CUpdateService():
    def __init__(self):
        gCreateCookieFunc()
        return
    def __del__(self):
        return

    def updateStocksInfo(self):
        for i in range(1, gConfigFileWrapper.getInt('xue_qiu', 'info_count')):
            lCStockInfoRequest = CStockRequestInfo(i)
            lRetcode, lRetList = lCStockInfoRequest.getResult()
            if gFaiedFunc(lRetcode):
                return lRetcode
            for lItem in lRetList:
                lNewStockInfo = CStockInfo(lItem['symbol'])
                lNewStockInfo.populate(lItem)

                lCount = gDatabaseService.countStockInfo(lItem['symbol'])
                if lCount > 0:
                    gDatabaseService.removeStockInfo(lItem['symbol'])

                hr = gDatabaseService.updateStockInfo(lItem['symbol'], lNewStockInfo)
                if hr != EnumErrorCode.S_OK:
                    gLogger.warning("{}: {}. Update failed: {}".format(gGetCurrentFunctionName(), lItem['symbol'], hr))
                    continue

        return EnumErrorCode.S_OK

    def updateStockHistory(self, iSymbol, iTimestamp, iCount = -1):
        lCStockHistoryRequest = CStockRequestHistory(iSymbol, iTimestamp, -1)
        lRetcode, lRetList = lCStockHistoryRequest.getResult()

        if gFaiedFunc(lRetcode):
            return lRetcode

        for lItem in lRetList:
            lNewStockHistory = CStockHistory(iSymbol, lItem['timestamp'])
            lNewStockHistory.populate(lItem)

            lCount = gDatabaseService.countStockHistory(iSymbol, lItem['timestamp'])
            if lCount > 0:
                gDatabaseService.removeStockHistory(iSymbol, lItem['timestamp'])

            hr = gDatabaseService.updateStockHistory(iSymbol, lItem['timestamp'], lNewStockHistory)
            if hr != EnumErrorCode.S_OK:
                gLogger.warning("{}: {} {}. Update failed: {}".format(gGetCurrentFunctionName(), iSymbol, lItem['timestamp'], hr))
                continue

        return EnumErrorCode.S_OK


gUpdateService = CUpdateService()