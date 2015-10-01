
import os
import config

# #############
# #  Config   #
# #############

userName = os.getlogin()
outputFolder = "/opt/sbg/scratch1/cms/"+userName+"/store/tmp/"

queue="sbg_local"
filesPerJobs=5

# ##################
# #  Initial call  #
# ##################

from core import pbsMultiprocessing

def main() :
    pbsMultiprocessing.launch(config.processor,
                              config.analyzer,
                              config.datasets,
                              queue,
                              filesPerJobs,
                              outputFolder)

