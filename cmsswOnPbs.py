#!/usr/bin/env python2.7

###################
#  Datasets       #
###################

import os
import glob
import fileinput
import subprocess
import time
import signal
from core import genericDataset

###################
#  Launch  	  #
###################

def launch(pbsBaseDir,pyJobTemplate,datasets,queueName,numberOfFilesPerJob,outputFolder) :

    ##################
    # Initial checks #
    ##################

    # Check user has a directory in /home-pbs
    if (os.path.isdir("/home-pbs/"+os.getlogin()) == False) :
        print "You don't have a directory in /home-pbs/. Contact a system administrator."
        return

    # Check output folder exists
    if (os.path.isdir(outputFolder) == False) :
        print "Output folder, "+outputFolder+", doesn't exists."
        return

    # Check writing permissions to output folder
    if (os.access(outputFolder, os.W_OK) == False) :
        print "You do not have permissions to write to the output folder, "+outputFolder+"."
        return

    # Check output folder doesn't already contain rootfiles
    if (len(glob.glob(outputFolder+"/*.root")) != 0) :
        print "Output folder, "+outputFolder+", already contains root files."
        print "To make sure this script doesn't erase previous outputs, please move them elsewhere or remove them."
        return

    ##########################################
    # Create working area in /home-pbs/user/ #
    ##########################################

    print "[Main] Creating working area for PBS in /home-pbs/"+os.getlogin()+" ... "

    # If needed, copy the ~/.local folder to /home-pbs/user/ to have rootpy
    if (os.path.isdir("/home-pbs/"+os.getlogin()+"/.local") == False) :
        os.system("cp -r ~/.local /home-pbs/"+os.getlogin()+"/.local")

    # If needed, copy the ~/.local folder to /home-pbs/user/ to have rootpy
    if (os.path.isdir("/home-pbs/"+os.getlogin()+"/.cache/rootpy") == False) :
        os.system("mkdir -p /home-pbs/"+os.getlogin()+"/.cache/rootpy")

    # Copy this PyROOF folder to shared volume
    # (Option L for cp will dereference the symlinks, effectively copying the
    # content pointed by a symlink instead of just copying the link itself)
    timeStamp = time.strftime("%y%m%d_%H%M%S")
    #PBSworkingDir = "/home-pbs/"+os.getlogin()+"/PyROOF_"+timeStamp
    PBSworkingDir = pbsBaseDir+"/PyROOF_"+timeStamp
    os.system("cp -Lr "+os.getcwd()+" "+PBSworkingDir)

    # Copy the grid/dpm proxy to shared volume
    dpmProxy = os.getenv('X509_USER_PROXY')
    if (dpmProxy == None) :
        print "Error : no proxy key found"
        return
    os.system("cp "+dpmProxy+" /home-pbs/"+os.getlogin()+"/.dpmProxy")

    print " "
    print "[Main] Loading datasets ..."
    #for dataset in datasets :
    #    dataset.load(processor.getNumberOfInitialEvents)

    #########################################
    # Creating the processes to be launched #
    #########################################

    shJobTemplate = "core/cmsswOnPbs/job.sh"
    #pyJobTemplate = "core/pbsTemplate/job.py"

    if os.path.exists(outputFolder+"/tmp") :
        os.system("rm -r "+outputFolder+"/tmp/")

    os.mkdir(outputFolder+"/tmp/")

    jobs = {}
    PBSsubprocesses = {}

    print " "
    print "[Main] Creating PBS jobs ..."

    #################################
    # For each file of each dataset #
    #################################

    for (i,dataset) in enumerate(datasets) :

        numberOfJobs = len(dataset.files)/numberOfFilesPerJob
        if (len(dataset.files)%numberOfFilesPerJob) :
            numberOfJobs += 1

        print "[Queuing "+dataset.name+", "+str(numberOfJobs)+" jobs for "+str(len(dataset.files))+" files]"

        # Create a list for each dataset
        PBSsubprocesses[dataset.name]   = []
        jobs[dataset.name] = []

        os.mkdir(outputFolder +"/tmp/"+dataset.name)

        for j in range(numberOfJobs) :
	    print dataset.files[j]
            ############################
            # Create the bash job file #
            ############################

            jobFile          = "PBSjob_" + dataset.name + "_" + str(j) + ".sh"
            jobFile_fullpath = PBSworkingDir + "/" + jobFile
            pyFile_fullpath  = PBSworkingDir + "/" + pyJobTemplate
	    outputFile       = outputFolder+"/tmp/"+dataset.name+"/PBSjob_"+str(j)+".root"

            # Add it to the jobs list
            jobs[dataset.name].append(jobFile)

	    # Copy the config python file to be run and modify it
	    print "cp " + pbsBaseDir + "/" + pyJobTemplate + " " + pyFile_fullpath
	    os.system("cp " + pbsBaseDir + "/" + pyJobTemplate + " " + pyFile_fullpath)
            for line in fileinput.input(pyFile_fullpath, inplace=True):
                line = line.replace('INPUTFILE', dataset.files[j] )
                line = line.rstrip('\n')
		print(line)
		
            os.system("cp " + shJobTemplate + " " + jobFile_fullpath)

            for line in fileinput.input(jobFile_fullpath, inplace=True):
                line = line.replace('LOGFILE', jobFile_fullpath+".log")
                line = line.replace('ERRFILE', jobFile_fullpath+".err")
                line = line.replace('MOVE_TO_WORKING_AREA', 'cd '+PBSworkingDir)
                #line = line.replace('LAUNCH_PYTHON_SCRIPT', 'python '+pyJobTemplate+' '+str(i)+' '+str(j)+' '+str(numberOfFilesPerJob)+' '+outputFile)
                line = line.replace('LAUNCH_PYTHON_SCRIPT', 'cmsRun ' + pyJobTemplate)
                line = line.rstrip('\n')
                print(line)

    #######################
    # Launch all the jobs #
    #######################

    print "[Main] Launching ..."

    # Move to PBS working dir
    os.chdir(PBSworkingDir)

    # Launch each jobs for each dataset,
    # keep track of the corresponding processes
    # to check their status later
    for dataset, jobList in jobs.iteritems() :
        for jobFile in jobList:
            result = subprocess.check_output("qsub -q "+queueName+" "+jobFile, shell=True)
            PBSsubprocesses[dataset].append((result,False))

    #########################
    # Check pbs jobs status #
    #########################

    print "[Main] Jobs launched. Starting jobs monitoring ..."
    print " "

    startTime = time.time()

    from core import pbsMultiprocessing as pbsm 

    try :
        print "there"
	pbsm.monitorPBSJobs(datasets,PBSworkingDir,PBSsubprocesses,outputFolder)
        print "[Main] ---------"
        print "[Main] All done."
        print "[Main] Time elapsed :", time.strftime("%H:%M:%S", time.gmtime(time.time() - startTime))
        print "[Main] Outputs available in", outputFolder
        print "[Main] ---------"
        print "[Main] Don't forget to clean the working area(s), /home-pbs/"+os.getlogin()+"/PyROOF_*"
    except :
        print "[Main] Interruption caught - aborting jobs."
        result = subprocess.check_output("qdel `qstat -u"+os.getlogin()+" | grep "+os.getlogin()+" | cut -d'.' -f1`", shell=True)
        print "[Main] Done."

