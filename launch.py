#!/usr/bin/env python

#mode="localMultiprocessing"
mode="WMS"

if (mode == "localMultiprocessing") :
    from configLocalMultiprocessing import *
    main()

if (mode == "WMS") :
    from configWMS import *
    main()
