#!/usr/bin/env python
# encoding:utf-8

from io import BytesIO
import urllib
import pycurl

headers = {}

def display_header(header_line):
    header_line = header_line.decode('iso-8859-1')

    # Ignore all lines without a colon
    if ':' not in header_line:
        return

    # Break the header line into header name and value
    h_name, h_value = header_line.split(':', 1)

    # Remove whitespace that may be present
    h_name = h_name.strip()
    h_value = h_value.strip()
    h_name = h_name.lower() # Convert header names to lowercase
    headers[h_name] = h_value # Header name and value.

def main():
    print("first try to connect without cookie")
    crl = pycurl.Curl()
    crl.setopt(crl.VERBOSE, True)
    crl.setopt(crl.USERAGENT,"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:61.0) Gecko/20100101 Firefox/61.0")
    crl.setopt(crl.URL, "https://xueqiu.com")
    crl.setopt(crl.COOKIEJAR, "cookies_xueqiu_stock_history.txt")
    crl.perform()

    print('**Using PycURL to get stock history**')
    stockHistoryPathUrl = 'https://stock.xueqiu.com/v5/stock/chart/kline.json'
    StockHistoryParams = {}
    StockHistoryParams['symbol'] = 'SH601318'
    StockHistoryParams['begin'] = '1584280231249'
    StockHistoryParams['period'] = 'day'
    StockHistoryParams['type'] = 'before'
    StockHistoryParams['count'] = '-1'
    StockHistoryParams['indicator'] = 'kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance'
    crl.setopt(crl.URL, stockHistoryPathUrl + '?' + urllib.urlencode(StockHistoryParams))
    crl.setopt(crl.HEADERFUNCTION, display_header)
    b_obj = BytesIO()
    crl.setopt(crl.WRITEDATA, b_obj)
    crl.setopt(crl.COOKIEFILE, "cookies_xueqiu_stock_history.txt");
    crl.perform()
    # End curl session
    crl.close()
    print('Header values:-')
    print(headers)
    print('-' * 20)
    # Get the content stored in the BytesIO object (in byte characters) 
    get_body = b_obj.getvalue()
    # Decode the bytes stored in get_body to HTML and print the result 
    print('Output of GET request:\n%s' % get_body.decode('utf8')) 
main()