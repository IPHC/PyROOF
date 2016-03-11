import glob
import sys, subprocess
import fnmatch

#######################################################
class Dataset:

    def __init__(self, name, wildcard = "", file = "", min = 0, max = 0, xsection = -1) :
        self.name        = name
        self.xsection    = xsection
        self.wildcard    = wildcard
        self.min         = min
        self.max         = max
        self.file        = file
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
            # xrdPath = self.wildcard.replace("dpm:","root://sbgse1.in2p3.fr//cms/phedex/store/user/")
            xrdPath = self.wildcard.replace("dpm:","root://sbgse1.in2p3.fr//cms/phedex/store/user/")

            cmd = "/usr/bin/rfdir", dpmPath

            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            p.wait()
            (out, err) = p.communicate()
            for line in out.split('\n') :
                fields = line.split()
                if (len(fields) == 9) :
                    fileName = fields[8];
                    if (fileName == "failed") : continue
                    self.files.append(xrdPath+"/"+fileName)

        #specify interval of output files you want to read
        # @MJ@ TODO generalize the names of files to read
        # @MJ@ FIXME This is not really nice way how to do things, beacuse this acesses DPM too much often
        # but useful if number of files in folder reaches some threshold
        elif (self.wildcard.startswith("dpm2:")) :

            # Path to use for rfdir (below)
            dpmPathIn = self.wildcard.replace("dpm2:","/dpm/in2p3.fr/home/cms/phedex/store/user/")

            for n in range(self.min, self.max+1) :
                nameStr = "output_"+str(n)+".root"
                dpmPath = dpmPathIn
                dpmPath += "/output_"+str(n)+".root"
                cmd = "/usr/bin/rfdir", dpmPath
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                p.wait()
                (out, err) = p.communicate()
                for line in out.split('\n') :
                    fields = line.split()
                    if (len(fields) == 9) :
                        fileName = fields[8];
                        if ("failed" in fileName) : continue
                        if (fnmatch.fnmatch(fileName, dpmPath)):
                            xrdPath = fileName.replace("/dpm/in2p3.fr/home/cms/phedex/store/","root://sbgse1.in2p3.fr//cms/phedex/store/")
                            self.files.append(xrdPath)

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


