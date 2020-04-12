#!/usr/bin/env python
# encoding:utf-8

from stock.common.enum import *
from stock.common.utility import *
from stock.common.base import *

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
    __lStockHistoryDataList = ['timestamp', 'volume', 'open', 'high', 'low', 'close', 'chg',\
                    'percent', 'turnoverrate', 'amount', 'pe', 'pb',\
                    'ps', 'pcf', 'market_capital']

    def populate(self, iJson):
        lHr = self.__ValidateData(iJson)
        if gFaiedFunc(lHr):
            return lHr

        self.mVolume = iJson['volume'] or -1
        self.mOpenPrice = iJson['open'] or -1
        self.mHighPrice = iJson['high'] or -1
        self.mLowPrice = iJson['low'] or -1
        self.mClosePrice = iJson['close'] or -1
        self.mChangePrice = iJson['chg'] or -1
        self.mChangePercent = iJson['percent'] or -1
        self.mTurnoverRate = iJson['turnoverrate'] or -1
        self.mAmount = iJson['amount'] or -1
        self.mPE = iJson['pe'] or -1
        self.mPB = iJson['pb'] or -1
        self.mPS = iJson['ps'] or -1
        self.mPCF = iJson['pcf'] or -1
        self.mMarketCapital = iJson['market_capital'] or -1

        return EnumErrorCode.S_OK

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

        return EnumErrorCode.S_OK

    def __ValidateData(self, iJson):
        for lKey in self.__lStockHistoryDataList:
            if iJson[lKey] is None:
                gLogger.warn("Stock {} at timestamp {}: stock history expect key {} not exist".format(self.mSymbol, self.mTimestamp, lKey))

        if len(self.__lStockHistoryDataList) != len(iJson):
            gLogger.warn("Stock {} at timestamp {}: stock history data length mismatch".format(self.mSymbol, self.mTimestamp))

        return EnumErrorCode.S_OK