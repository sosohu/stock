#!/usr/bin/env python
# encoding:utf-8

import sys

from data.CStockRequestBase import gCreateCookieFunc
from data import CStockRequestInfo

def main():
    gCreateCookieFunc()

    lCStockInfoRequest = CStockRequestInfo(1)
    print lCStockInfoRequest.getResult()
    del lCStockInfoRequest

if __name__ == "__main__":
    main()