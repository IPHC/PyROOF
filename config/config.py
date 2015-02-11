


analysisName = "stopPhys14"
processorName = "kirillFlatTree"



# #####################################################

import sys

analysisModule  = __import__("analysis."+analysisName, fromlist=['Analyzer', 'Datasets'])
processorModule = __import__("processors."+processorName, fromlist=['treeProcess', 'treeProcessWorker'])

datasets = analysisModule.Datasets.datasets
analyzer = analysisModule.Analyzer.Analyzer

processor         = processorModule.treeProcess
processorParallel = processorModule.treeProcessingWorker



