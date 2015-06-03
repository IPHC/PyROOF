import os
import glob
import fileinput
import subprocess
import time

from core import pbsStatus

def launch(processor,Analyzer,datasets,outputFolder) :
 
    template_file = "core/pbsTemplate/pbs_jobs.sh"
    pytemplate_file = "config/singleFileProcessing.py"
    pbs_dir = "/home-pbs/echabert/PyROOF"

    job_list = {} 
    pbs_id = {}

    for dataset in datasets :
        dataset.load(processor.getNumberOfInitialEvents)
    print " "


    ########################################
    # Creating the processes to be launched
    ########################################

    if os.path.exists(outputFolder+"/tmp") :
        os.system("rm -r "+outputFolder+"/tmp/") 
    
    os.mkdir(outputFolder+"/tmp/") 

    print "[Main] Preparing the files ..."
    print " "
    idataset = -1
    for dataset in datasets :

        print "[Main] Queuing", dataset.name, ",",len(dataset.files), " files."
    
        # increment
        idataset+=1

	# create an entry for the dataset in pbs_id
	pbs_id[dataset.name] = []
	job_list[dataset.name] = []

	os.mkdir(outputFolder +"/tmp/"+dataset.name) 
	
	for i in range(len(dataset.files)) :

            fileBaseName = os.path.basename(dataset.files[i])
	    
	    #########################
	    # create the python job #
	    #########################
	    
	    pythonfilename = "pbs_" + dataset.name + "_" + str(i) + ".py"
	    pythonfilename_fullpath = pbs_dir + "/" + pythonfilename
	    os.system("cp " + pytemplate_file + " " + pythonfilename_fullpath)
	    # open the file and add the main command
	    with open(pythonfilename_fullpath, "a") as fpython:
	        fpython.write("main(" + str(idataset) + "," + str(i) + ")" );
	    #os.system("cp " + pythonfilename_fullpath + " .")

	    #############################
	    # create the bash job file  #
	    #############################
	    
	    jobfilename = "pbs_" + dataset.name + "_" + str(i) + ".sh"
	    
	    # add it to the job_list
	    job_list[dataset.name].append(jobfilename)
	    
	    jobfilename_fullpath = pbs_dir + "/" + jobfilename
	    os.system("cp " + template_file + " " + jobfilename_fullpath)
	    #os.system("ls "+pbs_dir)

	    # open the file and modify it
	    #with open(jobfilename_fullpath,"rw") as shfile:
	    #    for line in shfile:
	    #        # modify the line with the main command
	    #        if line.find('LAUNCH_PYTHON_SCRIPT')!= 1:
	    #	        newline = line.replace('LAUNCH_PYTHON_SCRIPT', 'python ' + pythonfilename )
	    
	            # modify the line to copy the output file
	    #        if line.find('COPY_OUTPUT_FILE') != 1:
	    #	        newline = line.replace('COPY_OUTPUT_FILE', 'cp output.root ' + outputFolder + '/tmp/' + dataset.name + "output_" + str(i) + ".root" )



            for line in fileinput.input(jobfilename_fullpath, inplace=True):
                line = line.replace('LAUNCH_PYTHON_SCRIPT', 'python ' + pythonfilename_fullpath)
		line = line.replace('COPY_OUTPUT_FILE', 'cp output.root ' + outputFolder + '/tmp/' + dataset.name + "/output_" + str(i) + ".root")
		line = line.rstrip('\n')
		print(line)

	    
    #####################################
    #  launch all  the jobs             #
    #####################################

    print "[Main] Launching the pbs jobs..."

    #os.system("cd " + pbs_dir)
    os.chdir(pbs_dir)
    #os.system("pwd")
    #os.system("ls")
    for key, value in job_list.iteritems() :
        for i in value:
            #os.system("qsub -q vo.sbg.in2p3.fr " + i)
            result = subprocess.check_output("qsub -q vo.sbg.in2p3.fr " + i, shell=True)
	    pbs_id[key].append((result,False))

    #print pbs_id

    #####################################
    #  Check pbs jobs status            #
    #####################################
    
    allEnded = False
    DatasetRemoved  = {}
    for key, value in job_list.iteritems() :
        DatasetRemoved[key] = False
    while allEnded == False:
	time.sleep(10)
        jobStatus = pbsStatus.pbsStatus(pbs_id)
	for dataset, finished in jobStatus.iteritems():
	    print dataset, finished
	    if finished == True and DatasetRemoved[dataset] == False:
	        allEnded = True
	        print "#### Dataset ", dataset, "is fully processed "
    		for d in datasets :
		    if d.name == dataset:
			noffiles = subprocess.check_output("ls -l " +outputFolder + "/tmp/" + d.name + "/*.root | wc -l", shell=True)
			if len(d.files) != int(noffiles):
			    print "ERROR: the number of files produced does not match: ", noffiles, " / ", len(d.files)
			else: 
        			DatasetRemoved[dataset] = True
				print "[Main] Merging " + dataset
        			os.system("hadd -f "+outputFolder+"/"+dataset+".root "+outputFolder+"/tmp/"+dataset+"/*.root")

    				print "[Main] Removing tmp/*/*.root"
    				for file in glob.glob(outputFolder+"/tmp/*/*.root") :
        				os.remove(file) 
  
            else: 
	        allEnded = False

    #####################################
    #  Merge outputs, delete tmp files  #
    #####################################

    #print "[Main] Starging output merges"

    #for dataset in datasets :
    #    print "[Main] Merging "+dataset.name
    #    os.system("hadd -f "+outputFolder+"/"+dataset.name+".root "+outputFolder+"/tmp/"+dataset.name+"/*.root")

    #print "[Main] Removing tmp/*/*.root"
    #for file in glob.glob(outputFolder+"/tmp/*/*.root") :
    #    os.remove(file) 

    print "[Main] ---------"
    print "[Main] All done."
