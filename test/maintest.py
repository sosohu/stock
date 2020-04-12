#!/usr/bin/env python
# encoding:utf-8

from stock.dataservice.source.updateservice import gUpdateService

def main():
    #gUpdateService.updateStocksInfo()
    #gUpdateService.updateStockHistory('SZ000673', 1584633600, 1586361600)
    gUpdateService.updateAllStockHistory()

if __name__ == "__main__":
    main()