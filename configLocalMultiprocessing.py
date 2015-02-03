
########################
# Input/outputs config #
########################

from analysis.stopPhys14 import Datasets
datasets = Datasets.datasets

outputFolder = "./store/babyTuples/"

############################
#  Analyzer configuration  #
############################

from analysis.stopPhys14 import Analyzer
analyzer = Analyzer.Analyzer

from flatTreeProcessor import *
processor = flatTreeProcessingWorker

#########################
# Parallelization stuff #
#########################

from common import localMultiprocessing
launch = localMultiprocessing.launch

nWorkers = 10

def main() :

    launch(processor,analyzer,datasets,nWorkers,outputFolder)

