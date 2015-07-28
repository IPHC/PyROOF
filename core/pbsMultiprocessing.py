import os
import glob
import fileinput
import subprocess
import time

def launch(processor,Analyzer,datasets,queueName,outputFolder) :
 
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
        
    # Copy this PyROOF folder to shared volume
    # (Option L for cp will dereference the symlinks, effectively copying the 
    # content pointed by a symlink instead of just copying the link itself)
    timeStamp = time.strftime("%y%m%d_%H%M%S")
    PBSworkingDir = "/home-pbs/"+os.getlogin()+"/PyROOF_"+timeStamp
    os.system("cp -Lr "+os.getcwd()+" "+PBSworkingDir)

    # Copy the grid/dpm proxy to shared volume
    dpmProxy = os.getenv('X509_USER_PROXY')
    if (dpmProxy == None) :
        print "Error : no proxy key found"
        return
    os.system("cp "+dpmProxy+" /home-pbs/"+os.getlogin()+"/.dpmProxy")

    print " "
    print "[Main] Loading datasets ..."
    for dataset in datasets :
        dataset.load(processor.getNumberOfInitialEvents)

    #########################################
    # Creating the processes to be launched #
    #########################################

    shJobTemplate = "core/pbsTemplate/job.sh"
    pyJobTemplate = "core/pbsTemplate/job.py"
    
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

        print "[Queuing "+dataset.name+", "+str(len(dataset.files))+" files]"
        
        # Create a list for each dataset
        PBSsubprocesses[dataset.name]   = []
        jobs[dataset.name] = []

        os.mkdir(outputFolder +"/tmp/"+dataset.name) 
        
        for j in range(len(dataset.files)) :

            ############################
            # Create the bash job file #
            ############################
            
            jobFile          = "PBSjob_" + dataset.name + "_" + str(j) + ".sh"
            jobFile_fullpath = PBSworkingDir + "/" + jobFile
            outputFile         = outputFolder+"/tmp/"+dataset.name+"/PBSjob_"+str(j)+".root"
            
            # Add it to the jobs list
            jobs[dataset.name].append(jobFile)
            
            os.system("cp " + shJobTemplate + " " + jobFile_fullpath)

            for line in fileinput.input(jobFile_fullpath, inplace=True):
                line = line.replace('LOGFILE', jobFile_fullpath+".log")
                line = line.replace('ERRFILE', jobFile_fullpath+".err")
                line = line.replace('MOVE_TO_WORKING_AREA', 'cd '+PBSworkingDir)
                line = line.replace('LAUNCH_PYTHON_SCRIPT', 'python '+pyJobTemplate+' '+str(i)+' '+str(j)+' '+outputFile)
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
    
    datasetsRemaining = len(datasets)
    
    DatasetRemoved  = {}
    for key, value in jobs.iteritems() :
        DatasetRemoved[key] = False

    while (datasetsRemaining > 0) :

        # Wait a few seconds
        time.sleep(30)
        
        # Check & parse job status
        jobStatus = pbsStatus(PBSsubprocesses)

        for dataset, isDone in jobStatus.iteritems():

            if (isDone == False) : continue
            if (DatasetRemoved[dataset] == True) : continue

            print "[Main] Dataset ", dataset, "is fully processed."
            datasetsRemaining -= 1
            
            for d in datasets :
                if d.name == dataset:
                    
                    jobOutputsWildcard = outputFolder + "/tmp/" + d.name + "/*.root";
                    numberOfFilesInOutputFolder = len(glob.glob(jobOutputsWildcard))

                    if (len(d.files) != numberOfFilesInOutputFolder) :
                        print "ERROR : the number of files produced does not match : ", \
                               numberOfFilesInOutputFolder, "found, vs", len(d.files), "expected."
                    else : 
                        #  Merge outputs, remove tmp files
                        DatasetRemoved[dataset] = True
                        print " "
                        print "[Main] Merging " + dataset
                        datasetOutput = outputFolder+"/"+dataset+".root "
                        os.system("hadd -f "+datasetOutput+" "+jobOutputsWildcard)

                        print "[Main] Removing "+jobOutputsWildcard
                        for file in glob.glob(jobOutputsWildcard) :
                            os.remove(file) 
                        print " "
  
    print "[Main] ---------"
    print "[Main] All done."
    print "[Main] Outputs available in", outputFolder
    print "[Main] You may want to clean the working area(s), /home-pbs/"+os.getlogin()+"/PyROOF_*"

def pbsStatus(dataset_idlist):
    
    # Create a summmary of dataset jobs
    dataset_summary = {key:{'RUN':0, 'QUEUED':0, 'HOLD':0, 'ALL':len(value)} for key, value  in dataset_idlist.iteritems()}

    # Call PBS status command
    username = os.getlogin()
    result = subprocess.check_output("qstat -u " + username, shell=True)
    #print result
    
    # Parse results of the command
    lines = result.split('\n')
    for line in lines:
        
        list = line.split()
        if (len(list) != 11) : continue
        
        for dataset, value in dataset_idlist.iteritems():
            for jid in value:
                
                if (jid[0].split('\n')[0] != list[0]) : continue
                
                if list[9] == "R":
                    dataset_summary[dataset]['RUN'] +=1
                if list[9] == "Q":
                    dataset_summary[dataset]['QUEUED'] +=1
                if list[9] == "H":
                    dataset_summary[dataset]['HOLD'] +=1

    # Sum datasets to have a global summary
    allQueued = 0
    allRun    = 0
    allDone   = 0
    allJobs   = 0
    
    # Return a status per dataset (True if all jobs are ended)
    datasetIsDone = {}

    # Prepare summary display
    headers = [ "Dataset", "Submitted", "Running", "Done", "All" ]
    table = []
    for dataset, value in dataset_idlist.iteritems():
        
        summary = dataset_summary[dataset]
        tot     = summary['ALL']
        run     = summary['RUN']
        queued  = summary['QUEUED']
        hold    = summary['HOLD']
        done    = tot - (run + queued + hold)
       
        datasetIsDone[dataset] = (done == tot)
       
        table.append([dataset,queued,run,done,tot])

        # Sum datasets to have a global summary
        allQueued += queued
        allRun    += run
        allDone   += done
        allJobs   += tot
        
    table.append(["All",allQueued,allRun,allDone,allJobs])

    # The actual display (using black magic from stackoverflow)
    print time.strftime("%H:%M:%S")
    print "=============================================================="
    row_format ="{:>12}" * (len(headers))
    print row_format.format(*headers)
    print "--------------------------------------------------------------"
    for row in table:
        print row_format.format(*row)
    print "=============================================================="
    print " "

    return datasetIsDone


