#!/usr/bin/env python
# encoding:utf-8

import logging
from stock.common.configwrapper import CIniFileWrapper

gConfigFileWrapper = CIniFileWrapper('conf/config.ini')

gLogger = logging.getLogger()
gLogFile = logging.FileHandler(gConfigFileWrapper.getStr('log', 'objects_file'),encoding='utf-8')
gLogFormatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
gLogFile.setFormatter(gLogFormatter) 
gLogger.addHandler(gLogFile)
gLogger.setLevel(gConfigFileWrapper.getInt('log', 'objects_level'))