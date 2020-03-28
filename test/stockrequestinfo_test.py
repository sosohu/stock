#!/usr/bin/env python
# encoding:utf-8

import sys

from stock.dataservice.source.stockrequestbase import gCreateCookieFunc
from stock.dataservice.source.stockrequestinfo import CStockRequestInfo

def main():
    gCreateCookieFunc()

    lCStockInfoRequest = CStockRequestInfo(1)
    print lCStockInfoRequest.getResult()
    del lCStockInfoRequest

if __name__ == "__main__":
    main()