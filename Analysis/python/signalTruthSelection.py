"""
signalTruthSelection - Makes Histograms, Pre/Post Cuts on ROOT file 
                       for LNuAA Analysis
"""

# Python: main program for signal truth analysis
# Note: Run PyROOT in batch mode (-b) to suppress canvas output

# Created by Christopher Anelli, 8.4.2014
# Edits by Nicholas Zube, 9.30.2014
# Tested in Python 2.6.4

from ROOT import gSystem
from ROOT import TFile
from ROOT import TTree
from ROOT import TDirectory, gDirectory
from ROOT import TLorentzVector
from ROOT import TH1F, TH2F
from ROOT import TBranchElement
#Local Modules
import particleIdentification
import objectCuts
import eventCuts
import parentCuts
import histogramBuilder
import histPublish

# Define the following variables before running:
# Input file names
workDirLoc = '/home/nzube/qgc/CMSSW_5_3_19/src/Anomolous_QGC/Analysis/python/'
inRootFileDir = '../'
inRootFileName = 'signaltruth_job_summer12_Wgg_FSR.root'
treeLoc = 'ggNtuplizer/EventTree'
# Output file names
outRootFileName = 'signalTruthFSRSelection_Full.root'
histDirLoc = 'histF/'
acceptanceTableFileName = "FSR"
dressedLeptonsFlag = "off"

# Conditions for analysis: 
# tauVersion, if set to on, will do the analysis for tau events only
tauVersion = "off"
dressedLeptonsFlag = "off"
ptBins = [0, 15, 25, 40, 70]

