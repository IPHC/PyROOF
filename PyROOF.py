#!/usr/bin/env python2.7

###################
#  Parse options  #
###################

from optparse import OptionParser

parser = OptionParser()

parser.add_option("-d", "--debug", dest="debugMode", default=False,
                          action="store_true", help="Debug mode, meant to check if recent modifications in analysis code didn't break anything.")
parser.add_option("-l", "--local", dest="localMultiprocessingMode", default=False,
                          action="store_true", help="Local multiprocessing mode, run on N workers")
parser.add_option("-b", "--batch", dest="pbsMultiprocessingMode", default=False,
                          action="store_true", help="Batch/PBS multprocessing mode, launch one PBS job for each file to run on.")
parser.add_option("-p", "--prof", dest="profMode", default=False,
                          action="store_true", help="Use cProfile on the Debug mode, meant to check if recent modifications in analysis code didn't break anything.")

(options, args) = parser.parse_args()

############
#  Launch  #
############

from config import config
print " "
print " [Analysis module] ", config.analysisName
print " [Tree processor]  ", config.processorName
print " "

if (options.debugMode) :
    print " Running in debugging mode"
    print " -------------------------"
    print " "
    from config import debuggingMode
    debuggingMode.main()

elif (options.localMultiprocessingMode) :
    print " Running in local multiprocessing mode"
    print " -------------------------------------"
    print " "
    from config import localMultiprocessing
    localMultiprocessing.main()

elif (options.pbsMultiprocessingMode) :
    print " Running in batch/PBS multiprocessing mode"
    print " -----------------"
    print " "
    from config import pbsMultiprocessing
    pbsMultiprocessing.main()

elif (options.profMode) :
    print " Running in debugging mode"
    print " -------------------------"
    print " "
    from config import debuggingMode
    
    # perform profiling
    import cProfile 
    cProfile.run('debuggingMode.main()','fooprof')
    import pstats
    p = pstats.Stats('fooprof')
    print p.sort_stats(-1).print_stats()

else :
    print "No running mode selected, try --help"
