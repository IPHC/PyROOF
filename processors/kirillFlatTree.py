from rootpy import log
from core   import genericTree
import os, sys, time
from rootpy.io   import root_open

log["/ROOT.TClassTable.Add"].setLevel(log.ERROR)
log["/ROOT.TGClient.TGClient"].setLevel(log.ERROR)
log["/rootpy"].setLevel(log.ERROR)

genericTreeWriter = genericTree.Writer
genericTreeReader = genericTree.Reader

def treeProcess(inputFile, Analyzer, outputFile, dataset) :

    ###################
    # Create analyzer #
    ###################

    print "> Creating analyzer"
    analyzer = Analyzer(dataset)
    analyzerRequiredInputBranches = analyzer.requiredBranches
    analyzerBabyTupleFormat       = analyzer.babyTupleFormat

    #################
    # Open FlatTree #
    #################

    print "> Opening input tree ("+inputFile+")"
    flatTreeReader = genericTree.Reader()
    flatTreeReader.loadTree(inputFile,"FlatTree/tree")
    flatTreeReader.useBranches(analyzerRequiredInputBranches)

    #########################
    # Create babyTuple tree #
    #########################

    print "> Creating output babytuple ("+outputFile+")"
    babyTuple = genericTree.Writer(outputFile,"babyTuple")
    babyTuple.addBranches(analyzerBabyTupleFormat)

    ######################
    # Setup progress bar #
    ######################

    print "> Starting loop"
    progressBarWidth = 50
    sys.stdout.write("[%s]" % (" " * progressBarWidth))
    sys.stdout.flush()
    sys.stdout.write("\b" * (progressBarWidth+1))

    ##################
    # Loop on events #
    ##################

    i = 0
    nEntries = flatTreeReader.getTree().GetEntries()
    for event in flatTreeReader.getTree() :
    	#if(i>2000): break  
        # Update progress bar #
        i += 1
        if (i % (nEntries/progressBarWidth) == 0) : 
            sys.stdout.write("-")
            sys.stdout.flush()
        
        # Reset branches values to default #
        babyTuple.getTree().reset_branch_values()

        # Call analysis-specific process function #
        #fillEvent = analyzer.process(event,babyTuple.getTree(),True)
        fillEvent = analyzer.process(event,babyTuple.getTree())

        # If event should be filled, fill it #
        if (fillEvent) : babyTuple.fill()

    #############################
    # Write and close babytuple #
    #############################

    sys.stdout.write("\n")
    sys.stdout.flush()

    # write histogram containing the sum of input event weights
    analyzer.hWeights.Write()
    analyzer.hWeightsPlus.Write()
    analyzer.hWeightsMinus.Write()
    analyzer.hStopNeutralino.Write()

    print "> Writing and closing output tree."
    babyTuple.writeAndClose()
    print "> Done."


def treeProcessingWorker(id, queue) :

    # For ever
    while True :

        # Grab task from queue
        task = queue.get()

        # If task is a done signal, break from loop
        if (task == "DONE") : break

        # Else, parse arguments
        (dataset, i, Analyzer, outputFile) = task
        
        print "[Worker "+str(id+1)+"] Starting task for dataset", dataset.name, "- file "+str(i+1)+"/"+str(len(dataset.files))

        # Redirect stdout and stderr to log file
        (outputPath, outputExt) = os.path.splitext(outputFile)
        logFileName = outputPath+".log"
        oldStdout = sys.stdout
        oldStderr = sys.stderr
        sys.stdout = open(logFileName,"w")
        sys.stderr = open(logFileName,"w")

        # Launch processing function
        treeProcess(dataset.files[i], Analyzer, outputFile, dataset)

        # Restore old stdout/stderr
        sys.stdout = oldStdout
        sys.stderr = oldStderr


def getNumberOfInitialEvents(inputFileName) :

    # Open file and get number of entries in hcount
    theFile = root_open(inputFileName,"READ")
    theCountHisto = theFile.Get("FlatTree/hcount")
    count = theCountHisto.GetEntries();
    theFile.Close()
    return count;

