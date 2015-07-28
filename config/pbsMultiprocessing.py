
import os
import config

# #############
# #  Config   #
# #############

userName = os.getlogin()
outputFolder = "/opt/sbg/scratch1/cms/"+userName+"/store/babyTuples/"

queue="sbg_local_short"

# ##################
# #  Initial call  #
# ##################

from core import pbsMultiprocessing

def main() :
    pbsMultiprocessing.launch(config.processor,
                              config.analyzer,
                              config.datasets,
                              queue,
                              outputFolder)

