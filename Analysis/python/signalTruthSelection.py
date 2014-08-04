from ROOT import gSystem
from ROOT import TFile
from ROOT import TTree
from ROOT import TDirectory, gDirectory
from ROOT import TLorentzVector
from ROOT import TH1F, TH2F
from ROOT import TBranchElement
from math import sqrt, cos
#import sys
#My Own Help Functions
import selectionCuts

#
# Define Root Files and Tree Locations and Names
#
workDirLoc = '/home/cranelli/WGamGam/Anomolous_QGC/CMSSW_5_3_12/src/Anomolous_QGC/Analysis/python/'
inRootFileDir = '../test/'
inRootFileName = 'signalTruth_WAA_ISR_Job0.root'
#inRootFileDir = '/data/users/cranelli/WGamGam/SignalTruth'
#inRootFileName = "/signaltruth_job_summer12_WAA_ISR.root"
treeLoc = "ggNtuplizer/EventTree"
outRootFileName = 'signalTruthISRSelection.root'
#print sys.path

#
# Begining of Analysis Code
#
def signalTruthSelection():

    inRootFileLoc = inRootFileDir + inRootFileName
    inRootFile = TFile(inRootFileLoc, "READ")
    # Set Histograms
    h1PhoLeadPt = TH1F("h1PhoLeadPt","Lead Photon Pt", 400, 0, 200)
    h1PhoLeadEta = TH1F("h1PhoLeadEta", "Lead Photon Eta", 100, -3, 3)
    h2M3M4 = TH2F("h2M4M4", "M3 vs M4", 400, 0, 200, 400, 0 ,200)
    # h1PhoLeadPtWeighted = TH1F("h1" + prefix + "PhoLeadPtWeighted", prefix +"Lead Photon Pt Weighted",
    #                           400, 0, 200)
    
    # h1Mt = TH1F("h1"+prefix+"Mt", prefix + "Transverse Mass LV", 20, 0, 100)


    analysis_tree = inRootFile.Get(treeLoc)
    print "Tree ", analysis_tree
    
    num_entries = analysis_tree.GetEntries()
    print "Number of Entries: ", num_entries
    

    for entry in xrange(num_entries):
        analysis_tree.GetEntry(entry)
        # print analysis_tree.__dict__
            
        # Select Event, should be only one per entry.
        # event = analysis_tree.Event[0]
        # weight = event.Weight

        #Will be filled with TLorentz Vector, for now.
        photons = []
        electrons = []
        muons = []
        leptons = []
        nu_es = []
        nu_ms = []
        nus = []
        ws = []
        
        truthIDs = analysis_tree.mcPID
        for index in xrange(analysis_tree.nMC):
            """
            if truthIDs[index] == 22: photons.append(index)
            if abs(truthIDs[index]) == 11: electrons.append(index); leptons.append(index)
            if abs(truthIDs[index]) == 13: muons.append(index); leptons.append(index)
            if abs(truthIDs[index]) == 12: nu_es.append(index); nus.append(index)
            if abs(truthIDs[index]) ==14: nu_ms.append(index); nus.append(index)
            if abs(truthIDs[index]) == 24: ws.append(index)
            """
        
            if truthIDs[index] == 22: photons.append(makeTL(analysis_tree, index))
            # if particle.PID == 11 or particle.PID == -11: print particle.PID; print "lepton"
            if abs(truthIDs[index]) == 11:
                electrons.append(makeTL(analysis_tree, index))
                leptons.append(makeTL(analysis_tree, index))
            if abs(truthIDs[index]) == 13:
                muons.append(makeTL(analysis_tree, index))
                leptons.append(makeTL(analysis_tree, index))
            if abs(truthIDs[index]) == 12:
                nu_es.append(makeTL(analysis_tree, index))
                nus.append(makeTL(analysis_tree, index))
            if abs(truthIDs[index]) == 14:
                nu_ms.append(makeTL(analysis_tree, index))
                nus.append(makeTL(analysis_tree, index))
            if abs(truthIDs[index]) == 24:
                ws.append(makeTL(analysis_tree, index))
        #
        # Selection Cuts
        #
        # Make Kinematic Selection Cuts
        photons = selectionCuts.selectOnPhotonKinematics(photons)
        #electrons = selectionCuts.selectOnElectronKinematics(electrons)
        #muons = selectionCuts.selectOnMuonKinematics(muons)
        # Make Delta R Selection Cuts
        leadPhoton = selectLead(photons)
        #lepton = selectLead(leptons) # Have signal electron be the one with highest Pt 
        #nu = selectLead(nus)
        #subPhoton = selectSub(photons)

        if leadPhoton != None :
            h1PhoLeadPt.Fill(leadPhoton.Pt())
            h1PhoLeadEta.Fill(leadPhoton.Eta())
        
        """
        if leadPhoton != None and subPhoton != None and lepton != None and nu != None:
            m3 = (leadPhoton + lepton + nu).M() #Does not include sub leading lepton
            m4 = (leadPhoton + subPhoton + lepton +nu).M()
            h2M3M4.Fill(m3, m4)
        """
                         
    outRootFile = TFile(outRootFileName, 'RECREATE')
    outRootFile.cd()
    # outRootFile.Write #Does not seem to have anything in memmory.
    h1PhoLeadPt.Write()
    h1PhoLeadEta.Write()
    #Iterate Over Selection Histograms
    for key, Histogram in selectionCuts.SelectionHistograms.iteritems():
        Histogram.Write()
    #h2M3M4.Write()
    # h1PhoLeadPtWeighted.Write(
    # h1Mt.Write()
    inRootFile.Close()
    outRootFile.Close()

def makeTL(analysis_tree, index):
    photonTL = TLorentzVector()
    # Define TLorentz Vector
    photonTL.SetPtEtaPhiE(analysis_tree.mcPt[index], analysis_tree.mcEta[index],
                          analysis_tree.mcPhi[index],analysis_tree.mcE[index])
    return photonTL

def selectLead(particles):
    maxPt = 0
    lead = None
    for particle in particles:
        if particle.Pt() > maxPt :
            maxPt = particle.Pt()
            lead =  particle
    return lead

def selectSub(particles):
    maxPt = 0
    lead = None
    sub = None
    for particle in particles:
        if particle.Pt() > maxPt:
            maxPt = particle.Pt()
            sub = lead
            lead = particle
        
    return sub

if __name__=="__main__":
    signalTruthSelection()
    