def signalTruthSelection():

    inRootFileLoc = inRootFileDir + inRootFileName
    inRootFile = TFile(inRootFileLoc, "READ")
 
    # Set basic histograms
    #h1PhoLeadPt = TH1F("h1PhoLeadPt","Lead Photon Pt", 400, 0, 200)
    #h1PhoLeadEta = TH1F("h1PhoLeadEta", "Lead Photon Eta", 100, -3, 3)
    h2M3M4 = TH2F("h2M4M4", "M3 vs M4", 400, 0, 200, 400, 0 ,200)
    #h1pcuts = TH1F("h1pcuts", "P Counts after cuts", 5, 0, 4)
    #h1ecuts = TH1F("h1ecuts", "E Counts after cuts", 5, 0, 4)
    #h1mcuts = TH1F("h1mcuts", "M Counts after cuts", 5, 0, 4)

    print "Running on file: ", inRootFileLoc
    analysis_tree = inRootFile.Get(treeLoc)
    print "Tree ", analysis_tree  
    num_entries = analysis_tree.GetEntries()
    print "Number of Entries: ", num_entries
    
    # Lists of events remaining after each cut step 
    # (e.g., event_Electron_count)
    numberOfCuts = 14    
    evEcount = [0] * numberOfCuts
    evMcount = [0] * numberOfCuts
    evTcount = [0] * numberOfCuts
    countByPT = {}

    # Uses a dictionary to store [Ecounts, Mcounts, Tcounts] by PT bin for each cut
    # countByPt[pt bin min][cut #][# e counts, # mu counts, # t counts]
    for ptKey in ptBins:
        a = {}
        for cutNum in xrange(numberOfCuts):
            a[cutNum] = [0,0,0]
        countByPT[ptKey] = a
            
    # Loop Over Entries (Master Loop)
    for entry in xrange(5000):  #!!! change to num_entries
        analysis_tree.GetEntry(entry)

        # Assign Particles
        photons = []
        electrons = []
        muons = []
        taus = []
        nu_es = []
        nu_ms = []
        nu_ts = []
        ws = []

        # Particle Identification step
        particleIdentification.assignParticles(
                analysis_tree, photons, electrons, muons, taus, nu_es, nu_ms, 
                nu_ts, ws)
        
        # Dressed lepton step: add PT of objects in cone <0.2 deltaR to a lepton
        if dressedLeptonsFlag == "on":
            dressLeptons(photons, electrons, muons, taus)      
       
        # Lepton channel assignment step: lepton with highest PT sets channel
        # for the event.
        channelName = leptonChannelSelect(selectLead(electrons), selectLead(muons),
                                          selectLead(taus))
          
        [countByPT, evEcount, evMcount, evTcount] = fillCountAndHist(
                photons, electrons, muons, taus, ptBins, 
                "1_PreCuts_", 0,
                countByPT, evEcount, evMcount, evTcount, channelName)
            

        # Object Cuts: Make Kinematic Selection Cuts
        photons = objectCuts.selectOnPhotonKinematics(photons)
        [countByPT, evEcount, evMcount, evTcount] = fillCountAndHist(
                photons, electrons, muons, taus, ptBins, 
                "2a_PostPhotonObjectCuts_", 1,
                countByPT, evEcount, evMcount, evTcount,channelName)
        
        electrons = objectCuts.selectOnElectronKinematics(electrons)
        [countByPT, evEcount, evMcount, evTcount] = fillCountAndHist(
                photons, electrons, muons, taus, ptBins, 
                "2b_PostElectronObjectCuts_", 2,
                countByPT, evEcount, evMcount, evTcount,channelName)
       
        muons = objectCuts.selectOnMuonKinematics(muons)
        [countByPT, evEcount, evMcount, evTcount] = fillCountAndHist(
                photons, electrons, muons, taus, ptBins, 
                "2c_PostMuonObjectCuts_", 3,
                countByPT, evEcount, evMcount, evTcount,channelName)

        taus = objectCuts.selectOnTauKinematics(taus)
        [countByPT, evEcount, evMcount, evTcount] = fillCountAndHist(
                photons, electrons, muons, taus, ptBins, 
                "2d_PostTauObjectCuts_", 4,
                countByPT, evEcount, evMcount, evTcount,channelName)

        # Parentage cuts: Make cuts of leptons with non-W parents,
        # and cuts of photons with non-quark/lepton/W parents
        photons = parentCuts.selectOnPhotonParent(photons)
        [countByPT, evEcount, evMcount, evTcount] = fillCountAndHist(
                photons, electrons, muons, taus, ptBins, 
                "3a_PostPhotonParentCuts_", 5,
                countByPT, evEcount, evMcount, evTcount,channelName) 
                   
        electrons = parentCuts.selectOnElectronParent(electrons)
        [countByPT, evEcount, evMcount, evTcount] = fillCountAndHist(
                photons, electrons, muons, taus, ptBins, 
                "3b_PostElectronParentCuts_", 6,
                countByPT, evEcount, evMcount, evTcount,channelName)   

        muons = parentCuts.selectOnMuonParent(muons)
        [countByPT, evEcount, evMcount, evTcount] = fillCountAndHist(
                photons, electrons, muons, taus, ptBins, 
                "3c_PostMuonParentCuts_", 7,
                countByPT, evEcount, evMcount, evTcount,channelName) 
        
        taus = parentCuts.selectOnTauParent(taus)
        [countByPT, evEcount, evMcount, evTcount] = fillCountAndHist(
                photons, electrons, muons, taus, ptBins, 
                "3d_PostTauParentCuts_", 8,
                countByPT, evEcount, evMcount, evTcount,channelName) 
        
        # Event Cuts: beginning of split into electron and muon channels
        # Exact population requirement
        if not eventCuts.passReqNumParticles(photons, electrons, muons, taus):
            continue
        [countByPT, evEcount, evMcount, evTcount] = fillCountAndHist(
                photons, electrons, muons, taus, ptBins, 
                "4_PostExactPopulationCuts_", 9,
                countByPT, evEcount, evMcount, evTcount,channelName)         
        
        if not eventCuts.passPhotonPhotonDeltaR(photons): 
            continue
        [countByPT, evEcount, evMcount, evTcount] = fillCountAndHist(
                photons, electrons, muons, taus, ptBins, 
                "5_PostPhotonDeltaRCuts_", 10,
                countByPT, evEcount, evMcount, evTcount,channelName)              
        
        # Electron Channel
        if len(electrons) == 1:           
            if not eventCuts.passPhotonElectronDeltaR(photons, electrons):
                continue
            [countByPT, evEcount, evMcount, evTcount] = fillCountAndHist(
                    photons, electrons, muons, taus, ptBins, 
                    "6_PostElectronDeltaRCuts_", 11,
                    countByPT, evEcount, evMcount, evTcount,"e")         
            
            if not eventCuts.passZ2Mass(photons, electrons): continue
            [countByPT, evEcount, evMcount, evTcount] = fillCountAndHist(
                    photons, electrons, muons, taus, ptBins, 
                    "7_PostZ2MCut_", 12,
                    countByPT, evEcount, evMcount, evTcount,"e")         
            
            if not eventCuts.passZ3Mass(photons, electrons): continue
            [countByPT, evEcount, evMcount, evTcount] = fillCountAndHist(
                    photons, electrons, muons, taus, ptBins, 
                    "8_PostZ3MCut_", 13,
                    countByPT, evEcount, evMcount, evTcount,"e")         

        # Muon Channel
        if len(muons) == 1:
            if not eventCuts.passPhotonMuonDeltaR(photons, muons): 
                continue
            [countByPT, evEcount, evMcount, evTcount] = fillCountAndHist(
                    photons, electrons, muons, taus, ptBins, 
                    "6_PostMuonDeltaRCuts_", 11,
                    countByPT, evEcount, evMcount, evTcount,"m")         

        # Tau Channel
        if len(taus) == 1:
            if not eventCuts.passPhotonTauDeltaR(photons, muons): 
                continue
            [countByPT, evEcount, evMcount, evTcount] = fillCountAndHist(
                    photons, electrons, muons, taus, ptBins, 
                    "6_PostTauDeltaRCuts_", 11,
                    countByPT, evEcount, evMcount, evTcount,"t")         

        mAnalysis(photons, electrons, muons, nu_es, nu_ms, h2M3M4, 
                  "9_PostALL")

    outRootFile = TFile(outRootFileName, 'RECREATE')
    outRootFile.cd()
    h2M3M4.Write()
    
    # Iterate Over Selection Histograms
    for key, Histogram in histogramBuilder.Histograms.iteritems():
        Histogram.Write()
    inRootFile.Close()
    outRootFile.Close()
    
    print("E: ", evEcount, ", M: ", evMcount, ", T: ", evTcount)
    for ptKey in countByPT:
        print "Bin", ptKey, "by cut:", countByPT[ptKey]

    # Make .png files for all histograms
    # Note: Run PyROOT in batch mode (-b) to suppress canvas output
    histPublish.histToPNG(outRootFileName, histDirLoc)
    # Make an HTML table of acceptance cut flow
    histPublish.makeAcceptanceTable(evEcount, evMcount, evTcount, 
                                    acceptanceTableFileName + "_All")
    
    for ptKey in ptBins:
        for i in xrange(numberOfCuts):
            evEcount[i] = countByPT[ptKey][i][0]
            evMcount[i] = countByPT[ptKey][i][1]            
            evTcount[i] = countByPT[ptKey][i][2]            
        histPublish.makeAcceptanceTable(evEcount, evMcount, evTcount,  
                                        acceptanceTableFileName + 
                                        "_" + str(ptKey) + "PT")
        













    
