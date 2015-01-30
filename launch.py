#!/usr/bin/env python

mode="PyROOF"
#mode="WMS"




if (mode == "PyROOF") :
    from configPyROOF import *
    main()

if (mode == "WMS") :
    from configWMS import *
    main()
