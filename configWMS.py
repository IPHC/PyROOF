#!/usr/bin/env python

########################
# Input/outputs config #
########################

from tools               import genericDataset
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

#from tools import WMSMultiprocessing

# ...


nWorkers = 2

def main() :

    #processingQueue(processor,analyzer,datasets,nWorkers,outputFolder)
    writeWMSConfig()

def writeWMSConfig() :

    USERNAME=os.getlogin()
    CMSSW_VERSION="5_3_11"
    OUTPUT_DIRECTORY="testWMS"
    SCRAM_ARCH="slc5_amd64_gcc462"
    ANALYSIS_PACKAGE="https://github.com/alexAubin/flatTreeAnalysis"
    OUTPUT_DIRECTORY="/dpm/in2p3.fr/home/cms/phedex/store/user/"+USERNAME+"/"+OUTPUT_DIRECTORY+"/"

    with open("test.txt","w") as f :

        f.write('#!/bin/sh\n')
        f.write('\n')
        f.write('DATASET_NAME=$1\n')
        f.write('INPUT_FILE=$2\n')
        f.write('USERNAME=%s\n' % USERNAME)
        f.write('OUTPUT_DIRECTORY="%s"\n' % OUTPUT_DIRECTORY)
        f.write('CMSSW_VERSION="%s"\n' % CMSSW_VERSION)
        f.write('ANALYSIS_PACKAGE="%s"\n' % ANALYSIS_PACKAGE)
        f.write('export SCRAM_ARCH=%s\n' % SCRAM_ARCH)

        # TODO : dump job template here

        f.close()

main()
