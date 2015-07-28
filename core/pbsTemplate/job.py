import sys
from config import config

# ##################
# #  Initial call  #
# ##################

def main(datasetIndex, fileIndex, outputFile) :

    # Load dataset no = datasetIndex
    
    if (datasetIndex >= len(config.datasets) ) :
        print "This dataset does not exist (no = ", datasetIndex, ")"
        return

    config.datasets[datasetIndex].load(config.processor.getNumberOfInitialEvents)

    # Process file no = fileIndex
    
    if (fileIndex >= len(config.datasets[datasetIndex].files)):
        print "This file does not exist (no = ", fileIndex, ")"

    config.processor.treeProcess(config.datasets[datasetIndex].files[fileIndex], config.analyzer, outputFile, config.datasets[datasetIndex])

main(int(sys.argv[1]),int(sys.argv[2]),sys.argv[3])
