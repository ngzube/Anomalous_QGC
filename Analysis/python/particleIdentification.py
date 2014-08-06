"""Particle Identification - Assigns Particles From a Tree and Stores Them"""

# Python Module For Particle Identification
# Created by Christopher Anelli
# 8.6.2014

from ROOT import TTree
from ROOT import TLorentzVector

import histogramBuilder

def assignParticles(tree, photons, electrons, muons, nu_es, nu_ms, ws):
    truthIDs = tree.mcPID
    for index in xrange(tree.nMC):
        if truthIDs[index] == 22: photons.append(makeTL(tree, index))
        # if particle.PID == 11 or particle.PID == -11: print particle.PID; print "lepton"
        if abs(truthIDs[index]) == 11:
            electrons.append(makeTL(tree, index))
            #leptons.append(makeTL(tree, index))
        if abs(truthIDs[index]) == 13:
            muons.append(makeTL(tree, index))
            #leptons.append(makeTL(tree, index))
        if abs(truthIDs[index]) == 12:
            nu_es.append(makeTL(tree, index))
            #nus.append(makeTL(tree, index))
        if abs(truthIDs[index]) == 14:
            nu_ms.append(makeTL(tree, index))
            #nus.append(makeTL(tree, index))
        if abs(truthIDs[index]) == 24:
            ws.append(makeTL(tree, index))

        # Alternative Method, just storing the location index, not building the Lorentz Vector
        """
        if truthIDs[index] == 22: photons.append(index)
        if abs(truthIDs[index]) == 11: electrons.append(index); leptons.append(index)
        if abs(truthIDs[index]) == 13: muons.append(index); leptons.append(index)
        if abs(truthIDs[index]) == 12: nu_es.append(index); nus.append(index)
        if abs(truthIDs[index]) ==14: nu_ms.append(index); nus.append(index)
        if abs(truthIDs[index]) == 24: ws.append( index)
        """

def makeTL(tree, index):
    particleFourVector = TLorentzVector()
    # Define TLorentz Vector
    particleFourVector.SetPtEtaPhiE(tree.mcPt[index], tree.mcEta[index],
                          tree.mcPhi[index],tree.mcE[index])
    return particleFourVector
