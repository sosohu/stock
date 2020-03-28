#!/usr/bin/env python
# encoding:utf-8

from configparser import ConfigParser
from stock.common.utility import *

class CIniFileWrapper():
    def __init__(self, iPath):
        self.mParser = ConfigParser()
        self.mFile = open(iPath)
        self.mParser.read_file(self.mFile)

    def __del__(self):
        self.mFile.close()

    def getInt(self, section, key):
        return int(self.mParser.get(section, key))

    def getLong(self, section, key):
        return long(self.mParser.get(section, key))

    def getBoolean(self, section, key):
        return gStr2BooleanFunc(self.mParser.get(section, key))

    def getStr(self, section, key):
        return self.mParser.get(section, key)