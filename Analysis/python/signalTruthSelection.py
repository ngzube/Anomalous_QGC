"""
signalTruthSelection - Makes Histograms, Pre/Post Cuts on ROOT file 
                       for LNuAA Analysis
"""

# Python: main program for signal truth analysis
# Created by Christopher Anelli, 8.4.2014
# Edits by Nicholas Zube, 8.22.2014
# Tested in Python 2.6.4

from ROOT import gSystem
from ROOT import TFile
from ROOT import TTree
from ROOT import TDirectory, gDirectory
from ROOT import TLorentzVector
from ROOT import TH1F, TH2F
from ROOT import TBranchElement
from math import sqrt, cos
#Local Modules
import particleIdentification
import objectCuts
#import overlapCuts
import eventCuts
import parentCuts
import particleDataClass
import histogramBuilder
import histPublish
import htmlTable


# Define Root Files and Tree Locations and Names
workDirLoc = '/home/nzube/qgc/CMSSW_5_3_19/src/Anomolous_QGC/Analysis/python/'
inRootFileDir = '../'
inRootFileName = 'SignalTruth_WAA_FSR.root'
treeLoc = 'ggNtuplizer/EventTree'
outRootFileName = 'signalTruthFSRSelection.root'
histDirLoc = 'histF/'
#print sys.path

