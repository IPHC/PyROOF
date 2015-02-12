import glob

#######################################################
class Dataset:

    def __init__(self, name, wildcard, xsection = -1) :
        self.name        = name
        self.files       = glob.glob(wildcard)
        self.xsection    = xsection

    def files(self) :
        return self.files





