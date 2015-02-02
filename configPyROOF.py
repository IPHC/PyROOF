
########################
# Input/outputs config #
########################

from common import genericDataset
Dataset = genericDataset.Dataset
datasets = [  Dataset("ttbar","./store/FlatTrees/ttbar/*.root",xsection=800) ]

outputFolder = "./store/babyTuples/ttbar/"

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
processingQueue = localMultiprocessing.processingQueue

nWorkers = 2

def main() :

    processingQueue(processor,analyzer,datasets,nWorkers,outputFolder)

