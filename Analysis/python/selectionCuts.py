"""Selection Cuts - Makes Selection Cuts for LNuAA Analysis"""

# Python Module For Selection Cuts
# Created by Christopher Anelli
# 8.4.2014

from ROOT import TLorentzVector
from ROOT import TH1F, TH2F

#Selection Cut Values
#Photons
minPhotonPt = 15
maxPhotonEta = 2.5
minPhotonEndCapEta = 1.47
maxPhotonEndCapEta = 1.57
#Electrons
minElectronPt = 30
maxElectronEta = 2.5
#Muons
minMuonPt = 25
maxMuonEta = 2.5

# Python Dictionairy
SelectionHistograms = {}

def selectOnPhotonKinematics(photons):
    #if photons != None:
    fillPtHistograms(photons, 'Photon_Pt_PreCut')
    photons = filter(lambda photon: photon.Pt() > minPhotonPt, photons)
    fillPtHistograms(photons, 'Photon_Pt_PostPhotonPtCut')
    photons = filter(lambda photon: abs(photon.Eta()) < maxPhotonEta, photons)
    photons = filter(lambda photon: abs(photon.Eta()) < minPhotonEndCapEta
                     or abs(photon.Eta()) > maxPhotonEndCapEta, photons)
    return photons

def selectOnElectronKinematics(electrons):
    #if electrons != None:
    electrons = filter(lambda electron: electron.Pt() > minElectronPt, electrons)
    electrons = filter(lambda electron: abs(electron.Eta()) < maxElectronEta, electrons)
    return electrons

def selectOnMuonKinematics(muons):
    muons = filter(lambda muon: muon.Pt() > minMuonPt, muons)
    muons = filter(lambda muon: abs(muon.Eta()) < maxMuonEta, muons)
    return muons

def fillPtHistograms(particles, key):
    if not key in SelectionHistograms:
        SelectionHistograms[key] = TH1F(key,key, 400, 0, 200)
    for particle in particles: SelectionHistograms[key].Fill(particle.Pt())
    
