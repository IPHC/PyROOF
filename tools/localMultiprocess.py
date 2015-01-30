
from os.path             import basename
from multiprocessing     import Queue, Process

def processingQueue(processor,Analyzer,datasets,nWorkers,outputFolder) :

    ##################
    # Initiate queue #
    ##################

    queue = Queue()

    ##########################
    # Create pool of workers #
    ##########################

    print "Creating pool of", nWorkers, "workers"
    workers = []
    for i in range(nWorkers) :
        w = Process(target=processor,args=((queue),))
        w.daemon = True
        w.start()
        workers.append(w)

    ########################################
    # Populate queue with todo information #
    ########################################

    print "Filling queue..."
    for dataset in datasets :

        print "Queuing", dataset.name, ",",len(dataset.files), " files."

        for i in range(len(dataset.files)) :

            fileBaseName = basename(dataset.files[i])

            queue.put((dataset, i, Analyzer, outputFolder+"/"+fileBaseName))

    #####################################
    #  Wait for workers to do the jobs  #
    #####################################

    print "Waiting for workers."

    for i in range(nWorkers) :
        queue.put("DONE")

    # TODO/FIXME add display of status of jobs

    for worker in workers :
        worker.join()
        if (worker.exitcode != 0) :
            print "(WARNING!) A worker returned exit code", worker.exitcode

    print "---------"
    print "All done."