##############################    
###    Helper Functions    ###
##############################
# Boolean: returns true if event has at least 1 lepton and 2 photons
def eventTest(leptons, photons):
    if len(leptons) > 0 and len(photons) > 1 : return True
    return False

# Returns leading photon from list of photons, 
# returns None if list is empty
def selectLead(particles):
    maxPt = 0
    lead = None
    for particle in particles:
        if particle.Pt() > maxPt :
            maxPt = particle.Pt()
            lead =  particle
    return lead

# Returns subleading photon from list of photons, 
# returns None if # number of photons <= 1
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

# Given particle lists and cut information, iterates event counters and
# stores data in the standard histograms
def fillCountAndHist(photons, electrons, muons, taus, ptBins, histKey, cutNum,
                     countByPT, evEcount, evMcount, evTcount, channelName = 'e'):
    if channelName == 'e':
        leptons = electrons
        histKey += "E_"
    elif channelName == 'm': 
        leptons = muons
        histKey += "M_"
    elif channelName == 't': 
        leptons = taus
        histKey += "T_"
    
    if eventTest(leptons, photons):
        photonPTBin = whichPTBin(selectLead(photons), ptBins)
        if channelName == 'e': 
            evEcount[cutNum] += 1
            countByPT[photonPTBin][cutNum][0] += 1
        elif channelName == 'm': 
            evMcount[cutNum] += 1
            countByPT[photonPTBin][cutNum][1] += 1
        elif channelName == 't': 
            evTcount[cutNum] += 1
            countByPT[photonPTBin][cutNum][2] += 1
              
        histogramBuilder.fillStandardHistograms(photons, electrons, 
                muons, taus, histKey + str(photonPTBin) + "_PT")
    return [countByPT, evEcount, evMcount, evTcount]          

