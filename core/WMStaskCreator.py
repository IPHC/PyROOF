import os, time

def createWMStask(taskName,corePackage,analysis,processor) :

    userName=os.getlogin()
    folderName = taskName+"_"+time.strftime("%m%d_%H%M")
    DPMoutputDirectory=userName+"/WMStasks/"+folderName+"/"
    DPMoutputDirectoryFull="/dpm/in2p3.fr/home/cms/phedex/store/user/"+DPMoutputDirectory
    
    # Only used To have git and root available
    cmsswVersion="7_0_0"
    scramArch="slc6_amd64_gcc481"

    # Path to rootpy location from workers
    rootpyLocation="/opt/sbg/scratch1/cms/aaubin/lib/"

    print "Creating output directory on DPM in "+DPMoutputDirectory
   
    os.system("/usr/bin/rfmkdir -p "+DPMoutputDirectoryFull)

    print "Creating WMS task", taskName, "in local folder", folderName

    os.mkdir(folderName)  

    with open(folderName+"/workerJob.sh","w") as f :

        f.write('#!/bin/sh\n')
        f.write('\n')
        f.write('DATASET_NAME=$1\n')
        f.write('INPUT_FILE=$2\n')
        f.write('USERNAME='+userName+'\n')
        f.write('OUTPUT_DIRECTORY="'+DPMoutputDirectoryFull+'"\n')
        f.write('CMSSW_VERSION="'+cmsswVersion+'"\n')
        f.write('CORE_PACKAGE="'+corePackage+'"\n')
        f.write('ANALYSIS="'+analysis+'"\n')
        f.write('SCRAM_ARCH="'+scramArch+'"\n')
        f.write('ROOTPY_LOCATION="'+rootpyLocation+'"\n')

        # Dump job template
        with open("core/WMStemplate/workerJob.sh","r") as template :
            for line in template :
                f.write(line)

        f.close()

    jobs = [ ("datasetName","inputFile.root") ]

    os.mkdir(folderName+"/jobs/")
    for (i, job) in enumerate(jobs) :
        with open(folderName+"/jobs/"+str(i)+".jdl","w") as jobConfig :
            with open("core/WMStemplate/workerConfig.jdl","r") as template :
                for line in template :
                    jobConfig.write(line)
            
            (datasetName, inputFile) = job
            jobConfig.write('Arguments = "workerJob.sh '+datasetName+' '+inputFile+'";\n')
