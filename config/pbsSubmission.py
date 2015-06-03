
import config

# #############
# #  Config   #
# #############

outputFolder = "/opt/sbg/scratch1/cms/echabert/CMSSW_7_3_0/src/store/babyTuples/"

# ##################
# #  Initial call  #
# ##################

from core import pbsSubmission

def main() :
    pbsSubmission.launch(config.processor,
                                config.analyzer,
                                config.datasets,
                                outputFolder)

