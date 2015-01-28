#!/usr/bin/env python


from tools               import genericDataset
from analysis.stopPhys14 import Analyzer
from rootpy              import log
from os.path             import basename
from flatTreeProcessor   import *
from multiprocessing     import Queue, Process

genericTreeWriter = genericTree.Writer
genericTreeReader = genericTree.Reader
genericDataset    = genericDataset.Dataset

log["/ROOT.TClassTable.Add"].setLevel(log.ERROR)

###################
# Create datasets # 
###################

datasets = [  genericDataset("ttbar","./store/FlatTrees/ttbar/*.root",800) ]

outputFolder = "./store/babyTuples/ttbar/"

nWorkers = 3


# Initiate queue
queue = Queue()

# Create pool of workers process
print "Creating pool of", nWorkers, "workers"
workers = []
for i in range(nWorkers) :
    w = Process(target=flatTreeProcessingWorker,args=((queue),))
    w.daemon = True
    w.start()
    workers.append(w)

# Populate queue with todo information
print "Filling queue..."
for dataset in datasets :

    print "Queuing", dataset.name, ",",len(dataset.files), " files."

    for file in dataset.files :

        fileBaseName = basename(file)

        queue.put((dataset, file, Analyzer.Analyzer, outputFolder+"/"+fileBaseName))

print "Done. Waiting for workers."

for i in range(nWorkers) :
    queue.put("DONE")

for worker in workers :
    worker.join()

print "All done."
