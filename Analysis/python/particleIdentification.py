"""Particle Identification - Assigns Particles From a Tree and Stores Them"""

# Python module for creating Particle data objects using particleDataClass
# Created by Christopher Anelli, 8.4.2014
# Edits by Nicholas Zube, 8.22.2014
# Tested in Python 2.6.4

from ROOT import TTree
from ROOT import TLorentzVector 
import particleDataClass
#import histogramBuilder

maxDressedLepDeltaR = 0.2

def assignParticles(tree, photons, electrons, muons, taus, nu_es, nu_ms, nu_ts, ws):
    truthIDs = tree.mcPID
    for index in xrange(tree.nMC): # in Python 3.X, change xrange() to range()
        if truthIDs[index] == 22: 
            photons.append(makeParticle(tree, index))
        if abs(truthIDs[index]) == 11:
            electrons.append(makeParticle(tree, index))
        if abs(truthIDs[index]) == 13:
            muons.append(makeParticle(tree, index))
        if abs(truthIDs[index]) == 15:
            taus.append(makeParticle(tree, index))
        if abs(truthIDs[index]) == 12:
            nu_es.append(makeParticle(tree, index))
        if abs(truthIDs[index]) == 14:
            nu_ms.append(makeParticle(tree, index))
        if abs(truthIDs[index]) == 16:
            nu_ts.append(makeParticle(tree, index))
        if abs(truthIDs[index]) == 24:
            ws.append(makeParticle(tree, index))

#Not currently in use:
def assignParticlesByIndex(tree, photons, electrons, muons, nu_es, nu_ms, ws):
    truthIDs = tree.mcPID
    for index in xrange(tree.nMC):
        if     truthIDs[index]  == 22: photons.append(index)
        if abs(truthIDs[index]) == 11: electrons.append(index)
        if abs(truthIDs[index]) == 13: muons.append(index)
        if abs(truthIDs[index]) == 12: nu_es.append(index)
        if abs(truthIDs[index]) == 14: nu_ms.append(index) 
        if abs(truthIDs[index]) == 24: ws.append(index)

# Make particle TLorentz Vector
def makeTL(tree, index):
    particleFourVector = TLorentzVector()
    particleFourVector.SetPtEtaPhiE(tree.mcPt[index], tree.mcEta[index],
                          tree.mcPhi[index],tree.mcE[index])
    return particleFourVector

# Create particle class incorporating TLorentz Vector and any needed Monte Carlo vars
def makeParticle(tree, index):
    # ParticleData is a local subclass of TLorentzVector,
    # able to store additional Monte Carlo variables
    particleFourVector = particleDataClass.particleData()
    particleFourVector.SetPtEtaPhiE(tree.mcPt[index], tree.mcEta[index],
                          tree.mcPhi[index],tree.mcE[index])
    particleFourVector.SetMomPID(tree.mcMomPID[index]) 
    particleFourVector.SetGMomPID(tree.mcGMomPID[index]) 
    particleFourVector.SetStatus(tree.mcStatus[index]) 
       
    return particleFourVector


def DressedLepton(photons, electrons, muons, taus):
    for photon in photons:
        for electron in electrons:
            M = (electron + photon).M()
            if abs(M - zMass) < 5: return False
