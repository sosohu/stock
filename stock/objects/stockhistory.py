#!/usr/bin/env python
# encoding:utf-8

from stock.common.enum import *
from stock.common.utility import *
from stock.objects.init import *

class CStockHistory():    
    def __init__(self, iSymbol, iTimestamp):
        self.mSymbol = iSymbol
        self.mTimestamp = iTimestamp

        self.mVolume = None
        self.mOpenPrice = None
        self.mHighPrice = None
        self.mLowPrice = None
        self.mClosePrice = None
        self.mChangePrice = None
        self.mChangePercent = None
        self.mTurnoverRate = None
        self.mAmount = None
        self.mPE = None
        self.mPB = None
        self.mPS = None
        self.mPCF = None
        self.mMarketCapital = None
        return

    def getVolume(self):
        return self.mVolume

    def setVolume(self, iVolume):
        self.mVolume = iVolume

    def getOpenPrice(self):
        return self.mOpenPrice

    def setOpenPrice(self, iPrice):
        self.mOpenPrice = iPrice

    def getHighPrice(self):
        return self.mHighPrice

    def setHighPrice(self, iPrice):
        self.mHighPrice = iPrice

    def getLowPrice(self):
        return self.mLowPrice

    def setLowPrice(self, iPrice):
        self.mLowPrice = iPrice

    def getClosePrice(self):
        return self.mClosePrice

    def setClosePrice(self, iPrice):
        self.mClosePrice = iPrice

    def getChangePrice(self):
        return self.mChangePrice

    def setChangePrice(self, iPrice):
        self.mChangePrice = iPrice

    def getChangePercent(self):
        return self.mChangePercent

    def setChangePercent(self, iPercent):
        self.mChangePercent = iPercent

    def getTurnoverRate(self):
        return self.mTurnoverRate

    def setTurnonverRate(self, iTurnoverRate):
        self.mTurnoverRate = iTurnoverRate

    def getAmount(self):
        return self.mAmount

    def setAmount(self, iAmount):
        self.mAmount = iAmount

    def getPE(self):
        return self.mPE

    def setPE(self, iPE):
        self.mPE = iPE

    def getPB(self):
        return self.mPB

    def setPB(self, iPB):
        self.mPB = iPB

    def getPS(self):
        return self.mPS

    def setPS(self, iPS):
        self.mPS = iPS

    def getPCF(self):
        return self.mPCF

    def setPCF(self, iPCF):
        self.mPCF = iPCF

    def getMarketCapital(self):
        return self.mMarketCapital

    def setMarketCapital(self, iMarketCapital):
        self.mMarketCapital = iMarketCapital

    
    # Json standard
    __lStockHistoryDataList = ['volume', 'open', 'high', 'low', 'close', 'chg',\
                    'percent', 'turnoverrate', 'amount', 'pe', 'pb',\
                    'ps', 'pcf', 'market_capital']

    def populate(self, iJson):
        lHr = self.__ValidateData(iJson)
        if gFaiedFunc(lHr):
            return lHr

        self.mVolume = iJson['volume']
        self.mOpenPrice = iJson['open']
        self.mHighPrice = iJson['high']
        self.mLowPrice = iJson['low']
        self.mClosePrice = iJson['close']
        self.mChangePrice = iJson['chg']
        self.mChangePercent = iJson['percent']
        self.mTurnoverRate = iJson['turnoverrate']
        self.mAmount = iJson['amount']
        self.mPE = iJson['pe']
        self.mPB = iJson['pb']
        self.mPS = iJson['ps']
        self.mPCF = iJson['pcf']
        self.mMarketCapital = iJson['market_capital']

    def serialize(self, oJson):
        oJson = {}
        oJson['volume'] = self.mVolume
        oJson['open'] = self.mOpenPrice
        oJson['high'] = self.mHighPrice
        oJson['low'] = self.mLowPrice
        oJson['close'] = self.mClosePrice
        oJson['chg'] = self.mChangePrice
        oJson['percent'] = self.mChangePercent
        oJson['turnoverrate'] = self.mTurnoverRate
        oJson['amount'] = self.mAmount
        oJson['pe'] = self.mPE
        oJson['pb'] = self.mPB
        oJson['ps'] = self.mPS
        oJson['pcf'] = self.mPCF
        oJson['market_capital'] = self.mMarketCapital

    def __ValidateData(self, iJson):
        for lKey in self.__lStockHistoryDataList:
            if not iJson[lKey]:
                return EnumErrorCode.E_Validate_His_Fail

        if len(self.__lStockHistoryDataList) != len(iJson):
            gLogger.warn("{}: stock history data lenght mismatch".format(gGetCurrentFunctionName()))

        return EnumErrorCode.S_OK