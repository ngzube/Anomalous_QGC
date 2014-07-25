from ROOT import gSystem
from ROOT import TFile
from ROOT import TTree
from ROOT import TDirectory, gDirectory
from ROOT import TLorentzVector
from ROOT import TH1F, TH2F
from ROOT import TBranchElement
from math import sqrt, cos

#Working Directory Location
workDirLoc = '/home/cranelli/WGamGam/Anomolous_QGC/CMSSW_5_3_12/src/Anomolous_QGC/Analysis/'
inRootFileDir = '/home/cranelli/WGamGam/Anomolous_QGC/CMSSW_5_3_12/src/Anomolous_QGC/Analysis/test/'

inRootFileName = "../../../../LNuAA_SM/Analysis/LNuAA_SM.root"
TREENAME = "LHEF"

gSystem.Load( 'ExRootClasses_cc.so')
from ROOT import TSortableObject
from ROOT import TRootLHEFEvent
from ROOT import TRootLHEFParticle

#
# Begining of Script
#

inRootFileLoc = inRootFileName
inRootFile = TFile(inRootFileLoc, "READ")
# Set Histograms
h1Mt = TH1F("h1"+"Mt", "Transverse Mass LV", 20, 0, 100)


analysis_tree = inRootFile.Get(TREENAME)
print "Tree ", analysis_tree

num_entries = analysis_tree.GetEntries()
print "Number of Entries: ", num_entries

for entry in xrange(num_entries):
    analysis_tree.GetEntry(entry)
    #print analysis_tree.__dict__


    # Select Event, should be only one per entry.
    event = analysis_tree.Event[0]
    weight = event.Weight
    
    #num_particles = analysis_tree.Particle.GetEntries()
    
    photons = []
    ele = None
    muon = None
    lep = None
    nu_e = None
    nu_m = None
    nu = None
    w = None
    nu = None
    #for particleIndex in xrange(num_particles):
    particles = analysis_tree.Particle
    for particle in particles:
        if particle.PID == 22: photons.append(particle)
        #if particle.PID == 11 or particle.PID == -11: print particle.PID; print "lepton"
        if abs(particle.PID) == 11: ele = particle; lep = particle
        if abs(particle.PID) == 13: muon = particle; lep = particle
        if abs(particle.PID) == 12: nu_e = particle; nu = particle
        if abs(particle.PID) == 14: nu_m = particle; nu = particle
        if abs(particle.PID) == 24: w = particle

    #
    # Analyze Leptons and Neutrinos
    #
    lepLV = TLorentzVector(lep.Px, lep.Py, lep.Pz, lep.E)
    nuLV = TLorentzVector(nu.Px, nu.Py, nu.Pz, nu.E)
    Mt2 = 2*lepLV.Et()*nuLV.Et()*(1-cos(lepLV.DeltaPhi(nuLV)))
    Mt = sqrt(Mt2)
    h1Mt.Fill(Mt, weight)
    
outRootFile = TFile("../LNuAATreeLoop.root", 'UPDATE')
outRootFile.cd() 
#outRootFile.Write #Does not seem to have anything in memmory.
#h1PhoLeadPt.Draw()
#h1PhoLeadPt.Write()
#h1PhoLeadPtWeighted.Write()
h1Mt.Write()

inRootFile.Close()
outRootFile.Close()
    


