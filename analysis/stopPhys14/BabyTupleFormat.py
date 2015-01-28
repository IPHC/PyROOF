
from math        import sqrt, cos
 
###########################################################################################
#   ____        _           _               _         __                            _     #
#  | __ )  __ _| |__  _   _| |_ _   _ _ __ | | ___   / _| ___  _ __ _ __ ___   __ _| |_   #
#  |  _ \ / _` | '_ \| | | | __| | | | '_ \| |/ _ \ | |_ / _ \| '__| '_ ` _ \ / _` | __|  #
#  | |_) | (_| | |_) | |_| | |_| |_| | |_) | |  __/ |  _| (_) | |  | | | | | | (_| | |_   #
#  |____/ \__,_|_.__/ \__, |\__|\__,_| .__/|_|\___| |_|  \___/|_|  |_| |_| |_|\__,_|\__|  #
#                      |___/          |_|                                                 #
###########################################################################################

class BabyTupleFormat :
       
    babyTupleFormat = { 

      'eventId'                 :  'I',

      'numberOfSelectedLeptons' :  'I',
      
      'leadingLeptonId'         :  'I',
      'leadingLeptonPt'         :  'F',
      'leadingLeptonPhi'        :  'F',
      'leadingLeptonEta'        :  'F',
      'leadingLeptonIso'        :  'F',
      
      'secondLeptonId'          :  'I',
      'secondLeptonPt'          :  'F',
      'secondLeptonPhi'         :  'F',
      'secondLeptonEta'         :  'F',
      'secondLeptonIso'         :  'F',

      'numberOfSelectedJets'    :  'I',
      'numberOfBTaggedJets'     :  'I',
      'jetsPt'                  :  'F[6]',
      'jetsPhi'                 :  'F[6]',
      'jetsEta'                 :  'F[6]',
      'jetsCSV'                 :  'F[6]',
      'jetsCSVv2'               :  'F[6]',
      'jetsPUid'                :  'F[6]',

      'MET'                     :  'F',
      'METPhi'                  :  'F',
      'MT'                      :  'F'    
    }

    # Additional input branches needed during the filling of the babytuple
    branchesForMiscInfos = [ "ev_id", "met_pt", "met_phi" ]

    def fill(self,event,babyTupleTree) :

        babyTupleTree.eventId                 = event.ev_id
        babyTupleTree.numberOfSelectedLeptons = len(self.selectedLeptons)
        babyTupleTree.leadingLeptonId         = self.selectedLeptons[0].id
        babyTupleTree.leadingLeptonPt         = self.selectedLeptons[0].pT
        babyTupleTree.leadingLeptonEta        = self.selectedLeptons[0].eta
        babyTupleTree.leadingLeptonPhi        = self.selectedLeptons[0].phi
        babyTupleTree.leadingLeptonIso        = self.selectedLeptons[0].iso

        if (len(self.selectedLeptons) >= 2) :
            babyTupleTree.secondLeptonId      = self.selectedLeptons[1].id
            babyTupleTree.secondLeptonPt      = self.selectedLeptons[1].pT
            babyTupleTree.secondLeptonEta     = self.selectedLeptons[1].eta
            babyTupleTree.secondLeptonPhi     = self.selectedLeptons[1].phi
            babyTupleTree.secondLeptonIso     = self.selectedLeptons[1].iso
        else :
            babyTupleTree.secondLeptonId      = 0
            babyTupleTree.secondLeptonPt      = -1
            babyTupleTree.secondLeptonEta     = -9
            babyTupleTree.secondLeptonPhi     = -9
            babyTupleTree.secondLeptonIso     = -1
      
        babyTupleTree.numberOfSelectedJets    = len(self.selectedJets)
        
        # FIXME this is a C++ way of thinking, rewrite it in python
        babyTupleTree.numberOfBTaggedJets     = 0
        for jet in self.selectedJets :
            if (jet.CSV > 0.679) :
                babyTupleTree.numberOfBTaggedJets += 1


        for i, jet in enumerate(self.selectedJets) :
            if (i >= 6) : break;
            babyTupleTree.jetsPt[i]           = jet.pT
            babyTupleTree.jetsPhi[i]          = jet.phi
            babyTupleTree.jetsEta[i]          = jet.eta
            babyTupleTree.jetsCSV[i]          = jet.CSV
            babyTupleTree.jetsCSVv2[i]        = jet.CSVv2
            babyTupleTree.jetsPUid[i]         = jet.PUid

        babyTupleTree.MET                     = event.met_pt
        babyTupleTree.METPhi                  = event.met_phi
        babyTupleTree.MT                      = sqrt(2 * babyTupleTree.leadingLeptonPt  \
                                                       * babyTupleTree.MET              \
                                                       * (1 - cos(babyTupleTree.leadingLeptonPhi - babyTupleTree.METPhi)))
    

