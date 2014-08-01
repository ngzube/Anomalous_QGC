#define MyClass_cxx
#include "MyClass.h"


// ParticleID checking functions. Given an integer(s), return whether 
// it matches a particle ID tag or radiation type.

bool QGC(int p1, int p2){
	if((isW(p1))&&(isW(p2))) return true;
	else return false;
}

bool FSR(int p1, int p2){
	if( ( (isLep(p1))||(isNu(p1)) ) && ( (isLep(p2))||(isNu(p2)) ) ) return true;
	else return false;
}

bool ISR(int p1, int p2){
	if(((isW(p1)==false)&&(isLep(p1)==false)&&(isNu(p1)==false))&&
		((isW(p2)==false)&&(isLep(p2)==false)&&(isNu(p2)==false))) return true;
	else return false;
}

bool isLep(int a){
	int aPID = abs(a);
	if ((aPID==11)||(aPID==13)) return true;
	else return false;
}

bool isMu(int a){
	int aPID = abs(a);
	if (aPID==13) return true;
	else return false;
}

bool isNu(int a){
	int aPID = abs(a);
	if ((aPID==12)||(aPID==14)) return true;
	else return false;
}

bool isW(int a){ 
	int aPID = abs(a);
	if (aPID==24) return true;
	else return false;
}

bool isPhoton(int a){ 
	int aPID = abs(a);
	if (aPID==22) return true;
	else return false;
}

bool passesSelection(TLorentzVector photon1, TLorentzVector photon2, 
	TLorentzVector lepton, char leptonType, int StopAtStep = 12,
	bool xclusive = false;) {

/*bool passesSelection(Double_t p1pt, Double_t p2pt, Double_t lpt,
	Double_t p1eta, Double_t p2eta, Double_t leta){
*/
	// Checks if three TLorentz vectors for a given event pass the defined 
	// selection cuts. Assigning a value to StopAtStep allows the user to 
	// only check up to a certain step of selection cuts. Without a StopAtStep 
	// assigned, it will perform all cut checks.
	
	Double_t pPT_min = 15;
	Double_t ePT_min = 30;
	Double_t mPT_min = 25;
	Double_t pEta_max = 2.5;
	Double_t pEta_exclude_lo = 1.47;
	Double_t pEta_exclude_hi = 1.57;
	Double_t eEta_max = 2.5;
	Double_t mEta_max = 2.4;
	Double_t ppDeltaR_min = 0.4;
	Double_t LpDeltaR_min = 0.3;

	int currentStep = 0;

	if(StopAtStep>12 || StopAtStep<0){
		printf("Argument StopAtStep = %d for function passesSelection is out of range (0-12)\n", 
			StopAtStep);
		break;
	}

	if(leptonType != 'e' && leptonType != 'm'){
		printf("Argument leptonType = \"%c\" for function passesSelection is not valid\n",
			leptonType);
		break;
	}

	//Step 0: No cut
	if(StopAtStep==0) return true;
	currentStep++;

	//Step 1: Leading photon PT cut
	if(photon1.Pt()>pPT_min){
		if(StopAtStep == currentStep) return true; 
	}
	else return false;
	currentStep++;
		
	//Step 2: 2nd photon PT cut
	if(photon2.Pt()>pPT_min){ 
		if(StopAtStep == currentStep) return true; 
	}
	else return false;
	currentStep++;
		
	//Step 3: Leading photon Eta cut
	if( (abs(photon1.Eta())<pEta_max) && (((abs(photon1.Eta())<pEta_exclude_lo) || 
		(abs(photon1.Eta())>pEta_exclude_hi))) ){ 
		if(StopAtStep == currentStep) return true; 
	}
	else return false;
	currentStep++;
		
	//Step 4: 2nd photon Eta cut
	if( (abs(photon2.Eta())<pEta_max) && (((abs(photon2.Eta())<pEta_exclude_lo) || 
		(abs(photon2.Eta())>pEta_exclude_hi))) ){ 
		if(StopAtStep == currentStep) return true; 
	}
	else return false;
	currentStep++;

	//Step 5: DeltaR photon-photon cut
	if((photon1.DeltaR(photon2)>ppDeltaR_min)){
		if(StopAtStep == currentStep) return true; 
	}
	else return false;
	currentStep++;

	//Step 6: DeltaR photon1-lepton cut
	if((lepton.DeltaR(photon1)>LpDeltaR_min)){
		if(StopAtStep == currentStep) return true; 
	}
	else return false;
	currentStep++;

	//Step 7: DeltaR photon2-lepton cut
	if((lepton.DeltaR(photon2)>LpDeltaR_min)){
		if(StopAtStep == currentStep) return true; 
	}
	else return false;
	currentStep++;

	//Step 8 (8e): Electron PT cut
	if(leptonType == 'e'){
		if(lepton.Pt()>ePT_min){
			if(StopAtStep == currentStep) return true; 
		}
		else if(StopAtStep >= currentStep) return false;
	}
	currentStep++;

	//Step 9 (9e): Electron Eta cut
	if(leptonType == 'e'){
		if(lepton.Eta()<eEta_max){
			if(StopAtStep == currentStep) return true; 
		}
		else if(StopAtStep >= currentStep) return false;
	}
	currentStep++;

	//Step 10 (8m): Muon PT cut
	if(leptonType == 'm'){
		if(lepton.Pt()>mPT_min){
			if(StopAtStep == currentStep) return true; 
		}
		else if(StopAtStep >= currentStep) return false;
	}
	currentStep++;

	//Step 11 (9m): Muon Eta cut
	if(leptonType == 'm'){
		if(lepton.Eta()<mEta_max){
			if(StopAtStep == currentStep) return true; 
		}
		else if(StopAtStep >= currentStep) return false;
	}
	currentStep++;

	// If all cuts are passed and StopAtStep has not already triggered a return, 
	// the event passes selection and returns true
	return true;
}





