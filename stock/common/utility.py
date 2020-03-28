#!/usr/bin/env python
# encoding:utf-8

import time
import inspect
from stock.common.enum import *

def gNowTimeFunc():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

def gStr2BooleanFunc(iStr):
    return iStr.lower() in ['true', '1', 'yes']

def gNowTimeStampFunc():
    return long(time.time())

def gFaiedFunc(iCode):
    return iCode != EnumErrorCode.S_OK

def gGetCurrentFunctionName():
    return inspect.stack()[1][3]