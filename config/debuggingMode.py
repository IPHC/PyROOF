

import config

# ##################
# #  Initial call  #
# ##################

def main() :

    if (len(config.datasets) <= 0) :
        print "Warning : no datasets given"

    # Load only first dataset
    config.datasets[0].load(config.processor.getNumberOfInitialEvents)
    print " "

    # Launch analyzer of first file of first dataset
    config.processor.treeProcess(config.datasets[0].files[0], config.analyzer, "./debuggingOutput.tmp.root", config.datasets[0])
