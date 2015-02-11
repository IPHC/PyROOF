#!/usr/bin/env python2.6

#mode="debugging"
mode="localMultiprocessing"
#mode="wmsTaskCreator"

from config import config, debuggingMode, localMultiprocessing, wmsTaskCreator

if (mode == "debugging") :
    debuggingMode.main()
        
if (mode == "localMultiprocessing") :
    localMultiprocessing.main()

if (mode == "wmsTaskCreator") :
    wmsTaskCreato()

if (mode == "wmsWorker") :
    wmsWorker()
