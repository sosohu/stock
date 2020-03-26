#!/usr/bin/env python
# encoding:utf-8

from pymongo import MongoClient

from CStockRequestBase import gCreateCookieFunc
from DataCommon import *
from CStockRequestInfo import *
from CDatabaseService import *

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
                lResultCursor = gDatabaseService.getStockInfo(lItem['symbol'])
                lResultList = list(lResultCursor)
                if len(lResultList) > 1:
                    gLogger.warning("{}: {} has {} records".format(gGetCurrentFunctionName(), lItem['symbol'], len(lResultList)))
                    continue
                elif len(lResultList) == 1:
                    if lResultList[0]['name'] == lItem['name']:
                        gLogger.debug("{}: {} no change, do nothing".format(gGetCurrentFunctionName(), lItem['symbol']))
                        continue
                    
                    gDatabaseService.updateStockInfo(lItem['symbol'], lItem['name'], 1, lResultList[0]['create_time'])
                    gLogger.debug("{}: {} update success".format(gGetCurrentFunctionName(), lItem['symbol']))
                else:              
                    gDatabaseService.updateStockInfo(lItem['symbol'], lItem['name'], 1, gNowTimeStampFunc())
                    gLogger.debug("{}: {} insert success".format(gGetCurrentFunctionName(), lItem['symbol']))
            del lCStockInfoRequest

gUpdateService = CUpdateService()