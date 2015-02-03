from rootpy import log
from common import genericTree
import os, sys, time

log["/ROOT.TClassTable.Add"].setLevel(log.ERROR)

genericTreeWriter = genericTree.Writer
genericTreeReader = genericTree.Reader

def flatTreeProcess(inputFile, Analyzer, outputFile) :

    ###################
    # Create analyzer #
    ###################

    print "Creating analyzer"
    analyzer = Analyzer()
    analyzerRequiredInputBranches = analyzer.requiredBranches
    analyzerBabyTupleFormat       = analyzer.babyTupleFormat

    #################
    # Open FlatTree #
    #################

    print "Opening input tree (", inputFile, ")"
    flatTreeReader = genericTree.Reader()
    flatTreeReader.loadTree(inputFile,"FlatTree/tree")
    flatTreeReader.useBranches(analyzerRequiredInputBranches)

    #########################
    # Create babyTuple tree #
    #########################

    print "Creating output babytuple (", outputFile, ")"
    babyTuple = genericTree.Writer(outputFile,"babyTuple")
    babyTuple.addBranches(analyzerBabyTupleFormat)

    ######################
    # Setup progress bar #
    ######################

    print "Starting loop"
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
       
        # Update progress bar #
        i += 1
        if (i % (nEntries/progressBarWidth) == 0) : 
            sys.stdout.write("-")
            sys.stdout.flush()
        
        # Reset branches values to default #
        babyTuple.getTree().reset_branch_values()

        # Call analysis-specific process function #
        fillEvent = analyzer.process(event,babyTuple.getTree())

        # If event should be filled, fill it #
        if (fillEvent) : babyTuple.fill()

    #############################
    # Write and close babytuple #
    #############################

    babyTuple.writeAndClose()

    sys.stdout.write("\n")
    sys.stdout.flush()

def flatTreeProcessingWorker(id, queue) :

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
        flatTreeProcess(dataset.files[i], Analyzer, outputFile)

        # Restore old stdout/stderr
        sys.stdout = oldStdout
        sys.stderr = oldStderr


