#!/usr/bin/env python
# encoding:utf-8

import sys

from stock.dataservice.source.stockrequestbase import gCreateCookieFunc
from stock.dataservice.source.stockrequesthistory import CStockRequestHistory

def main():
    gCreateCookieFunc()

    lCStockInfoRequest = CStockRequestHistory('SH601318', 1584280231249, 1)
    lHr = lCStockInfoRequest.getResult()
    del lCStockInfoRequest

if __name__ == "__main__":
    main()