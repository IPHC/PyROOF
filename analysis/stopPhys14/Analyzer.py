
from Selection       import *
from BabyTupleFormat import *

class Analyzer(Selection,BabyTupleFormat) :
   
    # ####################################### #
    # Define branches needed for the analysis #
    # ####################################### #
        
    requiredBranches = BabyTupleFormat.branchesForMiscInfos   \
                     + Selection.branchesForElectronSelection \
                     + Selection.branchesForMuonSelection     \
                     + Selection.branchesForJetSelection      \
                     + Selection.branchesForEventSelection
    
    # ############# #
    # Reset objects #
    # ############# #

    def reset(self) :
        self.resetSelectedObjects()

    ###################################################################################
    #   _____                 _                                       _               #
    #  | ____|_   _____ _ __ | |_   _ __  _ __ ___   ___ ___  ___ ___(_)_ __   __ _   #
    #  |  _| \ \ / / _ \ '_ \| __| | '_ \| '__/ _ \ / __/ _ \/ __/ __| | '_ \ / _` |  #
    #  | |___ \ V /  __/ | | | |_  | |_) | | | (_) | (_|  __/\__ \__ \ | | | | (_| |  #
    #  |_____| \_/ \___|_| |_|\__| | .__/|_|  \___/ \___\___||___/___/_|_| |_|\__, |  #
    #                              |_|                                         |___/  #
    ###################################################################################

    def process(self,event,babyTupleTree) :

        self.reset()

        # Select muons,electrons
        self.muonSelector(event)
        self.electronSelector(event)

        # Sort selected leptons by pT
        self.selectedLeptons = sorted(self.selectedLeptons, key=lambda lepton: lepton.pT, reverse=True)
     
        # Selected jets
        self.jetSelector(event)

        # Sort selected jets by pT
        self.selectedJets = sorted(self.selectedJets, key=lambda jet: jet.pT, reverse=True)

        # Apply event selection
        passEventSelection = self.eventSelector(event)
        if (not passEventSelection) : return False

        # Fill event in babytuple
        self.fill(event,babyTupleTree)
        return True


