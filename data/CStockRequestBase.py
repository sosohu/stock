#!/usr/bin/env python
# encoding:utf-8

from io import BytesIO
import urllib
import pycurl
import uuid
import os
import sys
import json
import time

from DataCommon import gConfigFileWrapper

def gCreateCookieFunc():
    lCookieFile = gConfigFileWrapper.getStr('xue_qiu', 'cookie_file')
    if os.path.exists(lCookieFile):
        lCreateTime = os.path.getctime(lCookieFile)
        if long(time.time()) - lCreateTime < gConfigFileWrapper.getLong('xue_qiu', 'cookie_timeout'):
            return True
        os.remove(lCookieFile)

    lCurl = pycurl.Curl()
    lCurl.setopt(pycurl.VERBOSE, gConfigFileWrapper.getBoolean('curl', 'verbose'))
    lCurl.setopt(pycurl.CONNECTTIMEOUT, gConfigFileWrapper.getInt('curl', 'connect_timeout'))
    lCurl.setopt(pycurl.TIMEOUT, gConfigFileWrapper.getInt('curl', 'timeout'))
    lCurl.setopt(pycurl.USERAGENT, gConfigFileWrapper.getStr('curl', 'user_agent'))
    lCurl.setopt(pycurl.COOKIEJAR, lCookieFile)
    lCurl.setopt(pycurl.URL, gConfigFileWrapper.getStr('xue_qiu', 'home_url'))
    lResponseHeader = BytesIO()
    lResponseData = BytesIO()
    lCurl.setopt(pycurl.WRITEHEADER, lResponseHeader)
    lCurl.setopt(pycurl.WRITEDATA, lResponseData)
    lCurl.perform()
    lCurl.close()

    return os.path.exists(lCookieFile)

# GET
class CStockRequestBase():
    def __init__(self, iName, iUrl, iParams):
        self.__initMember(iName, iUrl, iParams)
        self.__constructCurl()
        self.mCurl.setopt(pycurl.COOKIEFILE, self.mCookieFile)

    def __del__(self):
        self.mCurl.close()

    def __initMember(self, iName, iUrl, iParams):
        self.mName = iName
        #self.mCookieFile  =  "{}-{}-{}.cookie".format(iName, gNowTimeFunc(), uuid.uuid4())
        self.mCookieFile = gConfigFileWrapper.getStr('xue_qiu', 'cookie_file')
        self.mResponseHeader = BytesIO()
        self.mResponseData = BytesIO()
        self.mUrl = iUrl
        self.mParams = iParams

    def __constructCurl(self):
        self.mCurl = pycurl.Curl()
        self.mCurl.setopt(pycurl.VERBOSE, gConfigFileWrapper.getBoolean('curl', 'verbose'))
        self.mCurl.setopt(pycurl.CONNECTTIMEOUT, gConfigFileWrapper.getInt('curl', 'connect_timeout'))
        self.mCurl.setopt(pycurl.TIMEOUT, gConfigFileWrapper.getInt('curl', 'timeout'))
        self.mCurl.setopt(pycurl.USERAGENT, gConfigFileWrapper.getStr('curl', 'user_agent'))
        self.mCurl.setopt(pycurl.WRITEHEADER, self.mResponseHeader)
        self.mCurl.setopt(pycurl.WRITEDATA, self.mResponseData)
        self.mCurl.setopt(pycurl.COOKIEJAR, self.mCookieFile)

    def performRequest(self):
        self.mCurl.setopt(pycurl.URL, self.mUrl + '?' + urllib.urlencode(self.mParams))
        self.mCurl.perform()
        # Get the content stored in the BytesIO object (in byte characters) 
        lResponsebody = self.mResponseData.getvalue()
        # Decode the bytes stored in get_body to HTML and print the result 
        return json.loads(lResponsebody.decode('utf-8'))