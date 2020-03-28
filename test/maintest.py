#!/usr/bin/env python
# encoding:utf-8

from stock.dataservice.source.updateservice import gUpdateService

def main():
    gUpdateService.updateStocksInfo()

if __name__ == "__main__":
    main()