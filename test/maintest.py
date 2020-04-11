#!/usr/bin/env python
# encoding:utf-8

from stock.dataservice.source.updateservice import gUpdateService

def main():
    #gUpdateService.updateStocksInfo()
    #gUpdateService.updateStockHistory('SZ000673', 1584633600)
    gUpdateService.updateAllStockHistory(1584633600)

if __name__ == "__main__":
    main()