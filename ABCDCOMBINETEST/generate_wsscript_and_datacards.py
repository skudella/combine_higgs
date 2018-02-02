import sys
import os
import subprocess
import time
import datetime
import stat
import ROOT

#sys.path.append(os.path.abspath("/nfs/dust/cms/user/skudella/pyroot-plotscripts/"))
#from plot_additional_Zprime_MC import *


def GetKeyNames( self, dir = "" ):
    self.cd(dir)
    return [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
ROOT.TFile.GetKeyNames = GetKeyNames







def createCcode(pathToOutputRootFile,nbins,rebin,SignalNick,WP,systlist=[],truesig="noSignal"):

    script=""
    script+="""


#include <TH1.h>
#include <TSystem.h>
#include <TObject.h>
#include <TNamed.h>
#include <RooRealVar.h>
#include <RooArgList.h>
#include <RooWorkspace.h>
#include <RooDataHist.h>
#include <../../../../../interface/RooParametricHist.h>
#include <RooAddition.h>
#include <TFile.h>
#include <iostream>

    
void createABCDCombineWorkspaceFile_""" + SignalNick + "_" + WP + """_""" + truesig + """(){





    // As usual, load the combine library to get access to the RooParametricHist
    gSystem->Load("libHiggsAnalysisCombinedLimit.so");
    // Output file and workspace 
    TFile *fOut = new TFile("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root","RECREATE");
    RooWorkspace wspace("wspace","wspace");

    // A search in a MET tail, define MET as our variable
    RooRealVar Zprime_M("Zprime_M","m(Zp)",0,10000);
    RooArgList vars(Zprime_M);
    
    
    //TH1 data_obs_th1("data_obs_withtbt","Data observed in signal region",4,200,1000);
    TH1 * datahistoA_wtb = 0;
    TH1 * datahistoB_wtb = 0;
    TH1 * datahistoC_wtb = 0;
    TH1 * datahistoD_wtb = 0;
    TH1 * datahistoA_ntb = 0;
    TH1 * datahistoB_ntb = 0;
    TH1 * datahistoC_ntb = 0;
    TH1 * datahistoD_ntb = 0;

    
    TFile* file=TFile::Open(""" + '"' + pathToOutputRootFile + '"' + """);
    file->GetObject("DATA_""" + truesig + """_ABCD5_withtopbtag_CatA_Zprime_M_ABCD5_nominal", datahistoA_wtb);
    file->GetObject("DATA_""" + truesig + """_ABCD5_withtopbtag_CatB_Zprime_M_ABCD5_nominal", datahistoB_wtb);
    file->GetObject("DATA_""" + truesig + """_ABCD5_withtopbtag_CatC_Zprime_M_ABCD5_nominal", datahistoC_wtb);
    file->GetObject("DATA_""" + truesig + """_ABCD5_withtopbtag_CatD_Zprime_M_ABCD5_nominal", datahistoD_wtb);
    file->GetObject("DATA_""" + truesig + """_ABCD5_notopbtag_CatA_Zprime_M_ABCD5_nominal", datahistoA_ntb);
    file->GetObject("DATA_""" + truesig + """_ABCD5_notopbtag_CatB_Zprime_M_ABCD5_nominal", datahistoB_ntb);
    file->GetObject("DATA_""" + truesig + """_ABCD5_notopbtag_CatC_Zprime_M_ABCD5_nominal", datahistoC_ntb);
    file->GetObject("DATA_""" + truesig + """_ABCD5_notopbtag_CatD_Zprime_M_ABCD5_nominal", datahistoD_ntb);

    

    
    std::vector <float> Zprime_M_bins;
    for(int i=1; i<datahistoA_wtb->GetNbinsX()+1;i++){
        std::cout<<i<<std::endl;
        Zprime_M_bins.push_back(datahistoA_wtb->GetBinCenter(i));
        std::cout<<datahistoA_wtb->GetBinCenter(i)<<std::endl;
    }


 
"""

    for syst in systlist:
        #for updown in ["Up","Down"]:
            systname=syst
            #print systname
            script+="""
            
    TH1 * ttbarhistoA_wtb_""" + systname + """ = 0;
    TH1 * ttbarhistoB_wtb_""" + systname + """ = 0;
    TH1 * ttbarhistoC_wtb_""" + systname + """ = 0;
    TH1 * ttbarhistoD_wtb_""" + systname + """ = 0;
    TH1 * ttbarhistoA_ntb_""" + systname + """ = 0;
    TH1 * ttbarhistoB_ntb_""" + systname + """ = 0;
    TH1 * ttbarhistoC_ntb_""" + systname + """ = 0;
    TH1 * ttbarhistoD_ntb_""" + systname + """ = 0;
    
   
    file->GetObject("ttbar_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_""" + systname + """", ttbarhistoA_wtb_""" + systname + """);
    file->GetObject("ttbar_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """_""" + systname + """", ttbarhistoB_wtb_""" + systname + """);
    file->GetObject("ttbar_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + """_""" + systname + """", ttbarhistoC_wtb_""" + systname + """);
    file->GetObject("ttbar_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + """_""" + systname + """", ttbarhistoD_wtb_""" + systname + """);
    file->GetObject("ttbar_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_""" + systname + """", ttbarhistoA_ntb_""" + systname + """);
    file->GetObject("ttbar_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """_""" + systname + """", ttbarhistoB_ntb_""" + systname + """);
    file->GetObject("ttbar_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + """_""" + systname + """", ttbarhistoC_ntb_""" + systname + """);
    file->GetObject("ttbar_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + """_""" + systname + """", ttbarhistoD_ntb_""" + systname + """);                
            
            
    RooDataHist ttbar_histA_wtb_""" + systname + """("ttbar_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + "_" + systname + """","ttbar_""" + systname + """",vars,ttbarhistoA_wtb_""" + systname + """);
    RooDataHist ttbar_histB_wtb_""" + systname + """("ttbar_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + "_" + systname + """","ttbar_""" + systname + """",vars,ttbarhistoB_wtb_""" + systname + """);
    RooDataHist ttbar_histC_wtb_""" + systname + """("ttbar_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + "_" + systname + """","ttbar_""" + systname + """",vars,ttbarhistoC_wtb_""" + systname + """);
    RooDataHist ttbar_histD_wtb_""" + systname + """("ttbar_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + "_" + systname + """","ttbar_""" + systname + """",vars,ttbarhistoD_wtb_""" + systname + """);
    RooDataHist ttbar_histA_ntb_""" + systname + """("ttbar_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + "_" + systname + """","ttbar_""" + systname + """",vars,ttbarhistoA_ntb_""" + systname + """);
    RooDataHist ttbar_histB_ntb_""" + systname + """("ttbar_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + "_" + systname + """","ttbar_""" + systname + """",vars,ttbarhistoB_ntb_""" + systname + """);
    RooDataHist ttbar_histC_ntb_""" + systname + """("ttbar_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + "_" + systname + """","ttbar_""" + systname + """",vars,ttbarhistoC_ntb_""" + systname + """);
    RooDataHist ttbar_histD_ntb_""" + systname + """("ttbar_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + "_" + systname + """","ttbar_""" + systname + """",vars,ttbarhistoD_ntb_""" + systname + """);
    
    wspace.import(ttbar_histA_wtb_""" + systname + """);
    wspace.import(ttbar_histB_wtb_""" + systname + """);
    wspace.import(ttbar_histC_wtb_""" + systname + """);
    wspace.import(ttbar_histD_wtb_""" + systname + """);
    wspace.import(ttbar_histA_ntb_""" + systname + """);
    wspace.import(ttbar_histB_ntb_""" + systname + """);
    wspace.import(ttbar_histC_ntb_""" + systname + """);
    wspace.import(ttbar_histD_ntb_""" + systname + """);
    
    //wspace.import(*ttbarhistoA_wtb_""" + systname + """);
    //wspace.import(*ttbarhistoB_wtb_""" + systname + """);
    //wspace.import(*ttbarhistoC_wtb_""" + systname + """);
    //wspace.import(*ttbarhistoD_wtb_""" + systname + """);
    //wspace.import(*ttbarhistoA_ntb_""" + systname + """);
    //wspace.import(*ttbarhistoB_ntb_""" + systname + """);
    //wspace.import(*ttbarhistoC_ntb_""" + systname + """);
    //wspace.import(*ttbarhistoD_ntb_""" + systname + """);    
    
    
"""
            if (syst=='nominal'):
                for l in range(1,nbins+1):
                  for var in  ["Up","Down"]:
                    systname="_stat_bin"+str(l)+var
                    script+="""
    TH1 *ttbarhistoA_wtb_ttbarMC_Awtb""" + systname + """ = (TH1*)ttbarhistoA_wtb_""" + syst + """->Clone("ttbar_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + "_ttbarMC_Awtb" + systname + """"); 
    TH1 *ttbarhistoB_wtb_ttbarMC_Bwtb""" + systname + """ = (TH1*)ttbarhistoB_wtb_""" + syst + """->Clone("ttbar_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + "_ttbarMC_Bwtb" + systname + """"); 
    TH1 *ttbarhistoC_wtb_ttbarMC_Cwtb""" + systname + """ = (TH1*)ttbarhistoC_wtb_""" + syst + """->Clone("ttbar_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + "_ttbarMC_Cwtb" + systname + """"); 
    TH1 *ttbarhistoD_wtb_ttbarMC_Dwtb""" + systname + """ = (TH1*)ttbarhistoD_wtb_""" + syst + """->Clone("ttbar_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + "_ttbarMC_Dwtb" + systname + """"); 
    TH1 *ttbarhistoA_ntb_ttbarMC_Antb""" + systname + """ = (TH1*)ttbarhistoA_ntb_""" + syst + """->Clone("ttbar_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + "_ttbarMC_Antb" + systname + """"); 
    TH1 *ttbarhistoB_ntb_ttbarMC_Bntb""" + systname + """ = (TH1*)ttbarhistoB_ntb_""" + syst + """->Clone("ttbar_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + "_ttbarMC_Bntb" + systname + """"); 
    TH1 *ttbarhistoC_ntb_ttbarMC_Cntb""" + systname + """ = (TH1*)ttbarhistoC_ntb_""" + syst + """->Clone("ttbar_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + "_ttbarMC_Cntb" + systname + """"); 
    TH1 *ttbarhistoD_ntb_ttbarMC_Dntb""" + systname + """ = (TH1*)ttbarhistoD_ntb_""" + syst + """->Clone("ttbar_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + "_ttbarMC_Dntb" + systname + """"); 
"""
                    if(var=="Up"):
                     script+="""
    if(ttbarhistoA_wtb_ttbarMC_Awtb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        ttbarhistoA_wtb_ttbarMC_Awtb""" + systname + """->SetBinContent("""+str(l)+""",(ttbarhistoA_wtb_ttbarMC_Awtb""" + systname + """->GetBinContent("""+str(l)+""")+ttbarhistoA_wtb_ttbarMC_Awtb""" + systname + """->GetBinErrorUp("""+str(l)+""")));
    };
    if(ttbarhistoB_wtb_ttbarMC_Bwtb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        ttbarhistoB_wtb_ttbarMC_Bwtb""" + systname + """->SetBinContent("""+str(l)+""",(ttbarhistoB_wtb_ttbarMC_Bwtb""" + systname + """->GetBinContent("""+str(l)+""")+ttbarhistoB_wtb_ttbarMC_Bwtb""" + systname + """->GetBinErrorUp("""+str(l)+""")));
    }
    if(ttbarhistoC_wtb_ttbarMC_Cwtb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        ttbarhistoC_wtb_ttbarMC_Cwtb""" + systname + """->SetBinContent("""+str(l)+""",(ttbarhistoC_wtb_ttbarMC_Cwtb""" + systname + """->GetBinContent("""+str(l)+""")+ttbarhistoC_wtb_ttbarMC_Cwtb""" + systname + """->GetBinErrorUp("""+str(l)+""")));
    }
    if(ttbarhistoD_wtb_ttbarMC_Dwtb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        ttbarhistoD_wtb_ttbarMC_Dwtb""" + systname + """->SetBinContent("""+str(l)+""",(ttbarhistoD_wtb_ttbarMC_Dwtb""" + systname + """->GetBinContent("""+str(l)+""")+ttbarhistoD_wtb_ttbarMC_Dwtb""" + systname + """->GetBinErrorUp("""+str(l)+""")));
    }
    if(ttbarhistoA_ntb_ttbarMC_Antb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        ttbarhistoA_ntb_ttbarMC_Antb""" + systname + """->SetBinContent("""+str(l)+""",(ttbarhistoA_ntb_ttbarMC_Antb""" + systname + """->GetBinContent("""+str(l)+""")+ttbarhistoA_ntb_ttbarMC_Antb""" + systname + """->GetBinErrorUp("""+str(l)+""")));
    }
    if(ttbarhistoB_ntb_ttbarMC_Bntb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        ttbarhistoB_ntb_ttbarMC_Bntb""" + systname + """->SetBinContent("""+str(l)+""",(ttbarhistoB_ntb_ttbarMC_Bntb""" + systname + """->GetBinContent("""+str(l)+""")+ttbarhistoB_ntb_ttbarMC_Bntb""" + systname + """->GetBinErrorUp("""+str(l)+""")));
    }
    if(ttbarhistoC_ntb_ttbarMC_Cntb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        ttbarhistoC_ntb_ttbarMC_Cntb""" + systname + """->SetBinContent("""+str(l)+""",(ttbarhistoC_ntb_ttbarMC_Cntb""" + systname + """->GetBinContent("""+str(l)+""")+ttbarhistoC_ntb_ttbarMC_Cntb""" + systname + """->GetBinErrorUp("""+str(l)+""")));
    }
    if(ttbarhistoD_ntb_ttbarMC_Dntb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        ttbarhistoD_ntb_ttbarMC_Dntb""" + systname + """->SetBinContent("""+str(l)+""",(ttbarhistoD_ntb_ttbarMC_Dntb""" + systname + """->GetBinContent("""+str(l)+""")+ttbarhistoD_ntb_ttbarMC_Dntb""" + systname + """->GetBinErrorUp("""+str(l)+""")));
    }

    
"""
                    else:
                     script+="""
    if(ttbarhistoA_wtb_ttbarMC_Awtb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        ttbarhistoA_wtb_ttbarMC_Awtb""" + systname + """->SetBinContent("""+str(l)+""",(ttbarhistoA_wtb_ttbarMC_Awtb""" + systname + """->GetBinContent("""+str(l)+""")+ttbarhistoA_wtb_ttbarMC_Awtb""" + systname + """->GetBinErrorLow("""+str(l)+""")));
    };
    if(ttbarhistoB_wtb_ttbarMC_Bwtb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        ttbarhistoB_wtb_ttbarMC_Bwtb""" + systname + """->SetBinContent("""+str(l)+""",(ttbarhistoB_wtb_ttbarMC_Bwtb""" + systname + """->GetBinContent("""+str(l)+""")+ttbarhistoB_wtb_ttbarMC_Bwtb""" + systname + """->GetBinErrorLow("""+str(l)+""")));
    }
    if(ttbarhistoC_wtb_ttbarMC_Cwtb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        ttbarhistoC_wtb_ttbarMC_Cwtb""" + systname + """->SetBinContent("""+str(l)+""",(ttbarhistoC_wtb_ttbarMC_Cwtb""" + systname + """->GetBinContent("""+str(l)+""")+ttbarhistoC_wtb_ttbarMC_Cwtb""" + systname + """->GetBinErrorLow("""+str(l)+""")));
    }
    if(ttbarhistoD_wtb_ttbarMC_Dwtb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        ttbarhistoD_wtb_ttbarMC_Dwtb""" + systname + """->SetBinContent("""+str(l)+""",(ttbarhistoD_wtb_ttbarMC_Dwtb""" + systname + """->GetBinContent("""+str(l)+""")+ttbarhistoD_wtb_ttbarMC_Dwtb""" + systname + """->GetBinErrorLow("""+str(l)+""")));
    }
    if(ttbarhistoA_ntb_ttbarMC_Antb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        ttbarhistoA_ntb_ttbarMC_Antb""" + systname + """->SetBinContent("""+str(l)+""",(ttbarhistoA_ntb_ttbarMC_Antb""" + systname + """->GetBinContent("""+str(l)+""")+ttbarhistoA_ntb_ttbarMC_Antb""" + systname + """->GetBinErrorLow("""+str(l)+""")));
    }
    if(ttbarhistoB_ntb_ttbarMC_Bntb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        ttbarhistoB_ntb_ttbarMC_Bntb""" + systname + """->SetBinContent("""+str(l)+""",(ttbarhistoB_ntb_ttbarMC_Bntb""" + systname + """->GetBinContent("""+str(l)+""")+ttbarhistoB_ntb_ttbarMC_Bntb""" + systname + """->GetBinErrorLow("""+str(l)+""")));
    }
    if(ttbarhistoC_ntb_ttbarMC_Cntb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        ttbarhistoC_ntb_ttbarMC_Cntb""" + systname + """->SetBinContent("""+str(l)+""",(ttbarhistoC_ntb_ttbarMC_Cntb""" + systname + """->GetBinContent("""+str(l)+""")+ttbarhistoC_ntb_ttbarMC_Cntb""" + systname + """->GetBinErrorLow("""+str(l)+""")));
    }
    if(ttbarhistoD_ntb_ttbarMC_Dntb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        ttbarhistoD_ntb_ttbarMC_Dntb""" + systname + """->SetBinContent("""+str(l)+""",(ttbarhistoD_ntb_ttbarMC_Dntb""" + systname + """->GetBinContent("""+str(l)+""")+ttbarhistoD_ntb_ttbarMC_Dntb""" + systname + """->GetBinErrorLow("""+str(l)+""")));
    }

"""


                    script+="""
    RooDataHist ttbar_histA_wtb_ttbarMC_Awtb""" + systname + """("ttbar_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + "_ttbarMC_Awtb" + systname + """","ttbar_ttbarMC_Awtb""" + systname + """",vars,ttbarhistoA_wtb_ttbarMC_Awtb""" + systname + """);
    RooDataHist ttbar_histB_wtb_ttbarMC_Bwtb""" + systname + """("ttbar_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + "_ttbarMC_Bwtb" + systname + """","ttbar_ttbarMC_Bwtb""" + systname + """",vars,ttbarhistoB_wtb_ttbarMC_Bwtb""" + systname + """);
    RooDataHist ttbar_histC_wtb_ttbarMC_Cwtb""" + systname + """("ttbar_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + "_ttbarMC_Cwtb" + systname + """","ttbar_ttbarMC_Cwtb""" + systname + """",vars,ttbarhistoC_wtb_ttbarMC_Cwtb""" + systname + """);
    RooDataHist ttbar_histD_wtb_ttbarMC_Dwtb""" + systname + """("ttbar_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + "_ttbarMC_Dwtb" + systname + """","ttbar_ttbarMC_Dwtb""" + systname + """",vars,ttbarhistoD_wtb_ttbarMC_Dwtb""" + systname + """);
    RooDataHist ttbar_histA_ntb_ttbarMC_Antb""" + systname + """("ttbar_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + "_ttbarMC_Antb" + systname + """","ttbar_ttbarMC_Antb""" + systname + """",vars,ttbarhistoA_ntb_ttbarMC_Antb""" + systname + """);
    RooDataHist ttbar_histB_ntb_ttbarMC_Bntb""" + systname + """("ttbar_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + "_ttbarMC_Bntb" + systname + """","ttbar_ttbarMC_Bntb""" + systname + """",vars,ttbarhistoB_ntb_ttbarMC_Bntb""" + systname + """);
    RooDataHist ttbar_histC_ntb_ttbarMC_Cntb""" + systname + """("ttbar_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + "_ttbarMC_Cntb" + systname + """","ttbar_ttbarMC_Cntb""" + systname + """",vars,ttbarhistoC_ntb_ttbarMC_Cntb""" + systname + """);
    RooDataHist ttbar_histD_ntb_ttbarMC_Dntb""" + systname + """("ttbar_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + "_ttbarMC_Dntb" + systname + """","ttbar_ttbarMC_Dntb""" + systname + """",vars,ttbarhistoD_ntb_ttbarMC_Dntb""" + systname + """);
    
    
    wspace.import(ttbar_histA_wtb_ttbarMC_Awtb""" + systname + """);
    wspace.import(ttbar_histB_wtb_ttbarMC_Bwtb""" + systname + """);
    wspace.import(ttbar_histC_wtb_ttbarMC_Cwtb""" + systname + """);
    wspace.import(ttbar_histD_wtb_ttbarMC_Dwtb""" + systname + """);
    wspace.import(ttbar_histA_ntb_ttbarMC_Antb""" + systname + """);
    wspace.import(ttbar_histB_ntb_ttbarMC_Bntb""" + systname + """);
    wspace.import(ttbar_histC_ntb_ttbarMC_Cntb""" + systname + """);
    wspace.import(ttbar_histD_ntb_ttbarMC_Dntb""" + systname + """);    

"""


    #for SignalNick in SignalNickList:
        #for syst in systlist:
    for syst in systlist:          #if syst is "nominal":
            systname=syst
            script+="""
            
    TH1 * """ + SignalNick + """_histoA_wtb_""" + systname + """ = 0;
    TH1 * """ + SignalNick + """_histoB_wtb_""" + systname + """ = 0;
    TH1 * """ + SignalNick + """_histoC_wtb_""" + systname + """ = 0;
    TH1 * """ + SignalNick + """_histoD_wtb_""" + systname + """ = 0;
    TH1 * """ + SignalNick + """_histoA_ntb_""" + systname + """ = 0;
    TH1 * """ + SignalNick + """_histoB_ntb_""" + systname + """ = 0;
    TH1 * """ + SignalNick + """_histoC_ntb_""" + systname + """ = 0;
    TH1 * """ + SignalNick + """_histoD_ntb_""" + systname + """ = 0;
    
   
    file->GetObject(\"""" + SignalNick + """_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_""" + systname + """\", """ + SignalNick + """_histoA_wtb_""" + systname + """);
    file->GetObject(\"""" + SignalNick + """_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """_""" + systname + """\", """ + SignalNick + """_histoB_wtb_""" + systname + """);
    file->GetObject(\"""" + SignalNick + """_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + """_""" + systname + """\", """ + SignalNick + """_histoC_wtb_""" + systname + """);
    file->GetObject(\"""" + SignalNick + """_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + """_""" + systname + """\", """ + SignalNick + """_histoD_wtb_""" + systname + """);
    file->GetObject(\"""" + SignalNick + """_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_""" + systname + """\", """ + SignalNick + """_histoA_ntb_""" + systname + """);
    file->GetObject(\"""" + SignalNick + """_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """_""" + systname + """\", """ + SignalNick + """_histoB_ntb_""" + systname + """);
    file->GetObject(\"""" + SignalNick + """_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + """_""" + systname + """\", """ + SignalNick + """_histoC_ntb_""" + systname + """);
    file->GetObject(\"""" + SignalNick + """_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + """_""" + systname + """\", """ + SignalNick + """_histoD_ntb_""" + systname + """);                
            
            
    RooDataHist """ + SignalNick + """_histA_wtb_""" + systname + """(\"""" + SignalNick + """_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + "_" + systname + """\",\"""" + SignalNick + """_""" + systname + """\",vars,""" + SignalNick + """_histoA_wtb_""" + systname + """);
    RooDataHist """ + SignalNick + """_histB_wtb_""" + systname + """(\"""" + SignalNick + """_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + "_" + systname + """\",\"""" + SignalNick + """_""" + systname + """\",vars,""" + SignalNick + """_histoB_wtb_""" + systname + """);
    RooDataHist """ + SignalNick + """_histC_wtb_""" + systname + """(\"""" + SignalNick + """_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + "_" + systname + """\",\"""" + SignalNick + """_""" + systname + """\",vars,""" + SignalNick + """_histoC_wtb_""" + systname + """);
    RooDataHist """ + SignalNick + """_histD_wtb_""" + systname + """(\"""" + SignalNick + """_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + "_" + systname + """\",\"""" + SignalNick + """_""" + systname + """\",vars,""" + SignalNick + """_histoD_wtb_""" + systname + """);
    RooDataHist """ + SignalNick + """_histA_ntb_""" + systname + """(\"""" + SignalNick + """_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + "_" + systname + """\",\"""" + SignalNick + """_""" + systname + """\",vars,""" + SignalNick + """_histoA_ntb_""" + systname + """);
    RooDataHist """ + SignalNick + """_histB_ntb_""" + systname + """(\"""" + SignalNick + """_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + "_" + systname + """\",\"""" + SignalNick + """_""" + systname + """\",vars,""" + SignalNick + """_histoB_ntb_""" + systname + """);
    RooDataHist """ + SignalNick + """_histC_ntb_""" + systname + """(\"""" + SignalNick + """_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + "_" + systname + """\",\"""" + SignalNick + """_""" + systname + """\",vars,""" + SignalNick + """_histoC_ntb_""" + systname + """);
    RooDataHist """ + SignalNick + """_histD_ntb_""" + systname + """(\"""" + SignalNick + """_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + "_" + systname + """\",\"""" + SignalNick + """_""" + systname + """\",vars,""" + SignalNick + """_histoD_ntb_""" + systname + """);
    
    
    wspace.import(""" + SignalNick + """_histA_wtb_""" + systname + """);
    wspace.import(""" + SignalNick + """_histB_wtb_""" + systname + """);
    wspace.import(""" + SignalNick + """_histC_wtb_""" + systname + """);
    wspace.import(""" + SignalNick + """_histD_wtb_""" + systname + """);
    wspace.import(""" + SignalNick + """_histA_ntb_""" + systname + """);
    wspace.import(""" + SignalNick + """_histB_ntb_""" + systname + """);
    wspace.import(""" + SignalNick + """_histC_ntb_""" + systname + """);
    wspace.import(""" + SignalNick + """_histD_ntb_""" + systname + """);

    //wspace.import(""" + SignalNick + """_histoA_wtb_""" + systname + """);
    //wspace.import(""" + SignalNick + """_histoB_wtb_""" + systname + """);
    //wspace.import(""" + SignalNick + """_histoC_wtb_""" + systname + """);
    //wspace.import(""" + SignalNick + """_histoD_wtb_""" + systname + """);
    //wspace.import(""" + SignalNick + """_histoA_ntb_""" + systname + """);
    //wspace.import(""" + SignalNick + """_histoB_ntb_""" + systname + """);
    //wspace.import(""" + SignalNick + """_histoC_ntb_""" + systname + """);
    //wspace.import(""" + SignalNick + """_histoD_ntb_""" + systname + """);
    
    """

            if syst=='nominal':
                for l in range(1,nbins+1):
                  for var in  ["Up","Down"]:
                   #for cat in ["A_wtb","B_wtb","C_wtb","D_wtb","A_ntb","B_ntb","C_ntb","D_ntb"]:   
                    systname="_stat_bin"+str(l)+var
                    script+="""
    TH1 *""" + SignalNick + """_histoA_wtb_SignalMC_Awtb""" + systname + """ = (TH1*)""" + SignalNick + """_histoA_wtb_""" + syst + """->Clone(\"""" + SignalNick + """_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + "_SignalMC_Awtb" + systname + """"); 
    TH1 *""" + SignalNick + """_histoB_wtb_SignalMC_Bwtb""" + systname + """ = (TH1*)""" + SignalNick + """_histoB_wtb_""" + syst + """->Clone(\"""" + SignalNick + """_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + "_SignalMC_Bwtb" + systname + """"); 
    TH1 *""" + SignalNick + """_histoC_wtb_SignalMC_Cwtb""" + systname + """ = (TH1*)""" + SignalNick + """_histoC_wtb_""" + syst + """->Clone(\"""" + SignalNick + """_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + "_SignalMC_Cwtb" + systname + """"); 
    TH1 *""" + SignalNick + """_histoD_wtb_SignalMC_Dwtb""" + systname + """ = (TH1*)""" + SignalNick + """_histoD_wtb_""" + syst + """->Clone(\"""" + SignalNick + """_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + "_SignalMC_Dwtb" + systname + """"); 
    TH1 *""" + SignalNick + """_histoA_ntb_SignalMC_Antb""" + systname + """ = (TH1*)""" + SignalNick + """_histoA_ntb_""" + syst + """->Clone(\"""" + SignalNick + """_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + "_SignalMC_Antb" + systname + """"); 
    TH1 *""" + SignalNick + """_histoB_ntb_SignalMC_Bntb""" + systname + """ = (TH1*)""" + SignalNick + """_histoB_ntb_""" + syst + """->Clone(\"""" + SignalNick + """_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + "_SignalMC_Bntb" + systname + """"); 
    TH1 *""" + SignalNick + """_histoC_ntb_SignalMC_Cntb""" + systname + """ = (TH1*)""" + SignalNick + """_histoC_ntb_""" + syst + """->Clone(\"""" + SignalNick + """_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + "_SignalMC_Cntb" + systname + """"); 
    TH1 *""" + SignalNick + """_histoD_ntb_SignalMC_Dntb""" + systname + """ = (TH1*)""" + SignalNick + """_histoD_ntb_""" + syst + """->Clone(\"""" + SignalNick + """_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + "_SignalMC_Dntb" + systname + """"); 
"""
                    if(var=="Up"):
                     script+="""
    if(""" + SignalNick + """_histoA_wtb_SignalMC_Awtb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        """ + SignalNick + """_histoA_wtb_SignalMC_Awtb""" + systname + """->SetBinContent("""+str(l)+""",(""" + SignalNick + """_histoA_wtb_SignalMC_Awtb""" + systname + """->GetBinContent("""+str(l)+""")+""" + SignalNick + """_histoA_wtb_SignalMC_Awtb""" + systname + """->GetBinErrorUp("""+str(l)+""")));
    };
    if(""" + SignalNick + """_histoB_wtb_SignalMC_Bwtb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        """ + SignalNick + """_histoB_wtb_SignalMC_Bwtb""" + systname + """->SetBinContent("""+str(l)+""",(""" + SignalNick + """_histoB_wtb_SignalMC_Bwtb""" + systname + """->GetBinContent("""+str(l)+""")+""" + SignalNick + """_histoB_wtb_SignalMC_Bwtb""" + systname + """->GetBinErrorUp("""+str(l)+""")));
    }
    if(""" + SignalNick + """_histoC_wtb_SignalMC_Cwtb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        """ + SignalNick + """_histoC_wtb_SignalMC_Cwtb""" + systname + """->SetBinContent("""+str(l)+""",(""" + SignalNick + """_histoC_wtb_SignalMC_Cwtb""" + systname + """->GetBinContent("""+str(l)+""")+""" + SignalNick + """_histoC_wtb_SignalMC_Cwtb""" + systname + """->GetBinErrorUp("""+str(l)+""")));
    }
    if(""" + SignalNick + """_histoD_wtb_SignalMC_Dwtb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        """ + SignalNick + """_histoD_wtb_SignalMC_Dwtb""" + systname + """->SetBinContent("""+str(l)+""",(""" + SignalNick + """_histoD_wtb_SignalMC_Dwtb""" + systname + """->GetBinContent("""+str(l)+""")+""" + SignalNick + """_histoD_wtb_SignalMC_Dwtb""" + systname + """->GetBinErrorUp("""+str(l)+""")));
    }
    if(""" + SignalNick + """_histoA_ntb_SignalMC_Antb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        """ + SignalNick + """_histoA_ntb_SignalMC_Antb""" + systname + """->SetBinContent("""+str(l)+""",(""" + SignalNick + """_histoA_ntb_SignalMC_Antb""" + systname + """->GetBinContent("""+str(l)+""")+""" + SignalNick + """_histoA_ntb_SignalMC_Antb""" + systname + """->GetBinErrorUp("""+str(l)+""")));
    }
    if(""" + SignalNick + """_histoB_ntb_SignalMC_Bntb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        """ + SignalNick + """_histoB_ntb_SignalMC_Bntb""" + systname + """->SetBinContent("""+str(l)+""",(""" + SignalNick + """_histoB_ntb_SignalMC_Bntb""" + systname + """->GetBinContent("""+str(l)+""")+""" + SignalNick + """_histoB_ntb_SignalMC_Bntb""" + systname + """->GetBinErrorUp("""+str(l)+""")));
    }
    if(""" + SignalNick + """_histoC_ntb_SignalMC_Cntb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        """ + SignalNick + """_histoC_ntb_SignalMC_Cntb""" + systname + """->SetBinContent("""+str(l)+""",(""" + SignalNick + """_histoC_ntb_SignalMC_Cntb""" + systname + """->GetBinContent("""+str(l)+""")+""" + SignalNick + """_histoC_ntb_SignalMC_Cntb""" + systname + """->GetBinErrorUp("""+str(l)+""")));
    }
    if(""" + SignalNick + """_histoD_ntb_SignalMC_Dntb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        """ + SignalNick + """_histoD_ntb_SignalMC_Dntb""" + systname + """->SetBinContent("""+str(l)+""",(""" + SignalNick + """_histoD_ntb_SignalMC_Dntb""" + systname + """->GetBinContent("""+str(l)+""")+""" + SignalNick + """_histoD_ntb_SignalMC_Dntb""" + systname + """->GetBinErrorUp("""+str(l)+""")));
    }

    
"""
                    else:
                     script+="""
    if(""" + SignalNick + """_histoA_wtb_SignalMC_Awtb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        """ + SignalNick + """_histoA_wtb_SignalMC_Awtb""" + systname + """->SetBinContent("""+str(l)+""",(""" + SignalNick + """_histoA_wtb_SignalMC_Awtb""" + systname + """->GetBinContent("""+str(l)+""")+""" + SignalNick + """_histoA_wtb_SignalMC_Awtb""" + systname + """->GetBinErrorLow("""+str(l)+""")));
    };
    if(""" + SignalNick + """_histoB_wtb_SignalMC_Bwtb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        """ + SignalNick + """_histoB_wtb_SignalMC_Bwtb""" + systname + """->SetBinContent("""+str(l)+""",(""" + SignalNick + """_histoB_wtb_SignalMC_Bwtb""" + systname + """->GetBinContent("""+str(l)+""")+""" + SignalNick + """_histoB_wtb_SignalMC_Bwtb""" + systname + """->GetBinErrorLow("""+str(l)+""")));
    }
    if(""" + SignalNick + """_histoC_wtb_SignalMC_Cwtb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        """ + SignalNick + """_histoC_wtb_SignalMC_Cwtb""" + systname + """->SetBinContent("""+str(l)+""",(""" + SignalNick + """_histoC_wtb_SignalMC_Cwtb""" + systname + """->GetBinContent("""+str(l)+""")+""" + SignalNick + """_histoC_wtb_SignalMC_Cwtb""" + systname + """->GetBinErrorLow("""+str(l)+""")));
    }
    if(""" + SignalNick + """_histoD_wtb_SignalMC_Dwtb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        """ + SignalNick + """_histoD_wtb_SignalMC_Dwtb""" + systname + """->SetBinContent("""+str(l)+""",(""" + SignalNick + """_histoD_wtb_SignalMC_Dwtb""" + systname + """->GetBinContent("""+str(l)+""")+""" + SignalNick + """_histoD_wtb_SignalMC_Dwtb""" + systname + """->GetBinErrorLow("""+str(l)+""")));
    }
    if(""" + SignalNick + """_histoA_ntb_SignalMC_Antb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        """ + SignalNick + """_histoA_ntb_SignalMC_Antb""" + systname + """->SetBinContent("""+str(l)+""",(""" + SignalNick + """_histoA_ntb_SignalMC_Antb""" + systname + """->GetBinContent("""+str(l)+""")+""" + SignalNick + """_histoA_ntb_SignalMC_Antb""" + systname + """->GetBinErrorLow("""+str(l)+""")));
    }
    if(""" + SignalNick + """_histoB_ntb_SignalMC_Bntb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        """ + SignalNick + """_histoB_ntb_SignalMC_Bntb""" + systname + """->SetBinContent("""+str(l)+""",(""" + SignalNick + """_histoB_ntb_SignalMC_Bntb""" + systname + """->GetBinContent("""+str(l)+""")+""" + SignalNick + """_histoB_ntb_SignalMC_Bntb""" + systname + """->GetBinErrorLow("""+str(l)+""")));
    }
    if(""" + SignalNick + """_histoC_ntb_SignalMC_Cntb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        """ + SignalNick + """_histoC_ntb_SignalMC_Cntb""" + systname + """->SetBinContent("""+str(l)+""",(""" + SignalNick + """_histoC_ntb_SignalMC_Cntb""" + systname + """->GetBinContent("""+str(l)+""")+""" + SignalNick + """_histoC_ntb_SignalMC_Cntb""" + systname + """->GetBinErrorLow("""+str(l)+""")));
    }
    if(""" + SignalNick + """_histoD_ntb_SignalMC_Dntb""" + systname + """->GetBinContent("""+str(l)+""")!=0){
        """ + SignalNick + """_histoD_ntb_SignalMC_Dntb""" + systname + """->SetBinContent("""+str(l)+""",(""" + SignalNick + """_histoD_ntb_SignalMC_Dntb""" + systname + """->GetBinContent("""+str(l)+""")+""" + SignalNick + """_histoD_ntb_SignalMC_Dntb""" + systname + """->GetBinErrorLow("""+str(l)+""")));
    }

"""


                    script+="""
    RooDataHist """ + SignalNick + """_histA_wtb_SignalMC_Awtb""" + systname + """(\""""+ SignalNick + """_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + "_SignalMC_Awtb" + systname + """","_SignalMC_Awtb""" + systname + """",vars,""" + SignalNick + """_histoA_wtb_SignalMC_Awtb""" + systname + """);
    RooDataHist """ + SignalNick + """_histB_wtb_SignalMC_Bwtb""" + systname + """(\""""+ SignalNick + """_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + "_SignalMC_Bwtb" + systname + """","_SignalMC_Bwtb""" + systname + """",vars,""" + SignalNick + """_histoB_wtb_SignalMC_Bwtb""" + systname + """);
    RooDataHist """ + SignalNick + """_histC_wtb_SignalMC_Cwtb""" + systname + """(\""""+ SignalNick + """_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + "_SignalMC_Cwtb" + systname + """","_SignalMC_Cwtb""" + systname + """",vars,""" + SignalNick + """_histoC_wtb_SignalMC_Cwtb""" + systname + """);
    RooDataHist """ + SignalNick + """_histD_wtb_SignalMC_Dwtb""" + systname + """(\""""+ SignalNick + """_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + "_SignalMC_Dwtb" + systname + """","_SignalMC_Dwtb""" + systname + """",vars,""" + SignalNick + """_histoD_wtb_SignalMC_Dwtb""" + systname + """);
    RooDataHist """ + SignalNick + """_histA_ntb_SignalMC_Antb""" + systname + """(\""""+ SignalNick + """_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + "_SignalMC_Antb" + systname + """","_SignalMC_Antb""" + systname + """",vars,""" + SignalNick + """_histoA_ntb_SignalMC_Antb""" + systname + """);
    RooDataHist """ + SignalNick + """_histB_ntb_SignalMC_Bntb""" + systname + """(\""""+ SignalNick + """_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + "_SignalMC_Bntb" + systname + """","_SignalMC_Bntb""" + systname + """",vars,""" + SignalNick + """_histoB_ntb_SignalMC_Bntb""" + systname + """);
    RooDataHist """ + SignalNick + """_histC_ntb_SignalMC_Cntb""" + systname + """(\""""+ SignalNick + """_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + "_SignalMC_Cntb" + systname + """","_SignalMC_Cntb""" + systname + """",vars,""" + SignalNick + """_histoC_ntb_SignalMC_Cntb""" + systname + """);
    RooDataHist """ + SignalNick + """_histD_ntb_SignalMC_Dntb""" + systname + """(\""""+ SignalNick + """_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + "_SignalMC_Dntb" + systname + """","_SignalMC_Dntb""" + systname + """",vars,""" +SignalNick + """_histoD_ntb_SignalMC_Dntb""" + systname + """);
    
    wspace.import(""" + SignalNick + """_histA_wtb_SignalMC_Awtb""" + systname + """);
    wspace.import(""" + SignalNick + """_histB_wtb_SignalMC_Bwtb""" + systname + """);
    wspace.import(""" + SignalNick + """_histC_wtb_SignalMC_Cwtb""" + systname + """);
    wspace.import(""" + SignalNick + """_histD_wtb_SignalMC_Dwtb""" + systname + """);
    wspace.import(""" + SignalNick + """_histA_ntb_SignalMC_Antb""" + systname + """);
    wspace.import(""" + SignalNick + """_histB_ntb_SignalMC_Bntb""" + systname + """);
    wspace.import(""" + SignalNick + """_histC_ntb_SignalMC_Cntb""" + systname + """);
    wspace.import(""" + SignalNick + """_histD_ntb_SignalMC_Dntb""" + systname + """);
"""





    script+="""

    for(int j=1; j<datahistoA_wtb->GetNbinsX()+1;j++){

        //if(datahistoA_wtb->GetBinContent(j)-ttbarhistoA_wtb_nominal->GetBinContent(j)<0.5){datahistoA_wtb->SetBinContent(j,ttbarhistoA_wtb_nominal->GetBinContent(j)*1.5+0.01);};
        //if(datahistoB_wtb->GetBinContent(j)-ttbarhistoB_wtb_nominal->GetBinContent(j)<0.5){datahistoB_wtb->SetBinContent(j,ttbarhistoB_wtb_nominal->GetBinContent(j)*1.5+0.01);};
        //if(datahistoC_wtb->GetBinContent(j)-ttbarhistoC_wtb_nominal->GetBinContent(j)<0.5){datahistoC_wtb->SetBinContent(j,ttbarhistoC_wtb_nominal->GetBinContent(j)*1.5+0.01);};
        //if(datahistoD_wtb->GetBinContent(j)-ttbarhistoD_wtb_nominal->GetBinContent(j)<0.5){datahistoD_wtb->SetBinContent(j,ttbarhistoD_wtb_nominal->GetBinContent(j)*1.5+0.01);};
        //if(datahistoA_ntb->GetBinContent(j)-ttbarhistoA_ntb_nominal->GetBinContent(j)<0.5){datahistoA_ntb->SetBinContent(j,ttbarhistoA_ntb_nominal->GetBinContent(j)*1.5+0.01);};
        //if(datahistoB_ntb->GetBinContent(j)-ttbarhistoB_ntb_nominal->GetBinContent(j)<0.5){datahistoB_ntb->SetBinContent(j,ttbarhistoB_ntb_nominal->GetBinContent(j)*1.5+0.01);};
        //if(datahistoC_ntb->GetBinContent(j)-ttbarhistoC_ntb_nominal->GetBinContent(j)<0.5){datahistoC_ntb->SetBinContent(j,ttbarhistoC_ntb_nominal->GetBinContent(j)*1.5+0.01);};
        //if(datahistoD_ntb->GetBinContent(j)-ttbarhistoD_ntb_nominal->GetBinContent(j)<0.5){datahistoD_ntb->SetBinContent(j,ttbarhistoD_ntb_nominal->GetBinContent(j)*1.5+0.01);};
        
        if((datahistoA_wtb->GetBinContent(j)-ttbarhistoA_wtb_nominal->GetBinContent(j))<0.01){datahistoA_wtb->SetBinContent(j,ttbarhistoA_wtb_nominal->GetBinContent(j)+0.01);};
        if((datahistoB_wtb->GetBinContent(j)-ttbarhistoB_wtb_nominal->GetBinContent(j))<0.01){datahistoB_wtb->SetBinContent(j,ttbarhistoB_wtb_nominal->GetBinContent(j)+0.01);};
        if((datahistoC_wtb->GetBinContent(j)-ttbarhistoC_wtb_nominal->GetBinContent(j))<0.01){datahistoC_wtb->SetBinContent(j,ttbarhistoC_wtb_nominal->GetBinContent(j)+0.01);};
        if((datahistoD_wtb->GetBinContent(j)-ttbarhistoD_wtb_nominal->GetBinContent(j))<0.01){datahistoD_wtb->SetBinContent(j,ttbarhistoD_wtb_nominal->GetBinContent(j)+0.01);};
        if((datahistoA_ntb->GetBinContent(j)-ttbarhistoA_ntb_nominal->GetBinContent(j))<0.01){datahistoA_ntb->SetBinContent(j,ttbarhistoA_ntb_nominal->GetBinContent(j)+0.01);};
        if((datahistoB_ntb->GetBinContent(j)-ttbarhistoB_ntb_nominal->GetBinContent(j))<0.01){datahistoB_ntb->SetBinContent(j,ttbarhistoB_ntb_nominal->GetBinContent(j)+0.01);};
        if((datahistoC_ntb->GetBinContent(j)-ttbarhistoC_ntb_nominal->GetBinContent(j))<0.01){datahistoC_ntb->SetBinContent(j,ttbarhistoC_ntb_nominal->GetBinContent(j)+0.01);};
        if((datahistoD_ntb->GetBinContent(j)-ttbarhistoD_ntb_nominal->GetBinContent(j))<0.01){datahistoD_ntb->SetBinContent(j,ttbarhistoD_ntb_nominal->GetBinContent(j)+0.01);};
    }
    
    RooDataHist data_histA_wtb("DATA_""" + truesig + """_ABCD5_withtopbtag_CatA_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoA_wtb);
    RooDataHist data_histB_wtb("DATA_""" + truesig + """_ABCD5_withtopbtag_CatB_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoB_wtb);
    RooDataHist data_histC_wtb("DATA_""" + truesig + """_ABCD5_withtopbtag_CatC_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoC_wtb);
    RooDataHist data_histD_wtb("DATA_""" + truesig + """_ABCD5_withtopbtag_CatD_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoD_wtb);
    RooDataHist data_histA_ntb("DATA_""" + truesig + """_ABCD5_notopbtag_CatA_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoA_ntb);
    RooDataHist data_histB_ntb("DATA_""" + truesig + """_ABCD5_notopbtag_CatB_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoB_ntb);
    RooDataHist data_histC_ntb("DATA_""" + truesig + """_ABCD5_notopbtag_CatC_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoC_ntb);
    RooDataHist data_histD_ntb("DATA_""" + truesig + """_ABCD5_notopbtag_CatD_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoD_ntb);


    wspace.import(data_histA_wtb);
    wspace.import(data_histB_wtb);
    wspace.import(data_histC_wtb);
    wspace.import(data_histD_wtb);
    wspace.import(data_histA_ntb);
    wspace.import(data_histB_ntb);
    wspace.import(data_histC_ntb);
    wspace.import(data_histD_ntb);
    
    
    RooArgList QCD_CatA_wtb_bins;
    RooArgList QCD_CatB_wtb_bins;
    RooArgList QCD_CatC_wtb_bins;
    RooArgList QCD_CatD_wtb_bins;
    RooArgList QCD_CatA_ntb_bins;
    RooArgList QCD_CatB_ntb_bins;
    RooArgList QCD_CatC_ntb_bins;
    RooArgList QCD_CatD_ntb_bins; 

    RooRealVar QCD_ABCD_shape_wtb("QCD_ABCD_shape_wtb","QCD_ABCD_shape_wtb",0.0,-100,100);
    RooRealVar QCD_ABCD_rate_wtb("QCD_ABCD_rate_wtb","QCD_ABCD_rate_wtb",0.0,-100,100);
    //RooRealVar QCD_ABCD_shape_wtb_m("QCD_ABCD_shape_wtb_m","QCD_ABCD_shape_wtb_m",""" + str(Zprime_withtopbtag_systshape_m) + """,-100,100);
    //RooRealVar QCD_ABCD_shape_wtb_y("QCD_ABCD_shape_wtb_y","QCD_ABCD_shape_wtb_y",""" + str(Zprime_withtopbtag_systshape_c) + """,-100,100);
    
    RooRealVar QCD_ABCD_shape_ntb("QCD_ABCD_shape_ntb","QCD_ABCD_shape_ntb",0.0,-100,100);
    RooRealVar QCD_ABCD_rate_ntb("QCD_ABCD_rate_ntb","QCD_ABCD_rate_ntb",0.0,-100,100);
    //RooRealVar QCD_ABCD_shape_ntb_m("QCD_ABCD_shape_ntb_m","QCD_ABCD_shape_ntb_m",""" + str(Zprime_notopbtag_systshape_m) + """,-100,100);
    //RooRealVar QCD_ABCD_shape_ntb_y("QCD_ABCD_shape_ntb_y","QCD_ABCD_shape_ntb_y",""" + str(Zprime_notopbtag_systshape_c) + """,-100,100);
    
"""

   #for Region  in ['A','B','C','D']:
     #for Category in ['wtb','ntb']:
   #script+="""
   #for(int i=0; i<22; i++){
       #RooRealVar QCD_Cat""" + Region + """_""" + Category + """_bin("QCD_Cat""" + Region + """_""" + Category + """_bin" + std::str(i),"QCD Background yield in signal region with top-btag, bin1" + std::str(i),1,0,1000);
       #QCD_Cat""" + Region + """_""" + Category + """_bins.add(QCD_Cat""" + Region + """_""" + Category + """_bin); 
       
   #}
           
#"""


    for i in range(1,nbins+1):
        script+="""
    //RooRealVar Bin_Mass_bin""" +  str(i) + """("Bin_Mass_bin""" +  str(i) + '"' + ""","Bin Mass, bin""" +  str(i) + '"' + """,1,0,100000);
    //RooRealVar QCD_CatB_wtb_bin""" +  str(i) + """("QCD_CatB_wtb_bin""" +  str(i) + '"' + ""","QCD Background region B with top-btag, bin""" +  str(i) + '"' + """,""" + str(datahisto.GetBinContent(i)) + """,0.01,100000);
    //RooRealVar QCD_CatC_wtb_bin""" +  str(i) + """("QCD_CatC_wtb_bin""" +  str(i) + '"' + ""","QCD Background region C with top-btag, bin""" +  str(i) + '"' + """,""" + str(datahisto.GetBinContent(i)) + """,0.01,100000);
    //RooRealVar QCD_CatD_wtb_bin""" +  str(i) + """("QCD_CatD_wtb_bin""" +  str(i) + '"' + ""","QCD Background region D with top-btag, bin""" +  str(i) + '"' + """,""" + str(datahisto.GetBinContent(i)) + """,0.01,100000);
    //RooRealVar QCD_CatB_ntb_bin""" +  str(i) + """("QCD_CatB_ntb_bin""" +  str(i) + '"' + ""","QCD Background region B no top-btag, bin""" +  str(i) + '"' + """,""" + str(datahisto.GetBinContent(i)) + """,0.01,100000);
    //RooRealVar QCD_CatC_ntb_bin""" +  str(i) + """("QCD_CatC_ntb_bin""" +  str(i) + '"' + ""","QCD Background region C no top-btag, bin""" +  str(i) + '"' + """,""" + str(datahisto.GetBinContent(i)) + """,0.01,100000);
    //RooRealVar QCD_CatD_ntb_bin""" +  str(i) + """("QCD_CatD_ntb_bin""" +  str(i) + '"' + ""","QCD Background region D no top-btag, bin""" +  str(i) + '"' + """,""" + str(datahisto.GetBinContent(i)) + """,0.01,100000);
    
    RooRealVar QCD_CatB_wtb_bin""" +  str(i) + """("QCD_CatB_wtb_bin""" +  str(i) + '"' + ""","QCD Background region B with top-btag, bin""" +  str(i) + '"' + """,datahistoB_wtb->GetBinContent(""" + str(i) + """)-ttbarhistoB_wtb_nominal->GetBinContent(""" + str(i) + """),0.00001,100000);
    std::cout<<"QCD_RegB_wtb_bin""" + str(i) + """\"<<datahistoB_wtb->GetBinContent(""" + str(i) + """)-ttbarhistoB_wtb_nominal->GetBinContent(""" + str(i) + """)<<std::endl;
    RooRealVar QCD_CatC_wtb_bin""" +  str(i) + """("QCD_CatC_wtb_bin""" +  str(i) + '"' + ""","QCD Background region C with top-btag, bin""" +  str(i) + '"' + """,datahistoC_wtb->GetBinContent(""" + str(i) + """)-ttbarhistoC_wtb_nominal->GetBinContent(""" + str(i) + """),0.00001,100000);
    std::cout<<"QCD_RegC_wtb_bin""" + str(i) + """\"<<datahistoC_wtb->GetBinContent(""" + str(i) + """)-ttbarhistoC_wtb_nominal->GetBinContent(""" + str(i) + """)<<std::endl;
    RooRealVar QCD_CatD_wtb_bin""" +  str(i) + """("QCD_CatD_wtb_bin""" +  str(i) + '"' + ""","QCD Background region D with top-btag, bin""" +  str(i) + '"' + """,datahistoD_wtb->GetBinContent(""" + str(i) + """)-ttbarhistoD_wtb_nominal->GetBinContent(""" + str(i) + """),0.00001,100000);
    std::cout<<"QCD_RegD_wtb_bin""" + str(i) + """\"<<datahistoD_wtb->GetBinContent(""" + str(i) + """)-ttbarhistoD_wtb_nominal->GetBinContent(""" + str(i) + """)<<std::endl;
    RooRealVar QCD_CatB_ntb_bin""" +  str(i) + """("QCD_CatB_ntb_bin""" +  str(i) + '"' + ""","QCD Background region B no top-btag, bin""" +  str(i) + '"' + """,datahistoB_ntb->GetBinContent(""" + str(i) + """)-ttbarhistoB_ntb_nominal->GetBinContent(""" + str(i) + """),0.00001,100000);
    std::cout<<"QCD_RegB_ntb_bin""" + str(i) + """\"<<datahistoB_ntb->GetBinContent(""" + str(i) + """)-ttbarhistoB_ntb_nominal->GetBinContent(""" + str(i) + """)<<std::endl;
    RooRealVar QCD_CatC_ntb_bin""" +  str(i) + """("QCD_CatC_ntb_bin""" +  str(i) + '"' + ""","QCD Background region C no top-btag, bin""" +  str(i) + '"' + """,datahistoC_ntb->GetBinContent(""" + str(i) + """)-ttbarhistoC_ntb_nominal->GetBinContent(""" + str(i) + """),0.00001,100000);
    std::cout<<"QCD_RegC_ntb_bin""" + str(i) + """\"<<datahistoC_ntb->GetBinContent(""" + str(i) + """)-ttbarhistoC_ntb_nominal->GetBinContent(""" + str(i) + """)<<std::endl;
    RooRealVar QCD_CatD_ntb_bin""" +  str(i) + """("QCD_CatD_ntb_bin""" +  str(i) + '"' + ""","QCD Background region D no top-btag, bin""" +  str(i) + '"' + """,datahistoD_ntb->GetBinContent(""" + str(i) + """)-ttbarhistoD_ntb_nominal->GetBinContent(""" + str(i) + """),0.00001,100000);
    std::cout<<"QCD_RegD_ntb_bin""" + str(i) + """\"<<datahistoD_ntb->GetBinContent(""" + str(i) + """)-ttbarhistoD_ntb_nominal->GetBinContent(""" + str(i) + """)<<std::endl;
    
"""    

    for i in range(1,nbins+1):
        script+="""
    //RooFormulaVar QCD_CatA_wtb_bin"""+  str(i) + """("QCD_CatA_wtb_bin"""+  str(i) + '"' + ""","QCD Background yield in signal region with top b-tag, bin"""+  str(i) + '"' + ""","@0*@1/@2*(1 +""" + str(1.0+Zprime_withtopbtag_systrate) + """*@4 +(("""+ str(Zprime_withtopbtag_systshape_m) +""") * """ + str(datahisto.GetBinCenter(i)) + """ + (""" + str(Zprime_withtopbtag_systshape_c) + """) ) * @3 )",RooArgList(QCD_CatB_wtb_bin""" +  str(i) + """,QCD_CatC_wtb_bin""" +  str(i) + """,QCD_CatD_wtb_bin""" +  str(i) + """, QCD_ABCD_shape_wtb, QCD_ABCD_rate_wtb));
    //RooFormulaVar QCD_CatA_ntb_bin"""+  str(i) + """("QCD_CatA_ntb_bin"""+  str(i) + '"' + ""","QCD Background yield in signal region no top b-tag, bin"""+  str(i) + '"' + ""","@0*@1/@2*(1 +""" + str(1.0+Zprime_notopbtag_systrate) + """*@4 + ((""" + str(Zprime_notopbtag_systshape_m) + """) * """ + str(datahisto.GetBinCenter(i)) + """ + (""" + str(Zprime_notopbtag_systshape_c) + """) ) * @3 )",RooArgList(QCD_CatB_ntb_bin""" +  str(i) + """,QCD_CatC_ntb_bin""" +  str(i) + """,QCD_CatD_ntb_bin""" +  str(i) + """, QCD_ABCD_shape_ntb, QCD_ABCD_rate_ntb));

    RooFormulaVar QCD_CatA_wtb_bin"""+  str(i) + """("QCD_CatA_wtb_bin"""+  str(i) + '"' + ""","QCD Background yield in signal region with top b-tag, bin"""+  str(i) + '"' + ""","@0*@1/@2*(1 +""" + str(1.0+Zprime_withtopbtag_systrate) + """*@4 +(("""+ str(Zprime_withtopbtag_systshape_m) +""") * """ + str(datahisto.GetBinCenter(i)) + """ + (""" + str(Zprime_withtopbtag_systshape_c) + """) ) * @3 )",RooArgList(QCD_CatB_wtb_bin""" +  str(i) + """,QCD_CatC_wtb_bin""" +  str(i) + """,QCD_CatD_wtb_bin""" +  str(i) + """, QCD_ABCD_shape_wtb, QCD_ABCD_rate_wtb));
    RooFormulaVar QCD_CatA_ntb_bin"""+  str(i) + """("QCD_CatA_ntb_bin"""+  str(i) + '"' + ""","QCD Background yield in signal region no top b-tag, bin"""+  str(i) + '"' + ""","@0*@1/@2*(1 +""" + str(1.0+Zprime_notopbtag_systrate) + """*@4 + ((""" + str(Zprime_notopbtag_systshape_m) + """) * """ + str(datahisto.GetBinCenter(i)) + """ + (""" + str(Zprime_notopbtag_systshape_c) + """) ) * @3 )",RooArgList(QCD_CatB_ntb_bin""" +  str(i) + """,QCD_CatC_ntb_bin""" +  str(i) + """,QCD_CatD_ntb_bin""" +  str(i) + """, QCD_ABCD_shape_ntb, QCD_ABCD_rate_ntb));
    """

    #RooFormulaVar QCD_ABCD_wtb_bin"""+  str(i) + """("QCD_CatA_wtb_bin"""+  str(i) + '"' + ""","QCD Background yield in signal region with top b-tag, bin"""+  str(i) + '"' + ""","@0*@1*@2",RooArgList(QCD_CatB_wtb_bin""" +  str(i) + """,QCD_CatC_wtb_bin""" +  str(i) + """,QCD_CatD_wtb_bin""" +  str(i) + """));
    #RooFormulaVar QCD_ABCD_ntb_bin"""+  str(i) + """("QCD_CatA_ntb_bin"""+  str(i) + '"' + ""","QCD Background yield in signal region no top b-tag, bin"""+  str(i) + '"' + ""","@0*@1*@2",RooArgList(QCD_CatB_ntb_bin""" +  str(i) + """,QCD_CatC_ntb_bin""" +  str(i) + """,QCD_CatD_ntb_bin""" +  str(i) + """));



    for i in range(1,nbins+1):
        script+="""
    QCD_CatA_wtb_bins.add(QCD_CatA_wtb_bin""" +  str(i) + """);
    QCD_CatB_wtb_bins.add(QCD_CatB_wtb_bin""" +  str(i) + """);
    QCD_CatC_wtb_bins.add(QCD_CatC_wtb_bin""" +  str(i) + """);
    QCD_CatD_wtb_bins.add(QCD_CatD_wtb_bin""" +  str(i) + """);
    QCD_CatA_ntb_bins.add(QCD_CatA_ntb_bin""" +  str(i) + """);
    QCD_CatB_ntb_bins.add(QCD_CatB_ntb_bin""" +  str(i) + """);
    QCD_CatC_ntb_bins.add(QCD_CatC_ntb_bin""" +  str(i) + """);
    QCD_CatD_ntb_bins.add(QCD_CatD_ntb_bin""" +  str(i) + """);
"""        


    script+="""
    
    RooParametricHist p_QCD_wtb_CatA("QCD_CatA_wtb","QCD Background PDF in signal region with top-btag",Zprime_M,QCD_CatA_wtb_bins,*datahistoA_wtb);
    RooParametricHist p_QCD_wtb_CatB("QCD_CatB_wtb","QCD Background PDF in BackgroundB region with top-btag",Zprime_M,QCD_CatB_wtb_bins,*datahistoB_wtb);
    RooParametricHist p_QCD_wtb_CatC("QCD_CatC_wtb","QCD Background PDF in BackgroundC region with top-btag",Zprime_M,QCD_CatC_wtb_bins,*datahistoC_wtb);
    RooParametricHist p_QCD_wtb_CatD("QCD_CatD_wtb","QCD Background PDF in BackgroundD region with top-btag",Zprime_M,QCD_CatD_wtb_bins,*datahistoD_wtb);
    RooParametricHist p_QCD_ntb_CatA("QCD_CatA_ntb","QCD Background PDF in signal region no top-btag",Zprime_M,QCD_CatA_ntb_bins,*datahistoA_ntb);
    RooParametricHist p_QCD_ntb_CatB("QCD_CatB_ntb","QCD Background PDF in BackgroundB region no top-btag",Zprime_M,QCD_CatB_ntb_bins,*datahistoB_ntb);
    RooParametricHist p_QCD_ntb_CatC("QCD_CatC_ntb","QCD Background PDF in BackgroundC region no top-btag",Zprime_M,QCD_CatC_ntb_bins,*datahistoC_ntb);
    RooParametricHist p_QCD_ntb_CatD("QCD_CatD_ntb","QCD Background PDF in BackgroundD region no top-btag",Zprime_M,QCD_CatD_ntb_bins,*datahistoD_ntb);

    RooAddition p_QCD_wtb_CatA_norm("QCD_CatA_wtb_norm","Total Number of events from Background in signal region with top-btag",QCD_CatA_wtb_bins);
    RooAddition p_QCD_wtb_CatB_norm("QCD_CatB_wtb_norm","Total Number of events from Background in BackgroundB region with top-btag",QCD_CatB_wtb_bins);
    RooAddition p_QCD_wtb_CatC_norm("QCD_CatC_wtb_norm","Total Number of events from Background in BackgroundC region with top-btag",QCD_CatC_wtb_bins);
    RooAddition p_QCD_wtb_CatD_norm("QCD_CatD_wtb_norm","Total Number of events from Background in BackgroundD region with top-btag",QCD_CatD_wtb_bins);
    RooAddition p_QCD_ntb_CatA_norm("QCD_CatA_ntb_norm","Total Number of events from Background in signal region no top-btag",QCD_CatA_ntb_bins);
    RooAddition p_QCD_ntb_CatB_norm("QCD_CatB_ntb_norm","Total Number of events from Background in BackgroundB region no top-btag",QCD_CatB_ntb_bins);
    RooAddition p_QCD_ntb_CatC_norm("QCD_CatC_ntb_norm","Total Number of events from Background in BackgroundC region no top-btag",QCD_CatC_ntb_bins);
    RooAddition p_QCD_ntb_CatD_norm("QCD_CatD_ntb_norm","Total Number of events from Background in BackgroundD region no top-btag",QCD_CatD_ntb_bins);

    
    // import the pdfs
    wspace.import(p_QCD_wtb_CatA);
    wspace.import(p_QCD_wtb_CatA_norm,RooFit::RecycleConflictNodes());
    wspace.import(p_QCD_wtb_CatB);
    wspace.import(p_QCD_wtb_CatB_norm,RooFit::RecycleConflictNodes());
    wspace.import(p_QCD_wtb_CatC);
    wspace.import(p_QCD_wtb_CatC_norm,RooFit::RecycleConflictNodes());
    wspace.import(p_QCD_wtb_CatD);
    wspace.import(p_QCD_wtb_CatD_norm,RooFit::RecycleConflictNodes());
    
    wspace.import(p_QCD_ntb_CatA);
    wspace.import(p_QCD_ntb_CatA_norm,RooFit::RecycleConflictNodes());
    wspace.import(p_QCD_ntb_CatB);
    wspace.import(p_QCD_ntb_CatB_norm,RooFit::RecycleConflictNodes());
    wspace.import(p_QCD_ntb_CatC);
    wspace.import(p_QCD_ntb_CatC_norm,RooFit::RecycleConflictNodes());
    wspace.import(p_QCD_ntb_CatD);
    wspace.import(p_QCD_ntb_CatD_norm,RooFit::RecycleConflictNodes());
    fOut->cd();
    wspace.Write();
    
}    
"""
    f=open("combine_datacards/cscripts_for_wspace/createABCDCombineWorkspaceFile_" + SignalNick + "_" + WP + "_" + truesig + ".cxx","w")
    f.write(script)
    f.close()
    st = os.stat("combine_datacards/cscripts_for_wspace/createABCDCombineWorkspaceFile_" + SignalNick + "_" + WP + "_" + truesig + ".cxx")
    os.chmod("combine_datacards/cscripts_for_wspace/createABCDCombineWorkspaceFile_" + SignalNick + "_" + WP + "_" + truesig + ".cxx", st.st_mode | stat.S_IEXEC)
   

def createScript(ABCDversion,SignalNick, WP,truesig):
  #script="#!/bin/bash \n"
  #if cmsswpath!='':
    #script+="export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch \n"
    #script+="source $VO_CMS_SW_DIR/cmsset_default.sh \n"
    #script+="export SCRAM_ARCH="+os.environ['SCRAM_ARCH']+"\n"
    #script+='cd '+cmsswpath+'/src\neval `scram runtime -sh`\n'
    #script+='cd - \n'
  #script+='export PROCESSNAME="'+processname+'"\n'
  #script+='export FILENAMES="'+filenames+'"\n'
  #script+='export OUTFILENAME="'+outfilename+'"\n'
  #script+='export MAXEVENTS="'+str(maxevents)+'"\n'
  #script+='export SKIPEVENTS="'+str(skipevents)+'"\n'
  #script+='export SUFFIX="'+suffix+'"\n'
  #script+='export FILENAMES_SCALEFUNCTIONS="'+scalefunctionsdir+scalefunctions+'"\n'
  #script+='export VO_CMS_SW_DIR="/cvmfs/cms.cern.ch"\n'
  #script+='source $VO_CMS_SW_DIR/cmsset_default.sh\n'
  #script+='export CMSSW_dir="/nfs/dust/cms/user/skudella/CMSSW_8_0_12"'
  #script+='cd $CMSSW_dir/src/'
  #script+='eval `scram runtime -sh`'
  #script+='cd $mycwd'
  #script+=programpath+'\n'
  script="""
imax * #number of bins/channels
jmax * #number of backgrounds
kmax *
---------------
"""

  script+="""
shapes data_obs CatA_wtb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:DATA_""" + truesig + """_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatB_wtb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:DATA_""" + truesig + """_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatC_wtb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:DATA_""" + truesig + """_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatD_wtb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:DATA_""" + truesig + """_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatA_ntb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:DATA_""" + truesig + """_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatB_ntb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:DATA_""" + truesig + """_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatC_ntb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:DATA_""" + truesig + """_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatD_ntb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:DATA_""" + truesig + """_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + """_nominal
"""

  script+="""

shapes Sig      CatA_wtb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes Sig      CatB_wtb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes Sig      CatC_wtb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes Sig      CatD_wtb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes Sig      CatA_ntb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes Sig      CatB_ntb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes Sig      CatC_ntb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes Sig      CatD_ntb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC

shapes tt       CatA_wtb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatB_wtb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatC_wtb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatD_wtb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatA_ntb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:ttbar_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatB_ntb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:ttbar_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatC_ntb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:ttbar_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatD_ntb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:ttbar_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC



shapes QCD      CatA_wtb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:QCD_CatA_wtb
shapes QCD      CatB_wtb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:QCD_CatB_wtb
shapes QCD      CatC_wtb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:QCD_CatC_wtb
shapes QCD      CatD_wtb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:QCD_CatD_wtb
shapes QCD      CatA_ntb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:QCD_CatA_ntb
shapes QCD      CatB_ntb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:QCD_CatB_ntb
shapes QCD      CatC_ntb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:QCD_CatC_ntb
shapes QCD      CatD_ntb rootfiles/param_ws_""" + SignalNick + "_" + WP + """_""" + truesig + """.root wspace:QCD_CatD_ntb

#------------------------------
bin             CatA_ntb   CatB_ntb   CatC_ntb   CatD_ntb     CatA_wtb CatB_wtb CatC_wtb CatD_wtb 
observation     -1         -1         -1         -1           -1       -1       -1       -1
#------------------------------
bin                                CatA_ntb   CatB_ntb   CatC_ntb   CatD_ntb   CatA_wtb CatB_wtb CatC_wtb CatD_wtb     CatA_ntb   CatB_ntb   CatC_ntb   CatD_ntb   CatA_wtb CatB_wtb CatC_wtb CatD_wtb   CatA_ntb   CatB_ntb   CatC_ntb   CatD_ntb   CatA_wtb CatB_wtb CatC_wtb CatD_wtb
process                            Sig    Sig    Sig    Sig    Sig    Sig    Sig    Sig        QCD    QCD    QCD    QCD    QCD    QCD    QCD    QCD      tt     tt     tt     tt     tt     tt     tt     tt           
process                            0      0      0      0      0      0      0      0          1      1      1      1      1      1      1      1        2      2      2      2      2      2      2      2
rate                               -1     -1     -1     -1     -1     -1     -1     -1         1      1      1      1      1      1      1      1        -1     -1     -1     -1     -1     -1     -1     -1
#--------------------------------
MCSF_CSVLF                shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVHF                shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVHFStats1          shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVLFStats1          shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVHFStats2          shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVLFStats2          shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVCErr1             shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVCErr2             shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_toptag               shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_topmisstag           shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_Wtag                 shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_Wtag_tag_t21         shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_Wtag_tag_t21anti     shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_Wtag_mistag_t21      shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_Wtag_mistag_t21anti  shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_PU                   shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_PDF                  shape    -      -      -      -      -      -      -      -          -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar
MCSF_Lumi                 shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_Trigger              shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_renfac_env           shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
nominal_JER               shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
nominal_JES               shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
ttbarXS                   shape    -      -      -      -      -      -      -      -          -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
"""

  for i in range(1,nbins):
    script=script+"""
SignalMC_Antb_stat_bin""" + str(i) + """            shape   1.0     -      -      -      -      -      -      -         -      -      -      -      -      -      -      -        -      -      -      -      -      -      -      -    #uncertainty from statistic in sideband
SignalMC_Bntb_stat_bin""" + str(i) + """            shape    -     1.0     -      -      -      -      -      -          -      -      -      -      -      -      -      -        -      -      -      -      -      -      -      -    #uncertainty from statistic in sideband
SignalMC_Cntb_stat_bin""" + str(i) + """            shape    -      -     1.0     -      -      -      -      -          -      -      -      -      -      -      -      -        -      -      -      -      -      -      -      -    #uncertainty from statistic in sideband
SignalMC_Dntb_stat_bin""" + str(i) + """            shape    -      -      -     1.0     -      -      -      -          -      -      -      -      -      -      -      -        -      -      -      -      -      -      -      -    #uncertainty from statistic in sideband
SignalMC_Awtb_stat_bin""" + str(i) + """            shape    -      -      -      -     1.0     -      -      -          -      -      -      -      -      -      -      -        -      -      -      -      -      -      -      -    #uncertainty from statistic in sideband
SignalMC_Bwtb_stat_bin""" + str(i) + """            shape    -      -      -      -      -     1.0     -      -          -      -      -      -      -      -      -      -        -      -      -      -      -      -      -      -    #uncertainty from statistic in sideband
SignalMC_Cwtb_stat_bin""" + str(i) + """            shape    -      -      -      -      -      -     1.0     -          -      -      -      -      -      -      -      -        -      -      -      -      -      -      -      -    #uncertainty from statistic in sideband
SignalMC_Dwtb_stat_bin""" + str(i) + """            shape    -      -      -      -      -      -      -     1.0         -      -      -      -      -      -      -      -        -      -      -      -      -      -      -      -    #uncertainty from statistic in sideband
ttbarMC_Antb_stat_bin""" + str(i) + """             shape    -      -      -      -      -      -      -      -          -      -      -      -      -      -      -      -       1.0     -      -      -      -      -      -      -    #uncertainty from statistic in sideband
ttbarMC_Bntb_stat_bin""" + str(i) + """             shape    -      -      -      -      -      -      -      -          -      -      -      -      -      -      -      -        -     1.0     -      -      -      -      -      -    #uncertainty from statistic in sideband
ttbarMC_Cntb_stat_bin""" + str(i) + """             shape    -      -      -      -      -      -      -      -          -      -      -      -      -      -      -      -        -      -     1.0     -      -      -      -      -    #uncertainty from statistic in sideband
ttbarMC_Dntb_stat_bin""" + str(i) + """             shape    -      -      -      -      -      -      -      -          -      -      -      -      -      -      -      -        -      -      -     1.0     -      -      -      -    #uncertainty from statistic in sideband
ttbarMC_Awtb_stat_bin""" + str(i) + """             shape    -      -      -      -      -      -      -      -          -      -      -      -      -      -      -      -        -      -      -      -     1.0     -      -      -    #uncertainty from statistic in sideband
ttbarMC_Bwtb_stat_bin""" + str(i) + """             shape    -      -      -      -      -      -      -      -          -      -      -      -      -      -      -      -        -      -      -      -      -     1.0     -      -    #uncertainty from statistic in sideband
ttbarMC_Cwtb_stat_bin""" + str(i) + """             shape    -      -      -      -      -      -      -      -          -      -      -      -      -      -      -      -        -      -      -      -      -      -     1.0     -    #uncertainty from statistic in sideband
ttbarMC_Dwtb_stat_bin""" + str(i) + """             shape    -      -      -      -      -      -      -      -          -      -      -      -      -      -      -      -        -      -      -      -      -      -      -     1.0   #uncertainty from statistic in sideband"""
    


  #script=script+"""
##------------------------------
#bin             CatA_ntb   CatB_ntb   CatC_ntb   CatD_ntb     CatA_wtb CatB_wtb CatC_wtb CatD_wtb 
#observation     -1         -1         -1         -1           -1       -1       -1       -1
##------------------------------
#bin                                CatA_ntb  CatA_wtb    CatA_ntb   CatB_ntb   CatC_ntb   CatD_ntb   CatA_wtb CatB_wtb CatC_wtb CatD_wtb   CatA_ntb   CatB_ntb   CatC_ntb   CatD_ntb   CatA_wtb CatB_wtb CatC_wtb CatD_wtb
#process                            Sig    Sig     QCD    QCD    QCD    QCD    QCD    QCD    QCD    QCD      tt     tt     tt     tt     tt     tt     tt     tt           
#process                            0      0      1      1      1      1      1      1      1      1        2      2      2      2      2      2      2      2
#rate                               -1     -1     1      1      1      1      1      1      1      1        -1     -1     -1     -1     -1     -1     -1     -1


#MCSF_CSVLF                shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_CSVHF                shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_CSVHFStats1          shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_CSVLFStats1          shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_CSVHFStats2          shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_CSVLFStats2          shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_CSVCErr1             shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_CSVCErr2             shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_toptag               shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
##MCSF_topmisstag           shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_Wtag_tag_t21         shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_Wtag_tag_t21anti     shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_Wtag_mistag_t21      shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_Wtag_mistag_t21anti  shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_PU                   shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_PDF                  shape    -      -      -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar
#MCSF_Lumi                 shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_Trigger              shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_renfac_env           shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar
#nominal_JER               shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#nominal_JES               shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#ttbarXS                   shape    -      -      -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#"""


  #for i in range(1,nbins):
    #script=script+"""
#SignalMC_Antb_stat_bin""" + str(i) + """            shape   1.0     -           -      -      -      -      -      -      -      -        -      -      -      -      -      -      -      -    #uncertainty from statistic in sideband
#SignalMC_Awtb_stat_bin""" + str(i) + """            shape    -     1.0          -      -      -      -      -      -      -      -        -      -      -      -      -      -      -      -    #uncertainty from statistic in sideband
#ttbarMC_Antb_stat_bin""" + str(i) + """             shape    -      -           -      -      -      -      -      -      -      -       1.0     -      -      -      -      -      -      -    #uncertainty from statistic in sideband
#ttbarMC_Bntb_stat_bin""" + str(i) + """             shape    -      -           -      -      -      -      -      -      -      -        -     1.0     -      -      -      -      -      -    #uncertainty from statistic in sideband
#ttbarMC_Cntb_stat_bin""" + str(i) + """             shape    -      -           -      -      -      -      -      -      -      -        -      -     1.0     -      -      -      -      -    #uncertainty from statistic in sideband
#ttbarMC_Dntb_stat_bin""" + str(i) + """             shape    -      -           -      -      -      -      -      -      -      -        -      -      -     1.0     -      -      -      -    #uncertainty from statistic in sideband
#ttbarMC_Awtb_stat_bin""" + str(i) + """             shape    -      -           -      -      -      -      -      -      -      -        -      -      -      -     1.0     -      -      -    #uncertainty from statistic in sideband
#ttbarMC_Bwtb_stat_bin""" + str(i) + """             shape    -      -           -      -      -      -      -      -      -      -        -      -      -      -      -     1.0     -      -    #uncertainty from statistic in sideband
#ttbarMC_Cwtb_stat_bin""" + str(i) + """             shape    -      -           -      -      -      -      -      -      -      -        -      -      -      -      -      -     1.0     -    #uncertainty from statistic in sideband
#ttbarMC_Dwtb_stat_bin""" + str(i) + """             shape    -      -           -      -      -      -      -      -      -      -        -      -      -      -      -      -      -     1.0   #uncertainty from statistic in sideband"""
    



  #for i in range(1,nbins):
    #script=script+"""
##SignalMC_bin""" + str(i) + """_stat            shape   1.0    1.0          -      -      -      -      -      -      -      -        -      -      -      -      -      -      -      -    #uncertainty from statistic in sideband
##ttbarMC_bin""" + str(i) + """_stat             shape    -      -           -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0   #uncertainty from statistic in sideband"""
    

  script=script+"""
# QCD ABCD systematic uncertainties
QCD_ABCD_shape_wtb      param 0.0 1.0
QCD_ABCD_shape_ntb      param 0.0 1.0
QCD_ABCD_rate_wtb       param 0.0 1.0
QCD_ABCD_rate_ntb       param 0.0 1.0

# free floating parameters, we do not need to declare them, but its a good idea to 
"""
  
  for i in range(1,nbins):
    script=script+"""
QCD_CatB_wtb_bin""" + str(i) + """ flatParam
QCD_CatC_wtb_bin""" + str(i) + """ flatParam
QCD_CatD_wtb_bin""" + str(i) + """ flatParam
QCD_CatB_ntb_bin""" + str(i) + """ flatParam
QCD_CatC_ntb_bin""" + str(i) + """ flatParam
QCD_CatD_ntb_bin""" + str(i) + """ flatParam
"""
  
  
  
  f=open('combine_datacards/'+SignalNick+'_'+ABCDversion+'_'+WP+'_'+truesig+'_Combine_datacard.txt','w')
  f.write(script)
  f.close()
  #st = os.stat(datacardname)
  #os.chmod(datacardname, st.st_mode | stat.S_IEXEC)

#def createScript(scriptname,programpath,processname,filenames,outfilename,maxevents,skipevents):


def make_submissionscripts_for_workspaces(SignalNick,ABCDversion,WP,truesig):
    
  cmsswpath='/nfs/dust/cms/user/skudella/CMSSW_7_4_7'
  
  script="#!/bin/bash \n"
  if cmsswpath!='':
    script+="export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch \n"
    script+="source $VO_CMS_SW_DIR/cmsset_default.sh \n"
    script+="export SCRAM_ARCH="+os.environ['SCRAM_ARCH']+"\n"
    script+="cd "+cmsswpath+"/src\neval `scram runtime -sh`\n"
    script+="cd - \n"
    script+="""export PROCESSNAME="workspaces_"""+SignalNick+"_"+ABCDversion+"_"+WP+"""_""" + truesig + """"\n"""


  script+="""
cd /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST
cd combine_datacards/cscripts_for_wspace
root -q -b createABCDCombineWorkspaceFile_""" + SignalNick + "_" + WP + """_""" + truesig + """.cxx

cd /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST
mkdir combine_workspaces 
cd /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces
mkdir """ + SignalNick+"_"+ABCDversion+"_"+WP+"""
cd ../combine_datacards
text2workspace.py """ +SignalNick+"_"+ABCDversion+"_"+WP+"""_""" + truesig + """_Combine_datacard.txt -o ../combine_workspaces/""" +SignalNick+"_"+ABCDversion+"_"+WP+"""/""" +SignalNick+"_"+ABCDversion+"_"+WP+"""_""" + truesig + """.root

"""  

  scriptname='submit_scripts/scripts/'+SignalNick+'_'+ABCDversion+'_'+WP+'_' + truesig + '.sh'
  f=open(scriptname,'w')
  f.write(script)
  f.close()
  st = os.stat(scriptname)
  os.chmod(scriptname, st.st_mode | stat.S_IEXEC)


def make_submissionscripts_for_MaxLikelyhoodFits(SignalNick,expectedSignal,ABCDversion,WP,truesignal):
    
  cmsswpath='/nfs/dust/cms/user/skudella/CMSSW_7_4_7'
  
  script="#!/bin/bash \n"
  if cmsswpath!='':
    script+="export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch \n"
    script+="source $VO_CMS_SW_DIR/cmsset_default.sh \n"
    script+="export SCRAM_ARCH="+os.environ['SCRAM_ARCH']+"\n"
    script+="cd "+cmsswpath+"/src\neval `scram runtime -sh`\n"
    script+="cd - \n"
    script+="""export PROCESSNAME="MaxlikelihoodFit_"""+SignalNick+"_"+ABCDversion+"_"+WP+""""\n"""


  script+="""
cd /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/"""+SignalNick+"_"+ABCDversion+"_"+WP+"""
mkdir MaxLikelihood_wAsimov_wSig
cd MaxLikelihood_wAsimov_wSig
eval `combine -M MaxLikelihoodFit --minimizerStrategy 0 --minimizerTolerance 0.0001 --rMin -"""+str(expectedSignal)+""" --rMax """+str(expectedSignal*4)+""" -t -1 --expectSignal """+str(expectedSignal)+""" --saveNormalizations --saveShapes --plots -n _MaxLikelihood_wAsimov_wSig ../"""+SignalNick+"_"+ABCDversion+"_"+WP+"""_noSignal.root`
cd ..
mkdir MaxLikelihood_wAsimov_nSig
cd MaxLikelihood_wAsimov_nSig
eval `combine -M MaxLikelihoodFit --minimizerStrategy 0 --minimizerTolerance 0.0001 --rMin -"""+str(expectedSignal)+""" --rMax """+str(expectedSignal*4)+""" -t -1 --expectSignal 0 --saveNormalizations --saveShapes --plots -n _MaxLikelihood_wAsimov_nSig ../"""+SignalNick+"_"+ABCDversion+"_"+WP+"""_noSignal.root`
cd ..


mkdir MaxLikelihood_nAsimov_nSig
cd MaxLikelihood_nAsimov_nSig
eval `combine -M MaxLikelihoodFit --minimizerStrategy 0 --minimizerTolerance 0.0001 --rMin -"""+str(expectedSignal)+""" --rMax """+str(expectedSignal*4)+""" --saveNormalizations --saveShapes --plots -n _MaxLikelihood_nAsimov_nSig ../"""+SignalNick+"_"+ABCDversion+"_"+WP+"""_noSignal.root`
cd ..
mkdir MaxLikelihood_nAsimov_wSig
cd MaxLikelihood_nAsimov_wSig
eval `combine -M MaxLikelihoodFit --minimizerStrategy 0 --minimizerTolerance 0.0001 --rMin -"""+str(expectedSignal)+""" --rMax """+str(expectedSignal*4)+""" --saveNormalizations --saveShapes --plots -n _MaxLikelihood_nAsimov_wSig ../"""+SignalNick+"_"+ABCDversion+"_"+WP+"""_""" + truesignal + """.root`
cd ..
"""

  #script+="""
#mkdir MaxLikelihood_Toy_wSig
#cd MaxLikelihood_Toy_wSig
#eval `combine -M MaxLikelihoodFit --minimizerStrategy 0 --minimizerTolerance 0.0001 --rMin -"""+str(expectedSignal)+""" --rMax """+str(expectedSignal*4)+""" -t 1000 --expectSignal """+str(expectedSignal)+""" --saveNormalizations --saveShapes --plots -n _MaxLikelihood_Toy_wSig ../"""+SignalNick+"_"+ABCDversion+"_"+WP+"""_noSignal.root`
#cd ..
#mkdir MaxLikelihood_Toy_nSig
#cd MaxLikelihood_Toy_nSig
#eval `combine -M MaxLikelihoodFit --minimizerStrategy 0 --minimizerTolerance 0.0001 --rMin -"""+str(expectedSignal)+""" --rMax """+str(expectedSignal*4)+""" -t 1000 --expectSignal 0 --saveNormalizations --saveShapes --plots -n _MaxLikelihood_Toy_nSig ../"""+SignalNick+"_"+ABCDversion+"_"+WP+"""_noSignal.root`
#cd ..
#"""  

  scriptname='submit_scripts/maxlikelihoodfit_scripts/MaxlikelihoodFit_'+SignalNick+'_'+ABCDversion+'_'+WP+'.sh'
  f=open(scriptname,'w')
  f.write(script)
  f.close()
  st = os.stat(scriptname)
  os.chmod(scriptname, st.st_mode | stat.S_IEXEC)

def make_submissionscripts_for_AsymptoticFits(SignalNick,expectedSignal,ABCDversion,WP):
    
  cmsswpath='/nfs/dust/cms/user/skudella/CMSSW_7_4_7'
  
  script="#!/bin/bash \n"
  if cmsswpath!='':
    script+="export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch \n"
    script+="source $VO_CMS_SW_DIR/cmsset_default.sh \n"
    script+="export SCRAM_ARCH="+os.environ['SCRAM_ARCH']+"\n"
    script+="cd "+cmsswpath+"/src\neval `scram runtime -sh`\n"
    script+="cd - \n"
    script+="""export PROCESSNAME="AsymptoticFit_"""+SignalNick+"_"+ABCDversion+"_"+WP+""""\n"""


  script+="""
cd /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/"""+SignalNick+"_"+ABCDversion+"_"+WP+"""
mkdir Asymptotic
cd Asymptotic
eval `combine -M Asymptotic --minosAlgo stepping --minimizerTolerance """ + str(expectedSignal*0.000001) + """ --run blind --rMin -""" + str(expectedSignal) + """ --rMax """ + str(expectedSignal*4) + """ -n _Asymptotic ../"""+SignalNick+"_"+ABCDversion+"_"+WP+"""_noSignal.root`

cp /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/impact_tab.py .

mkdir no_ABCD
cd no_ABCD
eval `combine -M Asymptotic --minosAlgo stepping --minimizerTolerance """ + str(expectedSignal*0.000001) + """ --run blind --rMin -""" + str(expectedSignal) + """ --rMax """ + str(expectedSignal*4) + """ -n _Asymptotic --freezeNuisances QCD_ABCD_shape_wtb,QCD_ABCD_shape_ntb,QCD_ABCD_rate_wtb,QCD_ABCD_rate_ntb ../../"""+SignalNick+"_"+ABCDversion+"_"+WP+"""_noSignal.root`
cd ..

mkdir no_btag
cd no_btag
eval `combine -M Asymptotic --minosAlgo stepping --minimizerTolerance """ + str(expectedSignal*0.000001) + """ --run blind --rMin -""" + str(expectedSignal) + """ --rMax """ + str(expectedSignal*4) + """ -n _Asymptotic --freezeNuisances MCSF_CSVLF,MCSF_CSVHF,MCSF_CSVHFStats1,MCSF_CSVLFStats1,MCSF_CSVHFStats2,MCSF_CSVLFStats2,MCSF_CSVCErr1,MCSF_CSVCErr2 ../../"""+SignalNick+"_"+ABCDversion+"_"+WP+"""_noSignal.root`
cd ..

mkdir no_ttag
cd no_ttag
eval `combine -M Asymptotic --minosAlgo stepping --minimizerTolerance """ + str(expectedSignal*0.000001) + """ --run blind --rMin -""" + str(expectedSignal) + """ --rMax """ + str(expectedSignal*4) + """ -n _Asymptotic --freezeNuisances MCSF_toptag,MCSF_topmisstag ../../"""+SignalNick+"_"+ABCDversion+"_"+WP+"""_noSignal.root`
cd ..

mkdir no_Wtag
cd no_Wtag
eval `combine -M Asymptotic --minosAlgo stepping --minimizerTolerance """ + str(expectedSignal*0.000001) + """ --run blind --rMin -""" + str(expectedSignal) + """ --rMax """ + str(expectedSignal*4) + """ -n _Asymptotic --freezeNuisances MCSF_Wtag, ../../"""+SignalNick+"_"+ABCDversion+"_"+WP+"""_noSignal.root`
cd ..

mkdir no_theory
cd no_theory
eval `combine -M Asymptotic --minosAlgo stepping --minimizerTolerance """ + str(expectedSignal*0.000001) + """ --run blind --rMin -""" + str(expectedSignal) + """ --rMax """ + str(expectedSignal*4) + """ -n _Asymptotic --freezeNuisances MCSF_PDF,MCSF_renfac_env,ttbarXS ../../"""+SignalNick+"_"+ABCDversion+"_"+WP+"""_noSignal.root`
cd ..

mkdir no_JEC
cd no_JEC
eval `combine -M Asymptotic --minosAlgo stepping --minimizerTolerance """ + str(expectedSignal*0.000001) + """ --run blind --rMin -""" + str(expectedSignal) + """ --rMax """ + str(expectedSignal*4) + """ -n _Asymptotic --freezeNuisances nominal_JER,nominal_JES ../../"""+SignalNick+"_"+ABCDversion+"_"+WP+"""_noSignal.root`
cd ..

mkdir no_exp
cd no_exp
eval `combine -M Asymptotic --minosAlgo stepping --minimizerTolerance """ + str(expectedSignal*0.000001) + """ --run blind --rMin -""" + str(expectedSignal) + """ --rMax """ + str(expectedSignal*4) + """ -n _Asymptotic --freezeNuisances MCSF_PU,MCSF_Lumi,MCSF_Trigger ../../"""+SignalNick+"_"+ABCDversion+"_"+WP+"""_noSignal.root`
cd ..

mkdir no_MCstat
cd no_MCstat
eval `combine -M Asymptotic --minosAlgo stepping --minimizerTolerance """ + str(expectedSignal*0.000001) + """ --run blind --rMin -""" + str(expectedSignal) + """ --rMax """ + str(expectedSignal*4) + """ -n _Asymptotic --freezeNuisances *tb_stat_bin* ../../"""+SignalNick+"_"+ABCDversion+"_"+WP+"""_noSignal.root`
cd ..

mkdir no_syst
cd no_syst
eval `combine -M Asymptotic --minosAlgo stepping --minimizerTolerance """ + str(expectedSignal*0.000001) + """ --run blind --rMin -""" + str(expectedSignal) + """ --rMax """ + str(expectedSignal*4) + """ -n _Asymptotic --freezeNuisances MCSF_PU,MCSF_Lumi,MCSF_Trigger,QCD_ABCD_shape_wtb,QCD_ABCD_shape_ntb,QCD_ABCD_rate_wtb,QCD_ABCD_rate_ntb,MCSF_CSVLF,MCSF_CSVHF,MCSF_CSVHFStats1,MCSF_CSVLFStats1,MCSF_CSVHFStats2,MCSF_CSVLFStats2,MCSF_CSVCErr1,MCSF_CSVCErr2,MCSF_toptag,MCSF_topmisstag,nominal_JER,nominal_JES,MCSF_PDF,MCSF_renfac_env,ttbarXS,MCSF_Wtag ../../"""+SignalNick+"_"+ABCDversion+"_"+WP+"""_noSignal.root`
cd ..



python impact_tab.py

"""  

  scriptname='submit_scripts/asymptoticfit_scripts/AsymptoticFit_'+SignalNick+'_'+ABCDversion+'_'+WP+'.sh'
  f=open(scriptname,'w')
  f.write(script)
  f.close()
  st = os.stat(scriptname)
  os.chmod(scriptname, st.st_mode | stat.S_IEXEC)



def make_submissionscripts_for_resultplots(SignalNick,expectedSignal,ABCDversion,WP):
    
  cmsswpath='/nfs/dust/cms/user/skudella/CMSSW_7_4_7'
  
  script="#!/bin/bash \n"
  if cmsswpath!='':
    script+="export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch \n"
    script+="source $VO_CMS_SW_DIR/cmsset_default.sh \n"
    script+="export SCRAM_ARCH="+os.environ['SCRAM_ARCH']+"\n"
    script+="cd "+cmsswpath+"/src\neval `scram runtime -sh`\n"
    script+="cd - \n"
    script+="""export PROCESSNAME="FitAnalysis_"""+SignalNick+"_"+ABCDversion+"_"+WP+""""\n"""


  script+="""
cd /nfs/dust/cms/user/skudella/CombineFitTests/PseudoDataTests/scripts/
./runPlotResults.sh /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/"""+SignalNick+"_"+ABCDversion+"_"+WP+"""/MaxLikelihood_nAsimov/mlfit_MaxLikelihood_nAsimov_nSig.root "" "1" 
cd /nfs/dust/cms/user/skudella/CombineFitTests/PseudoDataTests/scripts/
./runPlotResults.sh /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/"""+SignalNick+"_"+ABCDversion+"_"+WP+"""/MaxLikelihood_nAsimov/mlfit_MaxLikelihood_nAsimov_wSig.root "" "1" 
./runPlotResults.sh /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/"""+SignalNick+"_"+ABCDversion+"_"+WP+"""/MaxLikelihood_wAsimov_nSig/mlfit_MaxLikelihood_wAsimov_nSig.root "" "1" 
./runPlotResults.sh /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/"""+SignalNick+"_"+ABCDversion+"_"+WP+"""/MaxLikelihood_wAsimov_wSig/mlfit_MaxLikelihood_wAsimov_wSig.root "" "1"  

cd /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/"""+SignalNick+"_"+ABCDversion+"_"+WP+"""
cd MaxLikelihood_nAsimov; 
python /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/scripts/diffNuisances.py -g nAsimov_minosall_"""+SignalNick+"_"+ABCDversion+"_"+WP+""" mlfit_MaxLikelihood_nAsimov_nSig.root
cd .. 
cd MaxLikelihood_nAsimov; 
python /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/scripts/diffNuisances.py -g nAsimov_minosall_"""+SignalNick+"_"+ABCDversion+"_"+WP+""" mlfit_MaxLikelihood_nAsimov_wSig.root
cd .. 

cd MaxLikelihood_wAsimov_nSig
python /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/scripts/diffNuisances.py -g wAsimov_nSig_minosall_"""+SignalNick+"_"+ABCDversion+"_"+WP+""" mlfit_MaxLikelihood_wAsimov_nSig.root
cd ..
cd MaxLikelihood_wAsimov_wSig
python /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/scripts/diffNuisances.py -g wAsimov_wSig_minosall_"""+SignalNick+"_"+ABCDversion+"_"+WP+""" mlfit_MaxLikelihood_wAsimov_wSig.root
cd ..



"""  

  scriptname='submit_scripts/finanalysis_scripts/FitAnalysis_'+SignalNick+'_'+ABCDversion+'_'+WP+'.sh'
  f=open(scriptname,'w')
  f.write(script)
  f.close()
  st = os.stat(scriptname)
  os.chmod(scriptname, st.st_mode | stat.S_IEXEC)





def make_submissionscripts_for_impact_on_limits_plots(SignalNick,expectedSignal,ABCDversion,WP):
    
  cmsswpath='/nfs/dust/cms/user/skudella/CMSSW_7_4_7'
  
  script="#!/bin/bash \n"
  if cmsswpath!='':
    script+="export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch \n"
    script+="source $VO_CMS_SW_DIR/cmsset_default.sh \n"
    script+="export SCRAM_ARCH="+os.environ['SCRAM_ARCH']+"\n"
    script+="cd "+cmsswpath+"/src\neval `scram runtime -sh`\n"
    script+="cd - \n"
    script+="""export PROCESSNAME="FitAnalysis_"""+SignalNick+"_"+ABCDversion+"_"+WP+""""\n"""


  script+="""




"""  

  scriptname='submit_scripts/finanalysis_scripts/FitAnalysis_'+SignalNick+'_'+ABCDversion+'_'+WP+'.sh'
  f=open(scriptname,'w')
  f.write(script)
  f.close()
  st = os.stat(scriptname)
  os.chmod(scriptname, st.st_mode | stat.S_IEXEC)





################################################### Define ABCD systematic uncertainties #############


##################################################### Script starts here ######################


print "Creating Ccode for Workspacefiles"

cmsswpath="/nfs/dust/cms/user/skudella/CMSSW_7_4_7"

indir = "/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/"
outdir= "/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/"





   
systlist=["nominal","MCSF_CSVLFUp","MCSF_CSVHFUp","MCSF_CSVHFStats1Up","MCSF_CSVLFStats1Up","MCSF_CSVHFStats2Up","MCSF_CSVLFStats2Up","MCSF_CSVCErr1Up","MCSF_CSVCErr2Up","MCSF_toptagUp","MCSF_WtagUp","MCSF_PUUp","MCSF_PDFUp","MCSF_LumiUp","MCSF_TriggerUp","MCSF_renfac_envUp","nominal_JERUp","nominal_JESUp","ttbarXSUp","MCSF_CSVLFDown","MCSF_CSVHFDown","MCSF_CSVHFStats1Down","MCSF_CSVLFStats1Down","MCSF_CSVHFStats2Down","MCSF_CSVLFStats2Down","MCSF_CSVCErr1Down","MCSF_CSVCErr2Down","MCSF_toptagDown","MCSF_WtagDown","MCSF_PUDown","MCSF_PDFDown","MCSF_LumiDown","MCSF_TriggerDown","MCSF_renfac_envDown","nominal_JERDown","nominal_JESDown","ttbarXSDown"]
    
    

print 'Creating datacards'

cmsswpath='/nfs/dust/cms/user/skudella/CMSSW_7_4_7'
#SignalNickList=["SigZprime15001200_tWb"]
SignalNickList=["SigZprime15001200_tWb","SigZprime20001200_tWb","SigZprime25001200_tWb","SigZprime1500700_tWb","SigZprime1500900_tWb","SigZprime2000900_tWb","SigZprime20001500_tWb","SigZprime25001500_tWb"]+["SigZprime15001200_ttZ","SigZprime20001200_ttZ","SigZprime25001200_ttZ","SigZprime1500700_ttZ","SigZprime1500900_ttZ","SigZprime2000900_ttZ","SigZprime20001500_ttZ","SigZprime25001500_ttZ"]+["SigZprime15001200_ttH","SigZprime20001200_ttH","SigZprime25001200_ttH","SigZprime1500700_ttH","SigZprime1500900_ttH","SigZprime2000900_ttH","SigZprime20001500_ttH","SigZprime25001500_ttH"]+["SigZprime15001200_BR05_025_025","SigZprime20001200_BR05_025_025","SigZprime25001200_BR05_025_025","SigZprime1500700_BR05_025_025","SigZprime1500900_BR05_025_025","SigZprime2000900_BR05_025_025","SigZprime20001500_BR05_025_025","SigZprime25001500_BR05_025_025"]

Truesignallist=[]
for i in SignalNickList:
    print i[3:]
    Truesignallist.append(i[3:]+"_1pb")

SignalNickList=["Zprime15001200_BR05_025_025","SigZprime20001200_tWb","SigZprime25001200_tWb","SigZprime1500700_tWb","SigZprime1500900_tWb","SigZprime2000900_tWb","SigZprime20001500_tWb","SigZprime25001500_tWb"]+["SigZprime15001200_ttZ","SigZprime20001200_ttZ","SigZprime25001200_ttZ","SigZprime1500700_ttZ","SigZprime1500900_ttZ","SigZprime2000900_ttZ","SigZprime20001500_ttZ","SigZprime25001500_ttZ"]+["SigZprime15001200_ttH","SigZprime20001200_ttH","SigZprime25001200_ttH","SigZprime1500700_ttH","SigZprime1500900_ttH","SigZprime2000900_ttH","SigZprime20001500_ttH","SigZprime25001500_ttH"]+["SigZprime15001200_BR05_025_025","SigZprime20001200_BR05_025_025","SigZprime25001200_BR05_025_025","SigZprime1500700_BR05_025_025","SigZprime1500900_BR05_025_025","SigZprime2000900_BR05_025_025","SigZprime20001500_BR05_025_025","SigZprime25001500_BR05_025_025"]


expectedSignals=[8.6,0.27,0.33,0.8,1.5,0.21,0.9,0.29]+[3.1,0.29,0.18,3.1,2.4,0.4,0.33,0.13]+[11,0.54,0.26,3.5,2.6,0.56,0.59,0.22]+[8.6,0.27,0.33,0.8,1.5,0.21,0.9,0.29]

ABCDversion='ABCD5'
    
    
#for WP in ['CMS_WP','Anna_WP','CMS_WP_nodynEvtHT','Anna_WP_nodynEvtHT']:
#for WP in ['CMS_WP','Anna_WP','CMS_WP_nodynEvtHT']:
for WP in ['CMS_WP']:
    

    pathToOutputRootFile=indir + "/rootfiles/output_rebinned_added_"+ WP + ".root"
    f=ROOT.TFile(pathToOutputRootFile, "readonly")
    #print "looking at file ", 
    keyList = f.GetKeyNames()    
    for key in keyList:
        if ("DATA_noSignal" in key) and ("ABCD" in key) and ("nominal" in key) and ("Tprime" not in key) and ("inclusive" not in key) and ("Zprime_M" in key) and ("CatA" in key):
            datahisto=f.Get(key)
            print key, " selected to extract binning"
            break

    nbins=datahisto.GetNbinsX()

    rebin=1
    print "number of mass bins=", nbins    
    nbins=nbins/rebin
    print "rebinning to ", nbins

    #if WP=='Anna_WP':
                #Zprime_withtopbtag_systrate=0.0437729147047
                #Zprime_withtopbtag_systshape_m=-0.00000748147
                #Zprime_withtopbtag_systshape_c=0.959254
                #Zprime_notopbtag_systrate=0.0416820871399
                #Zprime_notopbtag_systshape_m=-0.0000748556
                #Zprime_notopbtag_systshape_c=1.111           
    #elif WP=='Anna_WP_nodynEvtHT':
                #Zprime_withtopbtag_systrate=0.026335429083
                #Zprime_withtopbtag_systshape_m=-0.000014237
                #Zprime_withtopbtag_systshape_c=1.01372
                #Zprime_notopbtag_systrate=0.025035741394
                #Zprime_notopbtag_systshape_m=-0.0000563142
                #Zprime_notopbtag_systshape_c=1.10324

    #elif WP=='CMS_WP':
                #Zprime_withtopbtag_systrate=0.0726471275379
                #Zprime_withtopbtag_systshape_m=0.000169601
                #Zprime_withtopbtag_systshape_c=0.696039
                #Zprime_notopbtag_systrate=0.0524079950827
                #Zprime_notopbtag_systshape_m=-0.000100387
                #Zprime_notopbtag_systshape_c=1.15173
    #elif WP=='CMS_WP_nodynEvtHT':
                #Zprime_withtopbtag_systrate=0.0615567929662
                #Zprime_withtopbtag_systshape_m=0.0000820445
                #Zprime_withtopbtag_systshape_c=0.815448
                #Zprime_notopbtag_systrate=0.0237731064005
                #Zprime_notopbtag_systshape_m=-0.000079382
                #Zprime_notopbtag_systshape_c=1.14017    
    #else:
        #print "heyo sucker"
        
    if WP=='Anna_WP':
                Zprime_withtopbtag_systrate=0.0437729147047
                Zprime_withtopbtag_systshape_m=-0.00000748147
                Zprime_withtopbtag_systshape_c=0.959254
                Zprime_notopbtag_systrate=0.0416820871399
                Zprime_notopbtag_systshape_m=-0.0000748556
                Zprime_notopbtag_systshape_c=1.111           
    elif WP=='Anna_WP_nodynEvtHT':
                Zprime_withtopbtag_systrate=0.0335348181752
                Zprime_withtopbtag_systshape_m=-1.16906e-05
                Zprime_withtopbtag_systshape_c=1.0233
                Zprime_notopbtag_systrate=0.0271682682657
                Zprime_notopbtag_systshape_m=-5.7266e-05
                Zprime_notopbtag_systshape_c=1.12188

    elif WP=='CMS_WP':               
                Zprime_withtopbtag_systrate=0.0259999485517
                Zprime_withtopbtag_systshape_m=-7.12241e-05
                Zprime_withtopbtag_systshape_c=1.12496
                Zprime_notopbtag_systrate=0.0347918985761 
                Zprime_notopbtag_systshape_m=-5.71104e-05
                Zprime_notopbtag_systshape_c=1.09896       
    elif WP=='CMS_WP_nodynEvtHT':
                Zprime_withtopbtag_systrate=0.0557880400592
                Zprime_withtopbtag_systshape_m=9.63432e-05
                Zprime_withtopbtag_systshape_c=0.806708
                Zprime_notopbtag_systrate=0.0278269539093
                Zprime_notopbtag_systshape_m=-6.73068e-05
                Zprime_notopbtag_systshape_c=1.1409    
    else:
        print "heyo sucker"
    
    for SignalNick,expectedSignal,truesignal in zip(SignalNickList,expectedSignals,Truesignallist):    
        make_submissionscripts_for_MaxLikelyhoodFits(SignalNick,expectedSignal,ABCDversion,WP,truesignal)
        make_submissionscripts_for_AsymptoticFits(SignalNick,expectedSignal,ABCDversion,WP)
        make_submissionscripts_for_resultplots(SignalNick,expectedSignal,ABCDversion,WP)
        
        for truesig in [truesignal,"noSignal"]:
            createScript(ABCDversion,SignalNick,WP,truesig)
            createCcode(pathToOutputRootFile,nbins,rebin,SignalNick,WP,systlist,truesig)
            make_submissionscripts_for_workspaces(SignalNick,ABCDversion,WP,truesig)        
