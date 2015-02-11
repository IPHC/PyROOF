

import config

# ##################
# #  Initial call  #
# ##################

def main() :
    config.processor(config.datasets[0].files[0], config.analyzer, "./debuggingOutput.tmp.root")

