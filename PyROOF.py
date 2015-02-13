#!/usr/bin/env python2.6

###################
#  Parse options  #
###################

from optparse import OptionParser

parser = OptionParser()

parser.add_option("-d", "--debug", dest="debugMode", default=False,
                          action="store_true", help="Debug mode, meant to check if recent modifications in analysis code didn't break anything.")
parser.add_option("-l", "--local", dest="localMultiprocessingMode", default=False,
                          action="store_true", help="Local multiprocessing mode, run on N workers")
parser.add_option("-w", "--WMStask", dest="wmsTaskCreatorMode", default=False,
                          action="store_true", help="Create a WMS task to run on the cluster. You'll need the proper tool to submit/monitor the task.")
parser.add_option("-j", "--WMSworker", dest="wmsWorkerMode", default=False,
                          action="store_true", help="(Not for user.) To be used by jobs created by a WMS tasks.")

(options, args) = parser.parse_args()

############
#  Launch  #
############

from config import config
print " "
print "Selected analysis  :", config.analysisName
print "Selected processor :", config.processorName
print " "

if (options.debugMode) :
    print "Launching debugging mode"
    print " "
    from config import debuggingMode
    debuggingMode.main()

elif (options.localMultiprocessingMode) :
    print "Launching local multiprocessing mode"
    print " "
    from config import localMultiprocessing
    localMultiprocessing.main()

elif (options.wmsTaskCreatorMode) :
    print "Creating WMS task"
    print " "
    from config import wmsTaskCreator
    wmsTaskCreator()

elif (options.wmsWorkerMode) :
    # TODO
    from config import wmsTaskCreator
    wmsWorker()

else :
    print "No running mode selected, try --help"
