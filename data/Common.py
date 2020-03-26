#!/usr/bin/env python
# encoding:utf-8

import time
import inspect

class EnumErrorCode():
    S_OK = 0x0
    E_Database_Error = 0x10000000
    E_Update_Error = 0x20000000

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