void MyClass::Loop(int sel=0) {

//   In a ROOT session, you can do:
//      Root > .L MyClass.C
//      Root > MyClass t
//      Root > t.GetEntry(12); // Fill t data members with entry number 12
//      Root > t.Show();       // Show values of entry 12
//      Root > t.Show(16);     // Read and show values of entry 16
//      Root > t.Loop();       // Loop on all entries

//   Histogram declarations
//   All particles:

/*	TH1F *hPID = new TH1F("hPID", "Wgg generator: Counts of particle ID's;PID",54,-27,27);
	TH1F *hPIDw = new TH1F("hPIDw", "Wgg generator: Counts of particle ID's, weighted;PID",54,-27,27);
	TH1F *hPT = new TH1F("hPT", "Wgg generator: Counts of particle pt;PT (GeV)", 30, 0, 100);
	TH1F *hPTw = new TH1F("hPTw", "Wgg generator: Counts of particle pt, weighted;PT (GeV)", 30, 0, 100);
*/
//	Photons
	TH1F *hphotonPT = new TH1F("hphotonPT", "Wgg generator: Counts of photon pt;PT (GeV)", 30, 0, 100);
	TH1F *hphotonPTw = new TH1F("hphotonPTw", "Wgg generator: Counts of photon pt, weighted;PT (GeV)", 30, 0, 100);

	// Selection hists
	TH1F *hp1pt = new TH1F("hp1pt", "Counts of leading photon pt;PT (GeV)", 100, 0, 100);
	TH1F *hp1ptw = new TH1F("hp1ptw", "Counts of leading photon pt, weighted;PT (GeV)", 100, 0, 100);
	TH1F *hp2pt = new TH1F("hp2pt", "Counts of 2nd photon pt;PT (GeV)", 100, 0, 100);
	TH1F *hp2ptw = new TH1F("hp2ptw", "Counts of 2nd photon pt, weighted;PT (GeV)", 100, 0, 100);
	TH1F *hp1eta = new TH1F("hp1Eta", "Wgg generator: Counts of 1st photon eta", 100, -3, 3);
	TH1F *hp2eta = new TH1F("hp2Eta", "Wgg generator: Counts of 2nd photon eta", 100, -3, 3);

	TH1F *hePT = new TH1F("hePT", "Wgg generator: Counts of electron pt;PT (GeV)", 100, 0, 100);
	TH1F *hePTw = new TH1F("hePTw", "Wgg generator: Counts of electron pt, weighted;PT (GeV)", 100, 0, 100);
	TH1F *heEta = new TH1F("heEta", "Wgg generator: Counts of electron eta", 100, -3, 3);
	TH1F *hePEtaw = new TH1F("heEtaw", "Wgg generator: Counts of electron eta, weighted", 100, -3, 3);
	TH1F *hmPT = new TH1F("hmPT", "Wgg generator: Counts of muon pt;PT (GeV)", 100, 0, 100);
	TH1F *hmPTw = new TH1F("hmPTw", "Wgg generator: Counts of muon pt, weighted;PT (GeV)", 100, 0, 100);
	TH1F *hmEta = new TH1F("hmEta", "Wgg generator: Counts of muon eta", 100, -3, 3);
	TH1F *hmPEtaw = new TH1F("hmEtaw", "Wgg generator: Counts of muon eta, weighted", 100, -3, 3);

	TH1F *hdRpp = new TH1F("hdRpp", "Wgg generator: Counts of DeltaR A-A", 100, 0, 6);
	TH1F *hdRlp1 = new TH1F("hdRlp1", "Wgg generator: Counts of DeltaR L-A1", 100, 0, 6);
	TH1F *hdRlp2 = new TH1F("hdRlp2", "Wgg generator: Counts of DeltaR L-A2", 100, 0, 6);



/*
	THStack *hsPPT = new THStack("hsPPT","PT of leading and 2nd photons");
	THStack *hsPPTw = new THStack("hsPPTw","PT of leading and 2nd photons, weighted");

	TH1F *hparent = new TH1F("hparent", "Wgg generator: Counts of particle ID's of photon mother1;PID",100,-50,50);
	TH1F *hparent2 = new TH1F("hparent2", "Wgg generator: Counts of particle ID's of photon mother2;PID",54,-27,27);
	THStack *hsP = new THStack("hsP","Parent1 & 2 of photons");
	THStack *hsPw = new THStack("hsPw","Parent1 & 2 of photons, weighted");

// Leptons

//	Mass
	TH1F *hM = new TH1F("hM", "Wgg generator: Counts of L-Nu mass;Mass (GeV)", 30, 0, 180);
	TH1F *hMw = new TH1F("hMw", "Wgg generator: Counts of L-Nu mass, weighted;Mass (GeV)", 30, 0, 180);
	TH1F *hWM = new TH1F("hWM", "Wgg generator: Counts of W mass;Mass (GeV)", 50, 60, 110);
	TH1F *hWMw = new TH1F("hWMw", "Wgg generator: Counts of W mass, weighted;Mass (GeV)", 50, 60, 110);

//  MT
	TH1F *hMT2 = new TH1F("hMT2", "Wgg generator: Counts of L-Nu transverse mass;MT (GeV)", 30, 0, 150);
	TH1F *hMT2w = new TH1F("hMT2w", "Wgg generator: Counts of L-Nu transverse mass, weighted;MT (GeV)", 30, 0, 150);
	TH1F *hMT2q = new TH1F("hMT2q", "Wgg generator: Counts of QGC L-Nu transverse mass;MT (GeV)", 30, 0, 150);
	TH1F *hMT2qw = new TH1F("hMT2qw", "Wgg generator: Counts of QGC L-Nu transverse mass, weighted;MT (GeV)", 30, 0, 150);
	TH1F *hMT2f = new TH1F("hMT2f", "Wgg generator: Counts of FSR L-Nu transverse mass;MT (GeV)", 30, 0, 150);
	TH1F *hMT2fw = new TH1F("hMT2fw", "Wgg generator: Counts of FSR L-Nu transverse mass, weighted;MT (GeV)", 30, 0, 150);
	TH1F *hMT2i = new TH1F("hMT2i", "Wgg generator: Counts of ISR L-Nu transverse mass;MT (GeV)", 30, 0, 150);
	TH1F *hMT2iw = new TH1F("hMT2iw", "Wgg generator: Counts of ISR L-Nu transverse mass, weighted;MT (GeV)", 30, 0, 150);
	TH1F *hMT2m = new TH1F("hMT2m", "Wgg generator: Counts of mixed L-Nu transverse mass;MT (GeV)", 30, 0, 150);
	TH1F *hMT2mw = new TH1F("hMT2mw", "Wgg generator: Counts of mixed L-Nu transverse mass, weighted;MT (GeV)", 30, 0, 150);
	THStack *hsMT = new THStack("hsMT","Wgg generator: Counts of mixed radiation type L-Nu transverse mass");
	
	TH1F *hMTg = new TH1F("hMTg", "Wgg generator: Counts of LA-Nu transverse mass;MT (GeV)", 30, 0, 180);
	TH1F *hMTgw = new TH1F("hMTgw", "Wgg generator: Counts of LA-Nu transverse mass, weighted;MT (GeV)", 30, 0, 180);
*/

	Int_t partCount, p6count = 0;	// counters and flags for particles
	Int_t p1Ind, p2Ind, lepInd, nuInd, wInd;	// indicies for particular particles in an event
	int p1m1, p1m2, p2m1, p2m2 = 0;		// variables distingiushing leading and 2nd photons
	int qgcC, fsrC, isrC, qgc_flag, fsr_flag, isr_flag = 0;  // counters and flags for radiation types
	double acceptance = 0.0;	// acceptance = # of events passing selection /  total # of events
	double acceptanceE = 0.0;
	double acceptanceM = 0.0;
	bool mu_flag = false;		// flag for muon in event
	bool missingW_flag = false;
	bool firstPhoton = true;
	char lepType = 'e';
	int muCount, eCount = 0;
	TLorentzVector TLlep, TLnu, TLp1, TLp2, TLw, TLsum, TLlep_g;	//TLorentz 4-vectors
	Double_t Pdot, MT, MT1, MT2, M, M2, MTg = 0;	// mass calculations
	Double_t EventWeight = 0;

	Double_t p1ptmin = 10000.0;
	Double_t p2ptmin = 10000.0;
	Double_t ppdrmin = 10000.0;
	Double_t lp1drmin = 10000.0;
	Double_t lp2drmin = 10000.0;
	Double_t eptmin = 10000.0;
	Double_t mptmin = 10000.0;
	Double_t p1etamax = 0.0;
	Double_t p2etamax = 0.0;
	Double_t eetamax = 0.0;
	Double_t metamax = 0.0;

//  This is the loop skeleton where:
//    jentry is the global entry number in the chain
//    ientry is the entry number in the current Tree
//  Note that the argument to GetEntry must be:
//    jentry for TChain::GetEntry
//    ientry for TTree::GetEntry and TBranch::GetEntry
//
//  To read only selected branches, Insert statements like:
// METHOD1:
//    fChain->SetBranchStatus("*",0);  // disable all branches
//    fChain->SetBranchStatus("branchname",1);  // activate branchname
// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch

	if (fChain == 0) return;
	Long64_t nentries = fChain->GetEntriesFast();
	//cout << "\nEvents: " << nentries << endl;
	Long64_t nbytes = 0, nb = 0;
  
	for (Long64_t jentry=0; jentry<nentries;jentry++) {	//Loop through Events
		Long64_t ientry = LoadTree(jentry);
		if (ientry < 0) break;	// if (Cut(ientry) < 0) continue;
		nb = fChain->GetEntry(jentry);   nbytes += nb;

		if (Event_Nparticles[0]==6) {
			p6count++; 
			missingW_flag = true;
		}
		EventWeight = Event_Weight[0];	//Store weight for histogram filling		
		
		for(Int_t j1=0; j1<Event_Nparticles[0]; j1++){	//Loop through Particles in an Event
			
			partCount++;
/*			hPID->Fill(Particle_PID[j1]);	hPIDw->Fill(Particle_PID[j1],EventWeight); 
			hPT->Fill(Particle_PT[j1]);		hPTw->Fill(Particle_PT[j1],EventWeight);
*/
			//Identifying leading and 2nd photons
			if(isPhoton(Particle_PID[j1])){		
				//hphotonPT->Fill(Particle_PT[j1]);	hphotonPTw->Fill(Particle_PT[j1],EventWeight);			
				if(firstPhoton){
					firstPhoton = false;  //1st photon has been found; flag off

					for(Int_t j2=0; j2<Event_Nparticles[0]; j2++){	//Look for second photon
				    
						if((isPhoton(Particle_PID[j2])) && (j2!=j1)){
							//Larger PT into hp1pt; smaller in hp2pt
							p1Ind = j1; p2Ind = j2;
							if(Particle_PT[p2Ind]>Particle_PT[p1Ind]){ p2Ind = j1; p1Ind = j2;}
							TLp1.SetPxPyPzE(Particle_Px[p1Ind],Particle_Py[p1Ind],Particle_Pz[p1Ind],Particle_E[p1Ind]);
							TLp2.SetPxPyPzE(Particle_Px[p2Ind],Particle_Py[p2Ind],Particle_Pz[p2Ind],Particle_E[p2Ind]);

						} //If 2nd particle is a unique photon
					}//Loop through event, finding 2nd photon
				}//If this is the first photon in an event
			}//If particle is photon
			
			if(isLep(Particle_PID[j1])){
				lepInd = j1;
				TLlep.SetPxPyPzE(Particle_Px[lepInd],Particle_Py[lepInd],Particle_Pz[lepInd],Particle_E[lepInd]);
				if(isMu(Particle_PID[lepInd])) {
					mu_flag = true;
					lepType = 'm';
					muCount++;
				}
				else eCount++;
			}
			if(isNu(Particle_PID[j1])){
				nuInd = j1;
				TLnu.SetPxPyPzE(Particle_Px[nuInd],Particle_Py[nuInd],Particle_Pz[nuInd],Particle_E[nuInd]);
			}
			if(isW(Particle_PID[j1])){
				wInd = j1;
				TLw.SetPxPyPzE(Particle_Px[wInd],Particle_Py[wInd],Particle_Pz[wInd],Particle_E[wInd]);
			}

		}//Loop through Particles in an Event

/*		// Find mins and maxes before selection cuts
		if(p1ptmin>Particle_PT[p1Ind]) p1ptmin = Particle_PT[p1Ind];
		if(p2ptmin>Particle_PT[p2Ind]) p2ptmin = Particle_PT[p2Ind];
		if(ppdrmin>TLp1.DeltaR(TLp2)) ppdrmin = TLp1.DeltaR(TLp2);
		if(lp1drmin>TLp1.DeltaR(TLlep)) lp1drmin = TLp1.DeltaR(TLlep);
		if(lp2drmin>TLp2.DeltaR(TLlep)) lp2drmin = TLp2.DeltaR(TLlep);
		if(eptmin>Particle_PT[lepInd] && lepType == 'e') eptmin = Particle_PT[lepInd];
		if(mptmin>Particle_PT[lepInd] && lepType == 'm') mptmin = Particle_PT[lepInd];

		if(p1etamax<Particle_Eta[p1Ind]) p1etamax = Particle_Eta[p1Ind];
		if(p2etamax<Particle_Eta[p2Ind]) p2etamax = Particle_Eta[p2Ind];
		if(eetamax<Particle_Eta[lepInd] && lepType == 'e') eetamax = Particle_Eta[lepInd];
		if(metamax<Particle_Eta[lepInd] && lepType == 'm') metamax = Particle_Eta[lepInd];
*/
		
		//if(lepType='e') {
		//if(lepType='m') {
		if(passesSelection(TLp1, TLp2, TLlep, lepType, sel)){ 
			
			acceptance = acceptance + 1.0;
			//acceptanceE = acceptanceE + 1.0;
			//acceptanceM = acceptanceM + 1.0;
		
			hp1pt->Fill(Particle_PT[p1Ind]);
			hp2pt->Fill(Particle_PT[p2Ind]);
			hp1eta->Fill(Particle_Eta[p1Ind]);
			hp2eta->Fill(Particle_Eta[p2Ind]);
			
			if(lepType == 'e') {
				hePT->Fill(Particle_PT[lepInd]);
				heEta->Fill(Particle_Eta[lepInd]);
			}
			else if(lepType == 'm'){
				hmPT->Fill(Particle_PT[lepInd]);
				hmEta->Fill(Particle_Eta[lepInd]);
			}

			hdRpp->Fill(TLp1.DeltaR(TLp2));
			hdRlp1->Fill(TLp1.DeltaR(TLlep));
			hdRlp2->Fill(TLp2.DeltaR(TLlep));


			/*
			hp1pt->Fill(Particle_PT[p1Ind]);	hp1ptw->Fill(Particle_PT[p1Ind],EventWeight); 
			hp2pt->Fill(Particle_PT[p2Ind]);	hp2ptw->Fill(Particle_PT[p2Ind],EventWeight);
							
			p1m1 = Particle_Mother1[p1Ind]; p2m1 = Particle_Mother1[p2Ind];
			p1m2 = Particle_Mother2[p1Ind]; p2m2 = Particle_Mother2[p2Ind];

			//if((Particle_PID[p1m1-1]>=10)&&(Particle_PID[p1m1-1]<20)){cout<<endl<<"WEIRDNESS at event "<<jentry<<"!"<<endl;	}
			if(p1m1>0){hparent->Fill(Particle_PID[p1m1-1]);}
			if(p2m1>0){hparent->Fill(Particle_PID[p2m1-1]);}							
			if((p1m2>0)&&(p1m2!=p1m1)){hparent2->Fill(Particle_PID[p1m2-1]);}
			if((p2m2>0)&&(p2m2!=p2m1)){hparent2->Fill(Particle_PID[p2m2-1]);}

			if(QGC(Particle_PID[p1m1-1],Particle_PID[p2m1-1])){
				qgcC++; qgc_flag=1;
			}
			else if(ISR(Particle_PID[p1m1-1],Particle_PID[p2m1-1])){
				isrC++; isr_flag=1;
			}
			else if(FSR(Particle_PID[p1m1-1],Particle_PID[p2m1-1])){
				fsrC++; fsr_flag=1;
			}
			else {
								
			}
			*/
		}// Acceptance cuts

		//}// E-mu channel cut

		/*

		//if(TLlep!=null && TLnu!=null) // do the Lepton-Neutrino calculations:
		TLsum = TLlep + TLnu;
		Pdot = TLlep.Vect() * TLnu.Vect();
		M = sqrt(pow(TLsum.E(),2)-Pdot);	//Mass
		hM->Fill(M); hMw->Fill(M,EventWeight);

		//M2 = TLlep.M() + TLnu.M();		//Wrong calculation for mass
		//MT1 = sqrt(pow(TLlep.Et()+TLnu.Et(),2) - pow(TLsum.Pt(),2)); //alternate calc method
		//hM2->Fill(M2);
 		//hMT1->Fill(MT1); 

		MT2 = sqrt(2*TLlep.Et()*TLnu.Et()* (1-cos(TLlep.DeltaPhi(TLnu)))); //L-Nu MT calculation
		hMT2->Fill(MT2); hMT2w->Fill(MT2,EventWeight);

		if(qgc_flag==1){hMT2q->Fill(MT2); hMT2qw->Fill(MT2,EventWeight);}
		else if(fsr_flag==1){hMT2f->Fill(MT2); hMT2fw->Fill(MT2,EventWeight);}
		else if(isr_flag==1){hMT2i->Fill(MT2); hMT2iw->Fill(MT2,EventWeight);}
		else {hMT2m->Fill(MT2); hMT2mw->Fill(MT2,EventWeight);}

		TLlep_g = TLlep + TLp1;
		MTg = sqrt(2*TLlep_g.Et()*TLnu.Et()* (1-cos(TLlep_g.DeltaPhi(TLnu))));	//(LA)-Nu MT calculation
		hMTg->Fill(MTg); hMTgw->Fill(MTg,EventWeight);
		hWM->Fill(TLw.M()); hWMw->Fill(TLw.M(),EventWeight);

		*/


		firstPhoton = true; //reset flags
		MT=MT1=MT2=M=M2=MTg=0;
		qgc_flag = fsr_flag = isr_flag = 0;
		mu_flag = missingW_flag = false;
		lepType = 'e';

	}//Loop through events
	
/*	cout << "Particles: " << partCount << endl;
	cout<<"Six particle events: "<<p6count<<endl;
	cout<<"QGC events: "<<qgcC<<endl;
	cout<<"FSR events: "<<fsrC<<endl;
	cout<<"ISR events: "<<isrC<<endl;
	cout<<"Mixed events: "<<(nentries-qgcC-fsrC-isrC)<<endl;
*/	cout<<"Acceptance (# passed truth cuts / total events): "<<acceptance/nentries<<endl;
	//cout<<"Events w/ e: "<<eCount<<" Events with mu: "<<muCount<<endl;
	//cout<<"e acceptance: "<<acceptanceE/eCount<<endl;
	//cout<<"mu acceptance: "<<acceptanceM/muCount<<endl;

/*	cout<<"p1PTmin: "<<p1ptmin<<"  p2PTmin: "<<p2ptmin<<"  ppDRmin: "<<ppdrmin<<endl;
	cout<<"lp1DRmin: "<<lp1drmin<<"lp2DRmin: "<<lp2drmin<<" ePTmin: "<<eptmin<<endl;
	cout<<"mPTmin: "<<mptmin<<" p1Etamax: "<<p1etamax<<" p2Etamax: "<<p2etamax<<endl;
	cout<<"eEtamax: "<<eetamax<<" mEtamax: "<<metamax<<endl;
*/

 /*
  	//Plot all histograms on a large canvas
	TCanvas *MyC = new TCanvas("MyC","test canvas",1);
	hPID->Draw();
	MyC->Print("/home/nzube/CMSSW_5_3_19/src/pid.png");
	hPT->Draw();
	MyC->Print("/home/nzube/CMSSW_5_3_19/src/pt.png");
	hphotonPT->Draw();
	MyC->Print("/home/nzube/CMSSW_5_3_19/src/ppt.png");
	hM->Draw();
	MyC->Print("/home/nzube/CMSSW_5_3_19/src/m.png");
   	hp1pt->SetLineColor(2);
   	hp2pt->SetTitle("Wgg generator: Combined photon pair PT");
  	hp2pt->Draw(); hp1pt->Draw("same");
   	TLegend *MyL = new TLegend(0.63,0.65,0.89,0.72);
   	MyL->AddEntry(hp1pt,"Leading photons","l");
   	MyL->AddEntry(hp2pt,"Secondary photons","l");
   	MyL->SetTextSize(0.025);
   	MyL->Draw();
	MyC->Print("/home/nzube/CMSSW_5_3_19/src/ppt2.png");
	hMT2->Draw();
	MyC->Print("/home/nzube/CMSSW_5_3_19/src/mt.png");
	hMT->Draw();
	MyC->Print("/home/nzube/CMSSW_5_3_19/src/mt2.png");

	MyC->Divide(2,2);
	MyC->cd(1); hPID->Draw();
	MyC->cd(2); hPT->Draw();
	MyC->cd(3); hphotonPT->Draw();
   
	hp1pt->SetLineColor(2);
	hp2pt->SetTitle("Combined photon pair PT");
	MyC->cd(4);
	hp2pt->Draw(); hp1pt->Draw("same");

	//THStack *hs = new THStack("hs","test stacked histograms");
	//hs->Add(hp1pt); hs->Add(hp2pt);
	//MyC->cd(6); hs->Draw("nostack"); 

	TLegend *MyL = new TLegend(0.63,0.65,0.89,0.72);
	//MyL->SetHeader("Legend");
	MyL->AddEntry(hp1pt,"Leading photons","l");
	MyL->AddEntry(hp2pt,"Secondary photons","l");
	MyL->SetTextSize(0.025);
	MyL->Draw();
  
	TCanvas *MyC2 = new TCanvas("MyC2","test canvas",1);
	MyC->Divide(1,2);
	MyC->cd(1); hM->Draw();
	MyC->cd(2); hMT->Draw();
  
	MyC1->Print("/home/nzube/CMSSW_5_3_19/src/MyCanvas.png");

	hparent2->SetLineColor(2);
	hsP->Add(hparent); hsP->Add(hparent2); 
*/


	TFile *t = new TFile("test.root","RECREATE");

	t->Add(hp1pt); t->Add(hp2pt); t->Add(hp1eta); t->Add(hp2eta); 
	t->Add(hePT); t->Add(hmPT); t->Add(heEta); t->Add(hmEta); 
	t->Add(hdRpp); t->Add(hdRlp1); t->Add(hdRlp2);



/*	t->Add(hPID); t->Add(hPT); t->Add(hphotonPT);
	t->Add(hPIDw); t->Add(hPTw); t->Add(hphotonPTw);

	t->Add(hp1pt); t->Add(hp2pt); t->Add(hsPPTw);
	t->Add(hM); t->Add(hMw);//t->Add(hM2);
	t->Add(hMT2); t->Add(hWM); t->Add(hMTg); //t->Add(hMT1); t->Add(hMT); 
	t->Add(hMT2w); t->Add(hWMw); t->Add(hMTgw);

	t->Add(hMT2q); t->Add(hMT2f); t->Add(hMT2i); t->Add(hMT2m); 
	t->Add(hMT2qw); t->Add(hMT2fw); t->Add(hMT2iw); t->Add(hMT2mw); 




	TCanvas *MyC = new TCanvas("MyC","test canvas",1);
	hMT2q->SetFillColor(kGreen);	hMT2q->SetMarkerStyle(21); hMT2q->SetMarkerColor(kGreen);
	hMT2m->SetFillColor(kRed);		hMT2m->SetMarkerStyle(21); hMT2m->SetMarkerColor(kRed);
	hMT2i->SetFillColor(kBlue);		hMT2i->SetMarkerStyle(21); hMT2i->SetMarkerColor(kBlue);
	hsMT->Add(hMT2q); hsMT->Add(hMT2m); hsMT->Add(hMT2i);
	hsMT->Draw();

	TLegend *legend=new TLegend(0.6,0.65,0.88,0.85);
	legend->SetTextFont(72);
	legend->SetTextSize(0.04);
	legend->AddEntry(hMT2q,"QGC","f");
	legend->AddEntry(hMT2i,"ISR","f");
	legend->AddEntry(hMT2m,"Mixed","f");
	legend->Draw();

	t->Add(hsMT);

	t->Add(hparent); t->Add(hparent2); t->Add(hsP); t->Add(hsPw);
*/	
	t->Write();
	t->Close();
}


/*
Old code:

	srand (time(NULL));
	int randEvent = rand() % 30000;
	int re2 = rand() % 30000;
	int re3 = rand() % 30000;


	//Show(176) = 6 particle event; Show(186)





*/