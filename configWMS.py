
##########################
# WMS task configuration #
##########################

taskName="wmsTask"
commonPackage="https://github.com/alexAubin/flatTreeAnalysis"

############################
#  Analyzer configuration  #
############################

analysis="stopPhys14"
processor="flatTree"

#from analysis.stopPhys14 import Analyzer
#analyzer = Analyzer.Analyzer

#from flatTreeProcessor import *
#processor = flatTreeProcessingWorker

########################
# Input/outputs config #
########################

from common import genericDataset
Dataset = genericDataset.Dataset
datasets = [  Dataset("ttbar","./store/FlatTrees/ttbar/*.root",xsection=800) ]

##########################

from common import WMStaskCreator

createWMStask = WMStaskCreator.createWMStask

def main() :
    createWMStask(taskName,commonPackage,analysis,processor)
