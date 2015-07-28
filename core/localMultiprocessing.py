
import os
import glob
from multiprocessing     import Queue, Process

def launch(processor,Analyzer,datasets,nWorkers,outputFolder) :

    ##################
    # Initial checks #
    ##################
    
    # Check output folder exists
    if (os.path.isdir(outputFolder) == False) :
        print "Output folder, "+outputFolder+", doesn't exists."
        return

    # Check output folder doesn't contain rootfiles already
    if (len(glob.glob(outputFolder+"/*.root")) != 0) :
        print "Output folder, "+outputFolder+", already contains root files."
        print "To make sure this script doesn't erase previous outputs, please move them elsewhere or remove them."
        return
   
    # Check writing permissions to output folder
    if (os.access(outputFolder, os.W_OK) == False) :
        print "You do not have permissions to write to the output folder, "+outputFolder+"."
        return

    #################
    # Load datasets #
    #################

    for dataset in datasets :
        dataset.load(processor.getNumberOfInitialEvents)
    print " "

    ##################
    # Initiate queue #
    ##################

    queue = Queue()

    ##########################
    # Create pool of workers #
    ##########################

    print "[Main] Creating pool of", nWorkers, "workers"
    workers = []
    for id in range(nWorkers) :
        w = Process(target=processor.treeProcessingWorker,args=(id,queue))
        w.daemon = True
        w.start()
        workers.append(w)

    ########################################
    # Populate queue with todo information #
    ########################################

    if os.path.exists(outputFolder+"/tmp") :
        os.system("rm -r "+outputFolder+"/tmp/") 
    
    os.mkdir(outputFolder+"/tmp/") 

    print "[Main] Filling queue..."
    print " "
    for dataset in datasets :

        print "[Main] Queuing", dataset.name, ",",len(dataset.files), " files."

        os.mkdir(outputFolder+"/tmp/"+dataset.name) 

        for i in range(len(dataset.files)) :

            fileBaseName = os.path.basename(dataset.files[i])

            queue.put((dataset, i, Analyzer, outputFolder+"/tmp/"+dataset.name+"/"+fileBaseName))

    #####################################
    #  Wait for workers to do the jobs  #
    #####################################

    print "[Main] Waiting for workers..."

    for i in range(nWorkers) :
        queue.put("DONE")

    for worker in workers :
        worker.join()
        if (worker.exitcode != 0) :
            print "[Main] (WARNING!) A worker returned exit code", worker.exitcode

    #####################################
    #  Merge outputs, delete tmp files  #
    #####################################

    print "[Main] Starging output merges"

    for dataset in datasets :
        print "[Main] Merging "+dataset.name
        os.system("hadd -f "+outputFolder+"/"+dataset.name+".root "+outputFolder+"/tmp/"+dataset.name+"/*.root")

    print "[Main] Removing tmp/*/*.root"
    for file in glob.glob(outputFolder+"/tmp/*/*.root") :
        os.remove(file) 

    print "[Main] ---------"
    print "[Main] All done."
