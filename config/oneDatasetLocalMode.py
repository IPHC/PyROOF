

import config
from core import genericDataset

# ##################
# #  Initial call  #
# ##################

def main(datasetname, filename) :

    dataset =  genericDataset.Dataset(datasetname, "local:"+filename)
    #if (len(config.datasets) <= 0) :
    #    print "Warning : no datasets given"

    # Load only first dataset
    dataset.load(config.processor.getNumberOfInitialEvents)
    #print " "

    # Launch analyzer of first file of first dataset
    #config.dataset[0] = genericDataset.Dataset(datasetname, "local:"+filename)
    config.processor.treeProcess(dataset.files[0], config.analyzer, datasetname+"..root", dataset)
