

import config

# ##################
# #  Initial call  #
# ##################

def main() :

    if (len(config.datasets) <= 0) :
        print "Warning : no datasets given"

    config.processor(config.datasets[0].files[0], config.analyzer, "./debuggingOutput.tmp.root")

