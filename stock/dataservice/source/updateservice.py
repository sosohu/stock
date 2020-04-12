#!/usr/bin/env python
# encoding:utf-8

from pymongo import MongoClient

from stock.common.utility import *
from stock.common.base import *
from stock.common.enum import *
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
                    gLogger.warning("Update stock {} info failed: result {}.".format(lItem['symbol'], hr))
                    continue

        return EnumErrorCode.S_OK

    # update [iBeginTimestamp, iEndTimestamp)
    def updateStockHistory(self, iSymbol, iBeginTimestamp, iEndTimestamp):
        lCStockHistoryRequest = CStockRequestHistory(iSymbol, iBeginTimestamp, iEndTimestamp)
        lRetcode, lRetList = lCStockHistoryRequest.getResult()

        if gFaiedFunc(lRetcode):
            return lRetcode

        for lItem in lRetList:
            lNewStockHistory = CStockHistory(iSymbol, lItem['timestamp'])
            hr = lNewStockHistory.populate(lItem)
            if hr != EnumErrorCode.S_OK:
                continue

            lCount = gDatabaseService.countStockHistory(iSymbol, lItem['timestamp'])
            if lCount > 0:
                gDatabaseService.removeStockHistory(iSymbol, lItem['timestamp'])

            hr = gDatabaseService.updateStockHistory(iSymbol, lItem['timestamp'], lNewStockHistory)
            if hr != EnumErrorCode.S_OK:
                gLogger.warning("Update stock {} history at timestamp {} failed: result {}.".format(iSymbol, lItem['timestamp'], hr))
                continue

        return EnumErrorCode.S_OK

    def updateAllStockHistory(self):
        lLastUpdateTimeStamp = gDatabaseService.getPropertyValue('update_time')
        if lLastUpdateTimeStamp is None:
            lLastUpdateTimeStamp = gConfigFileWrapper.getLong('stock', 'start_time')
        else:
            lLastUpdateTimeStamp = int(lLastUpdateTimeStamp)

        lTodayTimeStamp = gGetTodayTimeStampFunc()

        lCount = gGetDiffDaysFunc(lLastUpdateTimeStamp, lTodayTimeStamp)
        if lCount == 0:
            gLogger.debug("Database has already had the lastest result, do not need to update")
            return EnumErrorCode.S_OK

        lList = []
        hr = gDatabaseService.getStockSymbols(lList)
        if gFaiedFunc(hr):
            return hr

        for lItem in lList:
            self.updateStockHistory(lItem, lLastUpdateTimeStamp, lTodayTimeStamp)

        gDatabaseService.setPropertyValue('update_time', str(lTodayTimeStamp))

        return EnumErrorCode.S_OK

gUpdateService = CUpdateService()