# Given the leading leptons in an event, returns a character indicating
# which channel the event should be palced in.
def leptonChannelSelect(leadE, leadM, leadT):
    if leadE != None:
        leadEPt = leadE.Pt()
    else: leadEPt = 0
    
    if leadM != None:
        leadMPt = leadM.Pt()
    else: leadMPt = 0
    
    if leadT != None:
        leadTPt = leadT.Pt()
    else: leadTPt = 0
    
    if leadMPt > leadEPt and leadMPt > leadTPt:
        channelName = 'm'
    elif leadTPt > leadEPt and leadTPt > leadMPt:
        channelName = 't'
    # In the unusual case of equal PT, we use electron channel as the default    
    else:
        channelName = 'e'
    return channelName


def dressLeptons(photons, electrons, muons, taus):
    DRLimit = 0.2
    
    # If a photon is within the limit DR of a lepton, add the PT (4-vector) to 
    # that lepton exclusively (breaks to next photon if a dressed match is found).
    for photon in photons:
        for electron in electrons:
            if electron.DeltaR(photon) <= DRLimit:
                        electron = electron + photon
                        # Breaks from loop and goes to next photon if a dR<limit match is found
                        break
                        
        # If no matches in electrons are found, muons are checked
        else:
            for muon in muons:
                if muon.DeltaR(photon) <= DRLimit:
                        muon = muon + photon
                        break
            # If no matches in muons are found, taus are checked        
            else:     
                for tau in taus:
                    if tau.DeltaR(photon) <= DRLimit:
                        tau = tau + photon
                        break

    # If a lepton is within the limit DR of a lepton, add the smaller PT (4-vector) 
    # to the lepton with greater PT
    for electron in electrons:
        for muon in muons:
            if electron.DeltaR(muon) <= DRLimit:
                if electron.Pt() > muon.Pt(): 
                    electron = electron + muon
                else: 
                    muon = muon + electron
                break
        else: 
            for tau in taus:
                if electron.DeltaR(tau) <= DRLimit:
                    if electron.Pt() > tau.Pt():
                        electron = electron + tau
                    else: 
                        tau = tau + electron
                    break
                
    for muon in muons:
        for tau in taus:
            if muon.DeltaR(tau) <= DRLimit:
                if muon.Pt() > tau.Pt(): 
                    muon = muon + tau
                else: 
                    tau = tau + muon
                                   
    
# Creates a histogram comparing Mass(L-Nu-g) to Mass (L-L-Nu-g)
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

# Given a photon and an array of bin minimums, returns an integer for which
# bin it belongs in        
def whichPTBin(leadPhoton, ptBins):
    if leadPhoton != None:
        for i in xrange(len(ptBins)-1):
            min = ptBins[i]
            max = ptBins[i+1]
            if leadPhoton.Pt() >= min and leadPhoton.Pt()< max:
                return min
        finalMin = ptBins[len(ptBins)-1]
        if leadPhoton.Pt() >= finalMin:
            return finalMin
    return 0






if __name__=="__main__":
    signalTruthSelection()
    