def signalTruthSelection():

    inRootFileLoc = inRootFileDir + inRootFileName
    inRootFile = TFile(inRootFileLoc, "READ")
 
    # Set Histograms
    h1PhoLeadPt = TH1F("h1PhoLeadPt","Lead Photon Pt", 400, 0, 200)
    h1PhoLeadEta = TH1F("h1PhoLeadEta", "Lead Photon Eta", 100, -3, 3)
    h2M3M4 = TH2F("h2M4M4", "M3 vs M4", 400, 0, 200, 400, 0 ,200)
    h1pcuts = TH1F("h1pcuts", "P Counts after cuts", 5, 0, 4)
    h1ecuts = TH1F("h1ecuts", "E Counts after cuts", 5, 0, 4)
    h1mcuts = TH1F("h1mcuts", "M Counts after cuts", 5, 0, 4)
    ## Note: I don't know how "prefix" string should be set, 
    ## code not valid yet
    #prefix = ""
    #h1PhoLeadPtWeighted = TH1F("h1" + prefix + "PhoLeadPtWeighted", 
    #                           prefix +"Lead Photon Pt Weighted",
    #                           400, 0, 200)   
    #h1Mt = TH1F("h1"+prefix+"Mt", prefix + "Transverse Mass LV", 20, 0, 100)

    analysis_tree = inRootFile.Get(treeLoc)
    print "Tree ", analysis_tree  
    num_entries = analysis_tree.GetEntries()
    print "Number of Entries: ", num_entries
    
    evEcount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    evMcount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # Loop Over Entries
    for entry in xrange(num_entries-200000):
        analysis_tree.GetEntry(entry)
        #print analysis_tree.__dict__
            
        ## Select Event, should be only one per entry.
        #event = analysis_tree.Event[0]
        #weight = event.Weight

        # Assign Particles
        photons = []
        electrons = []
        muons = []
        nu_es = []
        nu_ms = []
        ws = []


        # Particle Identification
        particleIdentification.assignParticles(
                analysis_tree, photons, electrons, muons, nu_es, nu_ms, ws)
        histogramBuilder.fillStandardHistograms(photons, electrons, muons, 
                "1_PreCut")
        histogramBuilder.fillPtHistograms(electrons, '_E_PT_PreCut', 
                                          400, 0, 20)
        histogramBuilder.fillPtHistograms(muons, '_Mu_PT_PreCut', 400, 0, 70)
        mAnalysis(photons, electrons, muons, nu_es, nu_ms, h2M3M4, 
                  "1_PreCut")
        if eventTest(electrons, photons): evEcount[0] += 1        
        if eventTest(muons, photons): evMcount[0] += 1        
        #fillCutCount(photons, electrons, muons, h1pcuts, h1ecuts, h1mcuts, 1)

        # Object Cuts: Make Kinematic Selection Cuts
        photons = objectCuts.selectOnPhotonKinematics(photons)
        histogramBuilder.fillStandardHistograms(photons, electrons, muons, 
                                                "2a_PostPhotonObjectCuts")  
        if eventTest(electrons, photons): evEcount[1] += 1        
        if eventTest(muons, photons): evMcount[1] += 1        
        electrons = objectCuts.selectOnElectronKinematics(electrons)
        histogramBuilder.fillStandardHistograms(photons, electrons, muons, 
                                                "2b_PostElectronObjectCuts")  
        if eventTest(electrons, photons): evEcount[2] += 1        
        if eventTest(muons, photons): evMcount[2] += 1        
        muons = objectCuts.selectOnMuonKinematics(muons)
        histogramBuilder.fillStandardHistograms(photons, electrons, muons, 
                                                "2c_PostMuonObjectCuts")  
        if eventTest(electrons, photons): evEcount[3] += 1        
        if eventTest(muons, photons): evMcount[3] += 1        
        mAnalysis(photons, electrons, muons, nu_es, nu_ms, h2M3M4, 
                  "2_PostObjectCuts")        
        #fillCutCount(photons, electrons, muons, h1pcuts, h1ecuts, h1mcuts, 2)
        
        # Parentage cuts: Make cuts of leptons with non-W parents,
        # and cuts of photons with non-quark/lepton/W parents
        photons = parentCuts.selectOnPhotonParent(photons)
        histogramBuilder.fillStandardHistograms(photons, electrons, muons, 
                                                "3a_PostPhotonParentCuts")  
        if eventTest(electrons, photons): evEcount[4] += 1        
        if eventTest(muons, photons): evMcount[4] += 1        
        electrons = parentCuts.selectOnElectronParent(electrons)
        histogramBuilder.fillStandardHistograms(photons, electrons, muons, 
                                                "3b_PostElectronParentCuts")  
        if eventTest(electrons, photons): evEcount[5] += 1        
        if eventTest(muons, photons): evMcount[5] += 1        
        muons = parentCuts.selectOnMuonParent(muons)
        histogramBuilder.fillStandardHistograms(photons, electrons, muons, 
                                                "3c_PostMuonParentCuts")
        if eventTest(electrons, photons): evEcount[6] += 1        
        if eventTest(muons, photons): evMcount[6] += 1        
        mAnalysis(photons, electrons, muons, nu_es, nu_ms, h2M3M4, 
                  "3_PostParentCuts")          
        #fillCutCount(photons, electrons, muons, h1pcuts, h1ecuts, h1mcuts, 3)

        # Event Cuts: Make population requirement and overlap cuts
        if not eventCuts.passReqNumParticles(photons, electrons, muons): 
            continue
        if not eventCuts.passPhotonPhotonDeltaR(photons): 
            continue
        # Electron Channel
        if len(electrons) == 1:
            if not eventCuts.passPhotonElectronDeltaR(photons, electrons): 
                continue
            histogramBuilder.fillStandardHistograms(
                    photons, electrons, muons, 
                    "4a_PostEventCuts_EChannel")            
            if eventTest(electrons, photons): evEcount[7] += 1
            
            if not eventCuts.passZ2Mass(photons, electrons): continue
            histogramBuilder.fillStandardHistograms(
                    photons, electrons, muons, 
                    "5_PostZ2MCut_EChannel")
            if eventTest(electrons, photons): evEcount[8] += 1
            
            if not eventCuts.passZ3Mass(photons, electrons): continue
            histogramBuilder.fillStandardHistograms(
                    photons, electrons, muons, 
                    "6_PostZ3MCut_EChannel")
            if eventTest(electrons, photons): evEcount[9] += 1
            mAnalysis(photons, electrons, muons, nu_es, nu_ms, h2M3M4, 
                      "7_PostEventCuts_EChannel")                   

        # Muon Channel
        if len(muons) == 1:
            if not eventCuts.passPhotonMuonDeltaR(photons, muons): 
                continue
            histogramBuilder.fillStandardHistograms(
                    photons, electrons, muons, "4b_PostEventCuts_MuChannel")
            if eventTest(muons, photons): evMcount[7] += 1  
                  
            if not eventCuts.passZ2Mass(photons, muons): continue
            histogramBuilder.fillStandardHistograms(
                    photons, electrons, muons, 
                    "5_PostZ2MCut_MuChannel")
            #if eventTest(muons, photons): evMcount[8] += 1
            
            if not eventCuts.passZ3Mass(photons, muons): continue
            histogramBuilder.fillStandardHistograms(
                    photons, electrons, muons, 
                    "6_PostZ3MCut_MuChannel")
            #if eventTest(muons, photons): evMcount[9] += 1

            mAnalysis(photons, electrons, muons, nu_es, nu_ms, h2M3M4, 
                      "7_PostEventCuts_MuChannel")
        #fillCutCount(photons, electrons, muons, h1pcuts, h1ecuts, h1mcuts, 4)
        


    outRootFile = TFile(outRootFileName, 'RECREATE')
    outRootFile.cd()
    #h1PhoLeadPt.Write()
    #h1PhoLeadEta.Write()
    h2M3M4.Write()
    #h1pcuts.Write()
    #h1ecuts.Write()
    #h1mcuts.Write()
    #h1PhoLeadPtWeighted.Write()
    #h1Mt.Write()
    
    # Iterate Over Selection Histograms
    for key, Histogram in histogramBuilder.Histograms.iteritems():
        Histogram.Write()
    inRootFile.Close()
    outRootFile.Close()
    
    # Make .png files for all histograms
    # Note: Run PyROOT in batch mode (-b) to suppress canvas output
    print("E: ", evEcount, ", M: ", evMcount)
    histPublish.histToPNG(outRootFileName, histDirLoc)
    histPublish.makeAcceptanceTable(evEcount, evMcount)
    
    
    
