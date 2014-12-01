"""Particle Data Class - A class that can store TLorentzVectors, plus mc variables"""

# Python Class of a TLorentzVector with extra attributes for data storage
# Subclass of ROOT.TLorentzVector
# Created by Nicholas Zube, 8.22.2014
# Tested in Python 2.6.4

from ROOT import TLorentzVector

class particleData(TLorentzVector):

    def __init__(self):
        super(particleData, self).__init__()
        self.sPID = 0
        self.sMomPID = 0
        self.sGMomPID = 0
        self.status = 0

    def GMomPID(self):
        return self.sGMomPID

    def MomPID(self):
        return self.sMomPID
                
    def PID(self):
        return self.sPID
    
    def Status(self):
        return self.status
                
    def SetGMomPID(self, iGMomPID):
        self.sGMomPID = iGMomPID

    def SetMomPID(self, iMomPID):
        self.sMomPID = iMomPID

    def SetPID(self, iPID):
        self.sPID = iPID
        
    def SetStatus(self, iStatus):
        self.status = iStatus
