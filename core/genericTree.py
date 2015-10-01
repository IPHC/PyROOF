import ROOT
from rootpy.tree import Tree
from rootpy.io   import root_open

#######################################################

class Reader:

    def loadTree(self,inputFileName,treePath) :

        ROOT.gSystem.Setenv("XNet.UseOldClient","yes")

        # Open file and get tree
        self.theTreeFile = root_open(inputFileName,"READ")
        self.theTree     = self.theTreeFile.Get(treePath)
        
        # Disable all branches
        self.theTree.SetBranchStatus("*",0)
                
    def useBranches(self,branchesToUse) :

        # Enable only branches selected by user
        for branch in branchesToUse :
            self.theTree.SetBranchStatus(branch,1)

    def getTree(self) :
        return self.theTree

#######################################################

class Writer:
    
    def __init__(self,outputFileName,treeName) :

        # Open/recreate output file
        self.theTreeFile = root_open(outputFileName,"RECREATE")

        # Create tree with given name and branches structure
        self.theTree = Tree(treeName)

    def addBranches(self,branches) :
        self.theTree.create_branches(branches)

    def fill(self) :
        self.theTree.fill()

    def writeAndClose(self) :

        # Write the tree to the file
        self.theTree.write()
        self.theTreeFile.close()

    def getTree(self) :
        return self.theTree

#######################################################
