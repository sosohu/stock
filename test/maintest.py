#!/usr/bin/env python
# encoding:utf-8

from stock.dataservice.source.updateservice import gUpdateService

def main():
    #gUpdateService.updateStocksInfo()
    gUpdateService.updateStockHistory('SZ002351', 1584633600)

if __name__ == "__main__":
    main()