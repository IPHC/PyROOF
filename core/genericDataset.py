import glob
import sys, subprocess

#######################################################
class Dataset:

    def __init__(self, name, wildcard, xsection = -1) :
        self.name        = name
        self.xsection    = xsection
        self.files       = [ ]

        print "Listing files for dataset", self.name, "..."

        # Getting dataset file list

        if (wildcard.startswith("local:")) :
            self.files       = glob.glob(wildcard.replace("local:",""))
        elif (wildcard.startswith("dpm:")) :

            # Path to use for rfdir (below)
            dpmPath = wildcard.replace("dpm:","/dpm/in2p3.fr/home/cms/phedex/store/user/")
            # Path to use for root_open (later)
            xrdPath = wildcard.replace("dpm:","root://sbgse1.in2p3.fr//cms/phedex/store/user/")

            cmd = "/usr/bin/rfdir", dpmPath

            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            p.wait()
            (out, err) = p.communicate()
            for line in out.split('\n') :
                fields = line.split()
                if (len(fields) == 9) :
                    self.files.append(xrdPath+fields[8])

        else :
            print "Wildcard for dataset ", self.name, "doesn't starts with '/' or 'root://'"

        # Check files have been found

        if (len(self.files) == 0) :
            print "Error : found 0 files when initializing dataset "+self.name+"."
            print "Exiting."
            sys.exit(-1)

    def files(self) :
        return self.files





