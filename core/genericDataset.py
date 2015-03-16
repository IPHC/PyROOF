import glob
import sys, subprocess

#######################################################
class Dataset:

    def __init__(self, name, wildcard = "", xsection = -1) :
        self.name        = name
        self.xsection    = xsection
        self.wildcard    = wildcard
        self.files       = [ ]

    def load(self, methodToGetNumberOfEvent) :

        print "[Loading dataset "+self.name+"]"

        # Getting dataset file list

        if (self.wildcard.startswith("local:")) :
            self.files       = glob.glob(self.wildcard.replace("local:",""))
        elif (self.wildcard.startswith("dpm:")) :

            # Path to use for rfdir (below)
            dpmPath = self.wildcard.replace("dpm:","/dpm/in2p3.fr/home/cms/phedex/store/user/")
            # Path to use for root_open (later)
            xrdPath = self.wildcard.replace("dpm:","root://sbgse1.in2p3.fr//cms/phedex/store/user/")

            cmd = "/usr/bin/rfdir", dpmPath

            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            p.wait()
            (out, err) = p.communicate()
            for line in out.split('\n') :
                fields = line.split()
                if (len(fields) == 9) :
                    self.files.append(xrdPath+"/"+fields[8])

        else :
            print "Wildcard for dataset ", self.name, "doesn't starts with 'local:' or 'dpm:'"
            print "Exiting."
            sys.exit(-1)

        # Check files have been found

        if (len(self.files) == 0) :
            print "Error : no files found when loading dataset "+self.name+"."
            print "Check your input path/wildcard :", self.wildcard
            print "Exiting."
            sys.exit(-1)

        # Get total initial number of event
        self.initialNumberOfEvents = 0
        for file in self.files :
            self.initialNumberOfEvents += int(methodToGetNumberOfEvent(file))

        print "Found", len(self.files), "files,", self.initialNumberOfEvents, "total initial number of events"






