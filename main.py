#!/usr/bin/env python

from tools               import genericDataset
from analysis.stopPhys14 import Analyzer
from flatTreeProcessor   import *
from processingQueue     import *

genericDataset = genericDataset.Dataset


##########
# Config #
##########

datasets = [  genericDataset("ttbar","./store/FlatTrees/ttbar/*.root",800) ]

outputFolder = "./store/babyTuples/ttbar/"

nWorkers = 2

processor = flatTreeProcessingWorker
analyzer = Analyzer.Analyzer

###########
# Process #
###########

processingQueue(processor,analyzer,datasets,nWorkers,outputFolder)

