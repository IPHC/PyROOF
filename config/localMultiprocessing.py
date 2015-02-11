
import analysis

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
    localMultiprocessing.launch(processor,analyzer,datasets,nWorkers,outputFolder)