###########################
# Needed by dataset.load()
##########################
def DummyFunction(file):
	return 1


############
#  Launch  #
############


outputFolder = "/opt/sbg/scratch1/cms/echabert/store/tmp/"
queueName="sbg_local"
numberOfFilesPerJob=5
pbsBaseDir="/home-pbs/echabert/StopProd/CMSSW_7_4_12/src/IPHCFlatTree/FlatTreeProducer/test/"
pyJobTemplate="pbsJobs.py"

Dataset = genericDataset.Dataset
datasets = [
  #Dataset("t2tb_700-250_100", xsection=1  , wildcard="local:/opt/sbg/scratch1/cms/echabert/store/SignalMiniAOD/t2tb_miniAODs/t2tb_700_250_100/")
  #Dataset("t2tb_700-400_100", xsection=1  , wildcard="local:/opt/sbg/scratch1/cms/echabert/store/SignalMiniAOD/t2tb_miniAODs/t2tb_700_400_100/"),
  #Dataset("t2tb_700-550_100", xsection=1  , wildcard="local:/opt/sbg/scratch1/cms/echabert/store/SignalMiniAOD/t2tb_miniAODs/t2tb_700_550_100/"),
  Dataset("t2tb_700-550_100", xsection=1  , wildcard="local:/opt/sbg/scratch1/cms/echabert/store/SignalMiniAOD/t2tb_miniAODs/test/*")
]

#load dataset
for d in datasets:
	print "here:"
	d.load(DummyFunction)
	print len(d.files)
	print d.files


launch(pbsBaseDir,pyJobTemplate,datasets,queueName,numberOfFilesPerJob,outputFolder)



