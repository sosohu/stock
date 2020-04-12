#!/usr/bin/env python
# encoding:utf-8

import time

from pymongo import MongoClient
from enum import Enum

from stock.common.utility import *
from stock.common.base import *
from stock.objects.stockinfo import *
from stock.objects.stockhistory import *
from stock.objects.stockinstance import *

class EnumColPropInfo(Enum):
    PropName = 1
    PropVal = 2

class EnumColStockInfo(Enum):
    Symbol = 1
    Name = 2
    Status = 3
    CreateTime = 4
    UpdateTime = 5

class EnumColStockHistory(Enum):
    Symbol = 1
    TimeStamp = 2
    Record = 3

class EnumColStockHistoryRecord(Enum):
    Volume = 1
    Open = 2
    High = 3
    Low = 4
    Close = 5
    Chg = 6
    Percent = 7
    Turnoverrate = 8
    Amount = 9
    Pe = 10
    Pb = 11
    Ps = 12
    Pcf = 13
    MarketCapital = 14

class CDatabaseService():
    def __init__(self):
        self.mMongoClient = MongoClient(gConfigFileWrapper.getStr('mongo', 'connect_url'))
        self.mDb = self.mMongoClient[gConfigFileWrapper.getStr('mongo', 'database')]

        self.mColPropInfoName = 'property_info'
        self.mColPropInfo = self.mDb[self.mColPropInfoName]
        self.mColPropInfoKeys = {}
        self.mColPropInfoKeys[EnumColPropInfo.PropName] = 'prop_name'
        self.mColPropInfoKeys[EnumColPropInfo.PropVal] = 'prop_val'

        self.mColStockInfoName = 'stock_info'
        self.mColStockInfo = self.mDb['stock_info']
        self.mColStockInfoKeys = {}
        self.mColStockInfoKeys[EnumColStockInfo.Symbol] = 'symbol'
        self.mColStockInfoKeys[EnumColStockInfo.Name] = 'name'

        self.mColStockHistName = 'stock_history'
        self.mColStockHist = self.mDb['stock_history']
        self.mColStockHistKeys = {}
        self.mColStockHistKeys[EnumColStockHistory.Symbol] = 'symbol'
        self.mColStockHistKeys[EnumColStockHistory.TimeStamp] = 'timestamp'
        self.mColStockHistKeys[EnumColStockHistory.Record] = 'record'
        self.mColStockHistRecordKeys = {}
        self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Volume] = 'volume'
        self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Open] = 'open'
        self.mColStockHistRecordKeys[EnumColStockHistoryRecord.High] = 'high'
        self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Low] = 'low'
        self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Close] = 'close'
        self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Chg] = 'chg'
        self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Percent] = 'percent'
        self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Turnoverrate] = 'turnoverrate'
        self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Amount] = 'amount'
        self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Pe] = 'pe'
        self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Pb] = 'pb'
        self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Ps] = 'ps'
        self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Pcf] = 'pcf'
        self.mColStockHistRecordKeys[EnumColStockHistoryRecord.MarketCapital] = 'market_capital'
        return

    def __del__(self):
        return

    def getPropertyValue(self, iPropName):
        lQuery = {}
        lQuery[self.mColPropInfoKeys[EnumColPropInfo.PropName]] = iPropName

        gLogger.debug("Collection {} query : query {}, projection {{}}.".format(self.mColPropInfoName, lQuery))
        lResultCursor = self.mColPropInfo.find(lQuery)
        lResultList = list(lResultCursor)
        gLogger.debug("Collection {} query : result {}.".format(self.mColPropInfoName, lResultList))

        if len(lResultList) > 1:
            gLogger.warning("{} has {} records in property_info collection".format(iPropName, len(lResultList)))
        elif len(lResultList) == 1:
            return lResultList[0][self.mColPropInfoKeys[EnumColPropInfo.PropVal]]

        return 

    def setPropertyValue(self, iPropName, iPropValue):
        lQuery = {}
        lQuery[self.mColPropInfoKeys[EnumColPropInfo.PropName]] = iPropName
        lData = {}
        lData["$set"] = {}
        lData["$set"][self.mColPropInfoKeys[EnumColPropInfo.PropVal]] = iPropValue

        gLogger.debug("Collection {} update : query {} , data: {}.".format(self.mColPropInfoName, lQuery, lData))
        hr = self.mColPropInfo.update(lQuery, lData, upsert = True)
        gLogger.debug("Collection {} update : result: {}".format(self.mColPropInfoName, hr))

        return EnumErrorCode.S_OK

    def getStockSymbols(self, oList):
        lProjection = {}
        lProjection[self.mColStockInfoKeys[EnumColStockInfo.Symbol]] = 1

        gLogger.debug("Collection {} query : query {{}}, projection {}.".format(self.mColStockInfoName, lProjection))
        lResultCursor = self.mColStockInfo.find({}, lProjection)
        lResultList = list(lResultCursor)
        gLogger.debug("Collection {} query : result {}.".format(self.mColStockInfoName, lResultList))

        for lItem in lResultList:
            oList.append(lItem[self.mColStockInfoKeys[EnumColStockInfo.Symbol]])

        return EnumErrorCode.S_OK


    def countStockInfo(self, iSymbol):
        lQuery = {}
        lQuery[self.mColStockInfoKeys[EnumColStockInfo.Symbol]] = iSymbol
        
        gLogger.debug("Collection {} query : query {}, projection {{}}.".format(self.mColStockInfoName, lQuery))
        lResultCursor = self.mColStockInfo.find(lQuery)
        lResultList = list(lResultCursor)
        gLogger.debug("Collection {} query : result {}.".format(self.mColStockInfoName, lResultList))
        return len(lResultList)

    def getStockInfo(self, iSymbol, oStockInfo):
        lQuery = {}
        lQuery[self.mColStockInfoKeys[EnumColStockInfo.Symbol]] = iSymbol
        
        gLogger.debug("Collection {} query : query {}, projection {{}}.".format(self.mColStockInfoName, lQuery))
        lResultCursor = self.mColStockInfo.find(lQuery)
        lResultList = list(lResultCursor)
        gLogger.debug("Collection {} query : result {}.".format(self.mColStockInfoName, lResultList))
        if len(lResultList) > 1:
            gLogger.warning("{}: {} has {} records".format(self.mColStockInfoName, iSymbol, len(lResultList)))
            return EnumErrorCode.E_Database_Multi_Result
        elif len(lResultList) == 1:
            oStockInfo.setName(lResultList[0][self.mColStockInfoKeys[EnumColStockInfo.Name]])
            return EnumErrorCode.S_OK
        else:            
            return EnumErrorCode.E_Database_No_Result

    def updateStockInfo(self, iSymbol, iStockInfo):
        if not isinstance(iStockInfo, CStockInfo):
            return EnumErrorCode.E_INVALID_ARG

        lQuery = {}
        lQuery[self.mColStockInfoKeys[EnumColStockInfo.Symbol]] = iSymbol
        lData = {}
        lData["$set"] = {}
        lData["$set"][self.mColStockInfoKeys[EnumColStockInfo.Name]] = iStockInfo.getName()

        gLogger.debug("Collection {} update : query {}, data {}.".format(self.mColStockInfoName, lQuery, lData))
        hr = self.mColStockInfo.update(lQuery, lData, upsert = True)
        gLogger.debug("Collection {} update : result {}.".format(self.mColStockInfoName, hr))

        return EnumErrorCode.S_OK

    def removeStockInfo(self, iSymbol):
        lQuery = {}
        lQuery[self.mColStockInfoKeys[EnumColStockInfo.Symbol]] = iSymbol
        gLogger.debug("Collection {} remove : query {}.".format(self.mColStockInfoName, lQuery))
        hr =  self.mColStockInfo.delete_many(lQuery)
        gLogger.debug("Collection {} remove : result {}.".format(self.mColStockInfoName, hr))

        return EnumErrorCode.S_OK

    def countStockHistory(self, iSymbol, iTimestamp):
        lQuery = {}
        lQuery[self.mColStockHistKeys[EnumColStockHistory.Symbol]] = iSymbol
        lQuery[self.mColStockHistKeys[EnumColStockHistory.TimeStamp]] = iTimestamp

        gLogger.debug("Collection {} query : query {}, projection {{}}.".format(self.mColStockHistName, lQuery))
        lResultCursor = self.mColStockHist.find(lQuery)
        lResultList = list(lResultCursor)
        gLogger.debug("Collection {} query : result {}.".format(self.mColStockHistName, lResultList))
        return len(lResultList)

    def getStockHistory(self, iSymbol, iTimestamp, oStockHistoy):
        lQuery = {}
        lQuery[self.mColStockHistKeys[EnumColStockHistory.Symbol]] = iSymbol
        lQuery[self.mColStockHistKeys[EnumColStockHistory.TimeStamp]] = iTimestamp

        gLogger.debug("Collection {} query : query {}, projection {{}}.".format(self.mColStockHistName, lQuery))
        lResultCursor = self.mColStockHist.find(lQuery)
        lResultList = list(lResultCursor)
        gLogger.debug("Collection {} query : result {}.".format(self.mColStockHistName, lResultList))

        if len(lResultList) > 1:
            gLogger.warning("{}: {} at timestamp {} has {} records".format(self.mColStockHistName, iSymbol, iTimestamp, len(lResultList)))
            return EnumErrorCode.E_Database_Multi_Result
        elif len(lResultList) == 1:
            lRecord = lResultList[0][self.mColStockHistKeys[EnumColStockHistory.Record]]
            oStockHistoy.setVolume(lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Volume]])
            oStockHistoy.setOpenPrice(lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Open]])
            oStockHistoy.setHighPrice(lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.High]])
            oStockHistoy.setLowPrice(lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Low]])
            oStockHistoy.setClosePrice(lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Close]])
            oStockHistoy.setChangePrice(lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Chg]])
            oStockHistoy.setChangePercent(lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Percent]])
            oStockHistoy.setTurnonverRate(lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Turnoverrate]])
            oStockHistoy.setAmount(lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Amount]])
            oStockHistoy.setPE(lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Pe]])
            oStockHistoy.setPB(lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Pb]])
            oStockHistoy.setPS(lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Ps]])
            oStockHistoy.setPCF(lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Pcf]])
            oStockHistoy.setMarketCapital(lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.MarketCapital]])
            return EnumErrorCode.S_OK
        else:            
            return EnumErrorCode.E_Database_No_Result

    def updateStockHistory(self, iSymbol, iTimestamp, iStockHistoy):
        if not isinstance(iStockHistoy, CStockHistory):
            return EnumErrorCode.E_INVALID_ARG

        lQuery = {}
        lQuery[self.mColStockHistKeys[EnumColStockHistory.Symbol]] = iSymbol
        lQuery[self.mColStockHistKeys[EnumColStockHistory.TimeStamp]] = iTimestamp
        lData = {}
        lData["$set"] = {}
        lRecord = {}
        lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Volume]] = iStockHistoy.getVolume()
        lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Open]] = iStockHistoy.getOpenPrice()
        lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.High]] = iStockHistoy.getHighPrice()
        lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Low]] = iStockHistoy.getLowPrice()
        lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Close]] = iStockHistoy.getClosePrice()
        lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Chg]] = iStockHistoy.getChangePrice()
        lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Percent]] = iStockHistoy.getChangePercent()
        lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Turnoverrate]] = iStockHistoy.getTurnoverRate()
        lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Amount]] = iStockHistoy.getAmount()
        lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Pe]] = iStockHistoy.getPE()
        lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Pb]] = iStockHistoy.getPB()
        lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Ps]] = iStockHistoy.getPS()
        lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.Pcf]] = iStockHistoy.getPCF()
        lRecord[self.mColStockHistRecordKeys[EnumColStockHistoryRecord.MarketCapital]] = iStockHistoy.getMarketCapital()
        lData["$set"][self.mColStockHistKeys[EnumColStockHistory.Record]] = lRecord
        
        gLogger.debug("Collection {} update : query {}, data {}.".format(self.mColStockHistName, lQuery, lData))
        hr = self.mColStockHist.update(lQuery, lData, upsert = True)
        gLogger.debug("Collection {} update : result {}.".format(self.mColStockHistName, hr))

        return EnumErrorCode.S_OK

    def removeStockHistory(self, iSymbol, iTimestamp):
        lQuery = {}
        lQuery[self.mColStockHistKeys[EnumColStockHistory.Symbol]] = iSymbol
        lQuery[self.mColStockHistKeys[EnumColStockHistory.TimeStamp]] = iTimestamp
        gLogger.debug("Collection {} remove : query {}.".format(self.mColStockHistName, lQuery))
        hr =  self.mColStockHist.delete_many(lQuery)
        gLogger.debug("Collection {} remove : result {}.".format(self.mColStockHistName, hr))

        return EnumErrorCode.S_OK


gDatabaseService = CDatabaseService()