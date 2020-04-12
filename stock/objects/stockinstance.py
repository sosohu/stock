#!/usr/bin/env python
# encoding:utf-8

from stock.common.enum import *
from stock.common.utility import *
from stock.common.base import *
from stock.objects.stockhistory import *
from stock.objects.stockinfo import *

class CStockInstance():
    def __init__(self, iSymbol):
        self.mSymbol = iSymbol
        self.mInfo = None  # CStockInfo
        self.mHistory = {}  # timestamp <->  CStockHistory

    def populateInfo(self, iJson):
        self.mInfo =  CStockInfo(self.mSymbol)
        return self.mInfo.populate(iJson)

    def serializeInfo(self, oJson):
        return self.mInfo.serialize(oJson)

    def populateHistory(self, iJson):
        self.mHistory = {}

        for timestamp, record in iJson.items():
            self.mHistory[timestamp] = CStockHistory(self.mSymbol, timestamp)
            lHr = self.mHistory[timestamp].populate(record)
            if gFaiedFunc(lHr):
                gLogger.warn("Stock {} populate history at timestamp {} failed: result {}".format(self.mSymbol, timestamp, lHr))

        return EnumErrorCode.S_OK

    def serializeHistory(self, oJson):
        oJson = {}

        for timestamp, record in self.mHistory.items():
            lHr = record.serialize(record)
            if gFaiedFunc(lHr):
                gLogger.warn("stock {} serialize failed at timestamp {} failed: result {}".format(self.mSymbol, timestamp, lHr))

        return EnumErrorCode.S_OK
        