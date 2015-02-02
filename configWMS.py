#!/usr/bin/env python2.6

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

#from common import WMSMultiprocessing

# ...


nWorkers = 2

def main() :

    #processingQueue(processor,analyzer,datasets,nWorkers,outputFolder)
    writeWMSConfig()

import os, time

def writeWMSConfig(taskName = "wmsTask") :

    folderName = taskName+"_"+time.strftime("%m%d_%H%M")

    print "Creating WMS task", taskName, "in folder", folderName

    os.mkdir(folderName)  

    USERNAME=os.getlogin()
    CMSSW_VERSION="5_3_11"
    OUTPUT_DIRECTORY="testWMS"
    SCRAM_ARCH="slc5_amd64_gcc462"
    ANALYSIS_PACKAGE="https://github.com/alexAubin/flatTreeAnalysis"
    OUTPUT_DIRECTORY="/dpm/in2p3.fr/home/cms/phedex/store/user/"+USERNAME+"/"+OUTPUT_DIRECTORY+"/"

    with open(folderName+"/workerJob.sh","w") as f :

        f.write('#!/bin/sh\n')
        f.write('\n')
        f.write('DATASET_NAME=$1\n')
        f.write('INPUT_FILE=$2\n')
        f.write('USERNAME='+USERNAME+'\n')
        f.write('OUTPUT_DIRECTORY="'+OUTPUT_DIRECTORY+'"\n')
        f.write('CMSSW_VERSION="'+CMSSW_VERSION+'"\n')
        f.write('ANALYSIS_PACKAGE="'+ANALYSIS_PACKAGE+'"\n')
        f.write('export SCRAM_ARCH="'+SCRAM_ARCH+'"\n')

        # Dump job template
        with open("common/WMStemplate/workerJob.sh","r") as template :
            for line in template :
                f.write(line)

        f.close()

    jobs = [ ("datasetName","inputFile.root") ]

    os.mkdir(folderName+"/jobs/")
    for (i, job) in enumerate(jobs) :
        with open(folderName+"/jobs/"+str(i)+".jdl","w") as jobConfig :
            with open("common/WMStemplate/workerConfig.jdl","r") as template :
                for line in template :
                    jobConfig.write(line)
            
            (datasetName, inputFile) = job
            jobConfig.write('Arguments = "'+datasetName+' '+inputFile+'";\n')

main()
