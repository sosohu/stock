#!/usr/bin/env python
# encoding:utf-8

import time

from pymongo import MongoClient
from enum import Enum

from stock.dataservice.source.init import *
from stock.common.utility import *

class EnumColStockInfo(Enum):
    Symbol = 1
    Name = 2
    Status = 3
    CreateTime = 4
    UpdateTime = 5

class CDatabaseService():
    def __init__(self):
        self.mMongoClient = MongoClient(gConfigFileWrapper.getStr('mongo', 'connect_url'))
        self.mDb = self.mMongoClient[gConfigFileWrapper.getStr('mongo', 'database')]

        self.mColStockInfo = self.mDb['stock_info']
        self.mColStockInfoKeys = {}
        self.mColStockInfoKeys[EnumColStockInfo.Symbol] = 'symbol'
        self.mColStockInfoKeys[EnumColStockInfo.Name] = 'name'
        self.mColStockInfoKeys[EnumColStockInfo.Status] = 'status'
        self.mColStockInfoKeys[EnumColStockInfo.CreateTime] = 'create_time'
        self.mColStockInfoKeys[EnumColStockInfo.UpdateTime] = 'update_time'

        self.mColStockHist = self.mDb['stock_history']
        return

    def __del__(self):
        return

    def getStockInfo(self, iSymbol):
        lQuery = {}
        lQuery[self.mColStockInfoKeys[EnumColStockInfo.Symbol]] = iSymbol
        gLogger.debug("{}: {}".format(gGetCurrentFunctionName(), lQuery))
        return self.mColStockInfo.find(lQuery)

    def updateStockInfo(self, iSymbol, iName, iStatus, iCreateTime):
        lQuery = {}
        lQuery[self.mColStockInfoKeys[EnumColStockInfo.Symbol]] = iSymbol
        lData = {}
        lData["$set"] = {}
        lData["$set"][self.mColStockInfoKeys[EnumColStockInfo.Name]] = iName
        lData["$set"][self.mColStockInfoKeys[EnumColStockInfo.Status]] = iStatus
        lData["$set"][self.mColStockInfoKeys[EnumColStockInfo.CreateTime]] = iCreateTime
        lData["$set"][self.mColStockInfoKeys[EnumColStockInfo.UpdateTime]] = gNowTimeStampFunc()
        gLogger.debug("{}: {}".format(gGetCurrentFunctionName(), lData))
        return self.mColStockInfo.update(lQuery, lData, upsert = True)

    def removeStockInfo(self, iSymbol):
        lQuery = {}
        lQuery[self.mColStockInfoKeys[EnumColStockInfo.Symbol]] = iSymbol
        gLogger.debug("{}: {}".format(gGetCurrentFunctionName(), lQuery))
        return self.mColStockInfo.delete_many(lQuery)

gDatabaseService = CDatabaseService()