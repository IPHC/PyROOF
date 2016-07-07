
import os
import config

# #############
# #  Config   #
# #############

userName = os.getlogin()
outputFolder = "/opt/sbg/scratch1/cms/"+userName+"/store/tmp/"

#queue="sbg_local"
#queue="sbg_local_short"
#queue="cms_local_short"
#queue="cms_local"
queue="cms_local_mdm"

filesPerJobs=1

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