# Helper Functions

def eventTest(leptons, photons):
    if len(leptons) > 0 and len(photons) > 1: return True
    return False

def selectLead(particles):
    maxPt = 0
    lead = None
    for particle in particles:
        if particle.Pt() > maxPt :
            maxPt = particle.Pt()
            lead =  particle
    return lead

def selectSub(particles):
    maxPt, submaxPt = 0, 0
    lead, sub = None, None
    for particle in particles:
        if particle.Pt() > maxPt:
            sub = lead
            submaxPt = maxPt
            lead = particle
            maxPt = particle.Pt()
        elif particle.Pt() > submaxPt:
            sub = particle
            submaxPt = particle.Pt()   
    return sub

def fillCutCount(photons, electrons, muons, h1pcuts, h1ecuts, h1mcuts, 
                 cutNum = 0):
    pcount = len(photons)
    ecount = len(electrons)
    mcount = len(muons)
    for a in xrange(pcount): h1pcuts.Fill(cutNum)
    for a in xrange(ecount): h1ecuts.Fill(cutNum)
    for a in xrange(mcount): h1mcuts.Fill(cutNum)

def mAnalysis(photons, electrons, muons, nu_es, nu_ms, h2M3M4, suffix):
    # Leading/Sub-leading Photon Analysis        
    leptons = electrons + muons
    nus = nu_es + nu_ms
    
    leadPhoton = selectLead(photons)
    subPhoton = selectSub(photons)
    lepton = selectLead(leptons) # Let signal lepton be the one w/ highest PT 
    nu = selectLead(nus)
    
    if leadPhoton != None :
        histogramBuilder.fillPtHistograms([leadPhoton], 
                                          'Photon(Leading)_Pt_' + suffix)
        histogramBuilder.fillEtaHistograms([leadPhoton], 
                                          'Photon(Leading)_Eta_' + suffix)
    # Near-Z-Mass checks
    if(leadPhoton != None and subPhoton != None and lepton != None):
        m2_L = (leadPhoton + lepton).M()
        m2_S = (subPhoton + lepton).M()
        m3 = (leadPhoton + subPhoton + lepton).M()
        histogramBuilder.fillMHistograms(m2_L, 'Z2M(A_Lead+L)_' + suffix)
        histogramBuilder.fillMHistograms(m2_S, 'Z2M(A_Sub+L)_' + suffix)
        histogramBuilder.fillMHistograms(m3, 'Z3M(A+A+L)_' + suffix)               
    
    # Near-W-Mass checks
    if(leadPhoton != None and subPhoton != None and lepton != None 
       and nu != None):
        m3 = (leadPhoton + lepton + nu).M() # no sub leading lepton
        m4 = (leadPhoton + subPhoton + lepton + nu).M()
        histogramBuilder.fillMHistograms(m3, '3M(A+L+Nu)_' + suffix)
        histogramBuilder.fillMHistograms(m4, '4M(A+A+L+Nu)_' + suffix)        
        h2M3M4.Fill(m3, m4)

if __name__=="__main__":
    signalTruthSelection()
    