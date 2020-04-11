#!/usr/bin/env python
# encoding:utf-8

from stock.common.enum import *
from stock.common.utility import *
from stock.objects.init import *

class CStockInfo():
    def __init__(self, iSymbol):
        self.mSymbol = iSymbol
        
        self.mName = None
        self.mStatus = None
        self.mCreateTime = None
        self.mUpdateTime = None
        return

    def getName(self):
        return self.mName

    def setName(self, iName):
        self.mName = iName

    # Json standard
    __lStockInfoDataList = ['symbol', 'name']

    def populate(self, iJson):
        lHr = self.__ValidateData(iJson)
        if gFaiedFunc(lHr):
            return lHr
            
        self.mName = iJson['name']

    def serialize(self, oJson):
        oJson = {}

        oJson['symbol'] = self.mSymbol
        oJson['name'] = self.mName

    def __ValidateData(self, iJson):
        for lKey in self.__lStockInfoDataList:
            if not iJson[lKey]:
                return EnumErrorCode.E_Validate_His_Fail

        if len(self.__lStockInfoDataList) != len(iJson):
            gLogger.warn("{}: stock info data lenght mismatch".format(gGetCurrentFunctionName()))

        return EnumErrorCode.S_OK
    