
import config

# #############
# #  Config   #
# #############

outputFolder = "../store/babyTuples/"

nWorkers = 10

# ##################
# #  Initial call  #
# ##################

from core import localMultiprocessing

def main() :
    localMultiprocessing.launch(config.processor,
                                config.analyzer,
                                config.datasets,
                                nWorkers,
                                outputFolder)

