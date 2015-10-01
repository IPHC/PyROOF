import sys
from config import config

# ##################
# #  Initial call  #
# ##################

def main(datasetIndex, jobIndex, numberOfFilesPerJob, outputFile) :

    # Load dataset no = datasetIndex
    
    if (datasetIndex >= len(config.datasets) ) :
        print "This dataset does not exist (no = ", datasetIndex, ")"
        return

    config.datasets[datasetIndex].load(config.processor.getNumberOfInitialEvents)

    # Process files

    fileIndexBegin = jobIndex * numberOfFilesPerJob
    fileIndexEnd   = fileIndexBegin + numberOfFilesPerJob
    if (fileIndexEnd > len(config.datasets[datasetIndex].files)) :
        fileIndexEnd = len(config.datasets[datasetIndex].files)

    for fileIndex in range(fileIndexBegin,fileIndexEnd) :
        outputFile_ = outputFile[:-5]+"_"+str(fileIndex)+".root"
        config.processor.treeProcess(config.datasets[datasetIndex].files[fileIndex], config.analyzer, outputFile_, config.datasets[datasetIndex])

main(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),sys.argv[4])
