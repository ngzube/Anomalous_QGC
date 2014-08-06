"""Selection Cuts - Makes Selection Cuts for LNuAA Analysis"""

# Python Module For Selection Cuts
# Created by Christopher Anelli
# 8.4.2014

from ROOT import TLorentzVector
from ROOT import TH1F, TH2F

import histogramBuilder


# Particle Number
reqNumPhotons = 2
reqNumLeptons = 1

# Delta R
minPhotonPhotonDeltaR = 0.3
minPhotonElectronDeltaR = 0.4
minPhotonMuonDeltaR = 0.4

#Reject Event if it does not have a Single Lepton and Two Photons
def passReqNumParticles(photons, electrons, muons):
    if len(photons) == reqNumPhotons:
        if len(electrons) == reqNumLeptons and len(muons) == 0: return True
        if len(electrons) == 0 and len(muons) == reqNumLeptons: return True
    return False

# Reject Event if the Photons are Too Close
def passPhotonPhotonDeltaR(photons):
    for photon1 in photons:
        for photon2 in photons:
            if photon1 == photon2: continue # Do Not Compare it to Itself
            if photon1.DeltaR(photon2) < minPhotonPhotonDeltaR: return False
    # Only if all pairings pass
    return True 

# Reject Event if  Photon and Electron are too close
def passPhotonElectronDeltaR(photons, electrons):
    for photon in photons:
        for electron in electrons:
            if photon.DeltaR(electron) < minPhotonElectronDeltaR: return False
    # Only if all pairings pass
    return True

def passPhotonMuonDeltaR(photons, muons):
    for photon in photons:
        for muon in muons:
            if photon.DeltaR(muon) < minPhotonMuonDeltaR: return False
    # Only if all pairings pass
    return True
