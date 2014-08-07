"""Selection Cuts - Makes Selection Cuts for LNuAA Analysis"""

# Python Module For Selection Cuts
# Created by Christopher Anelli
# 8.4.2014

from ROOT import TLorentzVector
from ROOT import TH1F, TH2F

Histograms = {}
 
# Function to Create and Fill Count Histograms
def fillCountHistograms(particles, key):
    if not key in Histograms:
        Histograms[key] = TH1F(key,key, 2, 0, 2)
    for particle in particles: Histograms[key].Fill(1)

#Function to Create and Fill Number of Particles Histograms
def fillNumParticleHistograms(particles, key):
    if not key in Histograms:
        Histograms[key] = TH1F(key,key, 20, 0, 20)
    Histograms[key].Fill(len(particles))

# Function to Create and Fill Pt Histograms
def fillPtHistograms(particles, key):
    if not key in Histograms:
        Histograms[key] = TH1F(key,key, 400, 0, 200)
    for particle in particles: Histograms[key].Fill(particle.Pt())

# Function To Create and Fill Eta Histograms
def fillEtaHistograms(particles, key):
    if not key in Histograms:
        Histograms[key] = TH1F(key,key, 120, -3, 3)
    for particle in particles: Histograms[key].Fill(particle.Eta())

# Watch out for double counting when particles1 = particles2
def fillDeltaRHistograms(particles1, particles2, key):
    if not key in Histograms:
        Histograms[key] = TH1F(key, key, 200, 0, 10)
    for particle1 in particles1:
        for particle2 in particles2:
            #if particle 1 == particle 2 continue # Don't Histogram Itself
            Histograms[key].Fill(particle1.DeltaR(particle2))
        

def fillStandardHistograms(photons, electrons, muons, suffix):
    #print "working"
    # Photons
    fillCountHistograms(photons, 'Photon_'+suffix)
    fillPtHistograms(photons, 'Photon_Pt_' + suffix)
    fillEtaHistograms(photons, 'Photon_Eta_' + suffix)
    fillNumParticleHistograms(photons, 'Photon_Num_' + suffix)
    # Electrons
    fillCountHistograms(electrons, 'Electron_' + suffix)
    fillPtHistograms(electrons, 'Electron_Pt_' + suffix)
    fillEtaHistograms(electrons, 'Electron_Eta_' + suffix)
    fillNumParticleHistograms(electrons, 'Electron_Num_' + suffix)
    # Muons
    fillCountHistograms(muons, 'Muon_' + suffix)
    fillPtHistograms(muons, 'Muon_Pt_' + suffix)
    fillEtaHistograms(muons, 'Muon_Eta_' + suffix)
    fillNumParticleHistograms(muons, 'Muon_Num_' + suffix)
    # Delta R
    fillDeltaRHistograms(photons, electrons, 'PhotonElectron_DeltaR_' + suffix)
    fillDeltaRHistograms(photons, muons, 'PhotonMuon_DeltaR_' + suffix)
    fillDeltaRHistograms(photons, photons, 'PhotonPhoton_DeltaR_' + suffix)


