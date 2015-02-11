
import config

# #############
# #  Config   #
# #############

outputFolder = "../store/babyTuples/"

nWorkers = 10

# ##################
# #  Initial call  #
# ##################

from common import localMultiprocessing

def main() :
    localMultiprocessing.launch(config.processorParallel,config.analyzer,config.datasets,nWorkers,outputFolder)

