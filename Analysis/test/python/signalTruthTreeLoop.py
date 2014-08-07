from ROOT import gSystem
from ROOT import TFile
from ROOT import TTree
from ROOT import TDirectory, gDirectory
from ROOT import TLorentzVector
from ROOT import TH1F, TH2F
from ROOT import TBranchElement
from math import sqrt, cos

#
# Define File Locations and Names
#

#Working Directory Location
workDirLoc = '/home/cranelli/WGamGam/Anomolous_QGC/CMSSW_5_3_12/src/Anomolous_QGC/Analysis/'
inRootFileDir = '/data/users/cranelli/WGamGam/SignalTruth'
inRootFileName = "/signaltruth_job_summer12_WAA_ISR.root"
#prefix = "SM_"
treeLoc = "ggNtuplizer/EventTree"

#gSystem.Load( 'TRootLHEFParticle_C')
#from ROOT import TRootLHEFParticle

#gSystem.Load( 'ExRootClasses_cc.so')
#from ROOT import TSortableObject
#from ROOT import TRootLHEFEvent
#from ROOT import TRootLHEFParticle

#
# Begining of Analysis Code
#
def signalTruthTreeLoop():

    inRootFileLoc = inRootFileDir + inRootFileName
    inRootFile = TFile(inRootFileLoc, "READ")
    # Set Histograms
    h1PhoLeadPt = TH1F("h1PhoLeadPt","Lead Photon Pt", 400, 0, 200)
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
        
        # num_particles = analysis_tree.Particle.GetEntries()

        #Will be filled with TLorentz Vector, for now.
        photons = []
        electrons = []
        muons = []
        leptons = []
        nu_es = []
        nu_ms = []
        nus = []
        ws = []
        
        
        # for particleIndex in xrange(num_particles):
        truthIDs = analysis_tree.mcPID
        # truthPts = analysis_tree.mcPt
        # truthEtas = analysis_tree.mcEta
        # truthPhis = analysis_tree.mcPhi
        # truthEs = analysis_tree.mcE
        # numberParticles = analysis_tree.nMC
        for index in xrange(analysis_tree.nMC):
            # print truthIDs[index]
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
            
        leadPhoton = selectLead(photons)
        lepton = selectLead(leptons) # Have signal electron be the one with highest Pt 
        nu = selectLead(nus)
        subPhoton = selectSub(photons)

        if leadPhoton != None : h1PhoLeadPt.Fill(leadPhoton.Pt())

        if leadPhoton != None and subPhoton != None and lepton != None and nu != None:
            m3 = (leadPhoton + lepton + nu).M() #Does not include sub leading lepton
            m4 = (leadPhoton + subPhoton + lepton +nu).M()
            h2M3M4.Fill(m3, m4)

                         
    outRootFile = TFile("signalTruthISRTreeLoop.root", 'RECREATE')
    outRootFile.cd()
    # outRootFile.Write #Does not seem to have anything in memmory.
    # h1PhoLeadPt.Draw()
    h1PhoLeadPt.Write()
    h2M3M4.Write()
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
    signalTruthTreeLoop()

"""
        

        #Check Parentage
        print "Particle: ", particle.PID
        print "Particle's MothUp Index: ", particle.Mother1
        if(particle.Mother1 != 0):
            print "Particle's Mother: ", particles[particle.Mother1 -1].PID
        #print "Particle's Mother: ", particles[particle.Mother1]

    #
    # Analyze Photons
    #
    # print photonPts
    
    is_DoubleISR = False
    is_DoubleFSR = False
    is_QGC = False
    is_TGCISR = False
    is_TGCFSR = False
    is_ISRFSR = False

    #photonMothers = [] #Collection of First Mother Particles
    #for photon in photons:
        #photonMothers.append(particles[photon.Mother1 -1])  #Minus 1 Needed, since 0 is no photon
        #print "Photon's First Mother ", particles[photon.Mother1].PID

    # Double FSR
    #if abs(photonMothers[0].PID) == 11 or abs(photonMothers[0].PID) == 13:
        #print "Mother's mother: ", photonMothers[0].PID
    
    #print "Photon's First Mother: ", particles[photons[0].Mother1].PID 
    #print "Photon's Last Mother: ", particles[photons[0].Mother2].PID

    photonPts = []
    for photon in photons:
        
        photonPts.append(photon.PT)
        
    # Make Histogram of Lead Photon Pt
    h1PhoLeadPt.Fill(max(photonPts))
    #print event.Weight;
    h1PhoLeadPtWeighted.Fill(max(photonPts), weight);

    #
    # Analyze Leptons and Neutrinos
    #
    lepLV = TLorentzVector(lep.Px, lep.Py, lep.Pz, lep.E)
    nuLV = TLorentzVector(nu.Px, nu.Py, nu.Pz, nu.E)
    Mt2 = 2*lepLV.Et()*nuLV.Et()*(1-cos(lepLV.DeltaPhi(nuLV)))
    Mt = sqrt(Mt2)
    h1Mt.Fill(Mt, weight)

"""
    


