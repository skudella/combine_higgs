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


def Get_ABCD_data_histos(pathToOutputRootFile):
    
    f=ROOT.TFile(pathToOutputRootFile, "readonly")
    histoA_wtb=f.Get("DATA_2016_ABCD5_withtopbtag_CatA_Zprime_M_ABCD5_nominal")
    histoB_wtb=f.Get("DATA_2016_ABCD5_withtopbtag_CatB_Zprime_M_ABCD5_nominal")    
    histoC_wtb=f.Get("DATA_2016_ABCD5_withtopbtag_CatC_Zprime_M_ABCD5_nominal")    
    histoD_wtb=f.Get("DATA_2016_ABCD5_withtopbtag_CatD_Zprime_M_ABCD5_nominal") 
    histoA_ntb=f.Get("DATA_2016_ABCD5_notopbtag_CatA_Zprime_M_ABCD5_nominal")
    histoB_ntb=f.Get("DATA_2016_ABCD5_notopbtag_CatB_Zprime_M_ABCD5_nominal")    
    histoC_ntb=f.Get("DATA_2016_ABCD5_notopbtag_CatC_Zprime_M_ABCD5_nominal")    
    histoD_ntb=f.Get("DATA_2016_ABCD5_notopbtag_CatD_Zprime_M_ABCD5_nominal")
    #print histoA_wtb
    
    return [histoA_wtb,histoB_wtb,histoC_wtb,histoD_wtb,histoA_ntb,histoB_ntb,histoC_ntb,histoD_ntb]
    
def Get_x_mean(histoA,histoB,histoC,histoD):
    x0ABCD2=0.0
    x0widABCD2=0.0
    for i in range(histoA.GetNbinsX()):
        if histoA.GetBinContent(i)>0 and histoB.GetBinContent(i)>0 and histoC.GetBinContent(i)>0 and histoD.GetBinContent(i)>0:
            x0ABCD2=x0ABCD2+histoA.GetBinCenter(i)/(1.0/histoA.GetBinContent(i)+1.0/histoB.GetBinContent(i)+1.0/histoC.GetBinContent(i)+1.0/histoA.GetBinContent(i))
            x0widABCD2=x0widABCD2+1.0/(1.0/histoA.GetBinContent(i)+1.0/histoB.GetBinContent(i)+1.0/histoC.GetBinContent(i)+1.0/histoA.GetBinContent(i))
    x0ABCD2=x0ABCD2/x0widABCD2
    print "x0ABCD2",x0ABCD2
    
    return x0ABCD2


def createCcode_DATA_BKG(pathToOutputRootFile,nbins,systlist=[]):


    f=ROOT.TFile(pathToOutputRootFile, "readonly")
    histoA_wtb=f.Get("DATA_2016_ABCD5_withtopbtag_CatA_Zprime_M_ABCD5_nominal")
    histoB_wtb=f.Get("DATA_2016_ABCD5_withtopbtag_CatB_Zprime_M_ABCD5_nominal")    
    histoC_wtb=f.Get("DATA_2016_ABCD5_withtopbtag_CatC_Zprime_M_ABCD5_nominal")    
    histoD_wtb=f.Get("DATA_2016_ABCD5_withtopbtag_CatD_Zprime_M_ABCD5_nominal") 
    histoA_ntb=f.Get("DATA_2016_ABCD5_notopbtag_CatA_Zprime_M_ABCD5_nominal")
    histoB_ntb=f.Get("DATA_2016_ABCD5_notopbtag_CatB_Zprime_M_ABCD5_nominal")    
    histoC_ntb=f.Get("DATA_2016_ABCD5_notopbtag_CatC_Zprime_M_ABCD5_nominal")    
    histoD_ntb=f.Get("DATA_2016_ABCD5_notopbtag_CatD_Zprime_M_ABCD5_nominal")

    #x0_wtb=Get_x_mean(histolist[0],histolist[1],histolist[2],histolist[3])
    #x0_ntb=Get_x_mean(histolist[4],histolist[5],histolist[6],histolist[7])
    x0_wtb=Get_x_mean(histoA_wtb,histoB_wtb,histoC_wtb,histoD_wtb)
    x0_ntb=Get_x_mean(histoA_ntb,histoB_ntb,histoC_ntb,histoD_ntb)

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
//#include <../../../../../interface/RooParametricHist.h>
#include "../../../../../interface/RooParametricHist.h"
#include <RooAddition.h>
#include <TFile.h>
#include <iostream>

    
void createABCDCombineWorkspaceFile_DATA_BKG(){





    // As usual, load the combine library to get access to the RooParametricHist
    gSystem->Load("libHiggsAnalysisCombinedLimit.so");
    // Output file and workspace 
    TFile *fOut = new TFile("/nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root","RECREATE");
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
    file->GetObject("DATA_2016_ABCD5_withtopbtag_CatA_Zprime_M_ABCD5_nominal", datahistoA_wtb);
    file->GetObject("DATA_2016_ABCD5_withtopbtag_CatB_Zprime_M_ABCD5_nominal", datahistoB_wtb);
    file->GetObject("DATA_2016_ABCD5_withtopbtag_CatC_Zprime_M_ABCD5_nominal", datahistoC_wtb);
    file->GetObject("DATA_2016_ABCD5_withtopbtag_CatD_Zprime_M_ABCD5_nominal", datahistoD_wtb);
    file->GetObject("DATA_2016_ABCD5_notopbtag_CatA_Zprime_M_ABCD5_nominal", datahistoA_ntb);
    file->GetObject("DATA_2016_ABCD5_notopbtag_CatB_Zprime_M_ABCD5_nominal", datahistoB_ntb);
    file->GetObject("DATA_2016_ABCD5_notopbtag_CatC_Zprime_M_ABCD5_nominal", datahistoC_ntb);
    file->GetObject("DATA_2016_ABCD5_notopbtag_CatD_Zprime_M_ABCD5_nominal", datahistoD_ntb);

    

    
    std::vector <float> Zprime_M_bins;
    for(int i=1; i<datahistoA_wtb->GetNbinsX()+1;i++){
        std::cout<<i<<std::endl;
        Zprime_M_bins.push_back(datahistoA_wtb->GetBinCenter(i));
        std::cout<<datahistoA_wtb->GetBinCenter(i)<<std::endl;
    }


 
"""

    for syst in systlist:
        #for updown in ["Up","Down"]:
            #if ('renfac' in syst) or ('PDF' in syst):
            if ('PDF' in syst):
                #systname=syst+'_BKG'
                systname1=syst
                #systname2=syst+'_BKG'
                if ('Up' in syst):
                    systname2=syst.replace("Up","_BKGUp")
                if ('Down' in syst):
                    systname2=syst.replace("Down","_BKGDown")
                
            else:
                systname1=syst
                systname2=syst
            #print systname2
            script+="""
    //std::cout<<"here 1 """+syst+""" "<<std::endl;       
    TH1 * ttbarhistoA_wtb_""" + systname1 + """ = 0;
    TH1 * ttbarhistoB_wtb_""" + systname1 + """ = 0;
    TH1 * ttbarhistoC_wtb_""" + systname1 + """ = 0;
    TH1 * ttbarhistoD_wtb_""" + systname1 + """ = 0;
    TH1 * ttbarhistoA_ntb_""" + systname1 + """ = 0;
    TH1 * ttbarhistoB_ntb_""" + systname1 + """ = 0;
    TH1 * ttbarhistoC_ntb_""" + systname1 + """ = 0;
    TH1 * ttbarhistoD_ntb_""" + systname1 + """ = 0;


   
    file->GetObject("ttbar_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_""" + systname1 + """", ttbarhistoA_wtb_""" + systname1 + """);
    file->GetObject("ttbar_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """_""" + systname1 + """", ttbarhistoB_wtb_""" + systname1 + """);
    file->GetObject("ttbar_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + """_""" + systname1 + """", ttbarhistoC_wtb_""" + systname1 + """);
    file->GetObject("ttbar_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + """_""" + systname1 + """", ttbarhistoD_wtb_""" + systname1 + """);
    file->GetObject("ttbar_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_""" + systname1 + """", ttbarhistoA_ntb_""" + systname1 + """);
    file->GetObject("ttbar_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """_""" + systname1 + """", ttbarhistoB_ntb_""" + systname1 + """);
    file->GetObject("ttbar_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + """_""" + systname1 + """", ttbarhistoC_ntb_""" + systname1 + """);
    file->GetObject("ttbar_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + """_""" + systname1 + """", ttbarhistoD_ntb_""" + systname1 + """);                
            
    //std::cout<<"here 1.1 """+syst+""" "<<std::endl;       
    //std::cout<<"ttbar_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_""" + systname1 + """"<<std::endl;       

            
    RooDataHist ttbar_histA_wtb_""" + systname2 + """("ttbar_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + "_" + systname2 + """","ttbar_""" + systname1 + """",vars,ttbarhistoA_wtb_""" + systname1 + """);
    RooDataHist ttbar_histB_wtb_""" + systname2 + """("ttbar_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + "_" + systname2 + """","ttbar_""" + systname1 + """",vars,ttbarhistoB_wtb_""" + systname1 + """);
    RooDataHist ttbar_histC_wtb_""" + systname2 + """("ttbar_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + "_" + systname2 + """","ttbar_""" + systname1 + """",vars,ttbarhistoC_wtb_""" + systname1 + """);
    RooDataHist ttbar_histD_wtb_""" + systname2 + """("ttbar_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + "_" + systname2 + """","ttbar_""" + systname1 + """",vars,ttbarhistoD_wtb_""" + systname1 + """);
    RooDataHist ttbar_histA_ntb_""" + systname2 + """("ttbar_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + "_" + systname2 + """","ttbar_""" + systname1 + """",vars,ttbarhistoA_ntb_""" + systname1 + """);
    RooDataHist ttbar_histB_ntb_""" + systname2 + """("ttbar_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + "_" + systname2 + """","ttbar_""" + systname1 + """",vars,ttbarhistoB_ntb_""" + systname1 + """);
    RooDataHist ttbar_histC_ntb_""" + systname2 + """("ttbar_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + "_" + systname2 + """","ttbar_""" + systname1 + """",vars,ttbarhistoC_ntb_""" + systname1 + """);
    RooDataHist ttbar_histD_ntb_""" + systname2 + """("ttbar_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + "_" + systname2 + """","ttbar_""" + systname1 + """",vars,ttbarhistoD_ntb_""" + systname1 + """);
    
    //std::cout<<"here 1.2 """+syst+""" "<<std::endl;       
    
    wspace.import(ttbar_histA_wtb_""" + systname2 + """);
    wspace.import(ttbar_histB_wtb_""" + systname2 + """);
    wspace.import(ttbar_histC_wtb_""" + systname2 + """);
    wspace.import(ttbar_histD_wtb_""" + systname2 + """);
    wspace.import(ttbar_histA_ntb_""" + systname2 + """);
    wspace.import(ttbar_histB_ntb_""" + systname2 + """);
    wspace.import(ttbar_histC_ntb_""" + systname2 + """);
    wspace.import(ttbar_histD_ntb_""" + systname2 + """);
    
    //std::cout<<"here 2 """+syst+""" "<<std::endl;       
    
"""
            if (syst=='nominal'):
                for l in range(1,nbins+1):
                  for var in  ["Up","Down"]:
                    systname="_stat_bin"+str(l)+var
                    script+="""
                    
    //std::cout<<"here 3"<<std::endl;       
    TH1 *ttbarhistoA_wtb_ttbarMC_Awtb""" + systname + """ = (TH1*)ttbarhistoA_wtb_""" + syst + """->Clone("ttbar_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + "_ttbarMC_Awtb" + systname + """"); 
    TH1 *ttbarhistoB_wtb_ttbarMC_Bwtb""" + systname + """ = (TH1*)ttbarhistoB_wtb_""" + syst + """->Clone("ttbar_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + "_ttbarMC_Bwtb" + systname + """"); 
    TH1 *ttbarhistoC_wtb_ttbarMC_Cwtb""" + systname + """ = (TH1*)ttbarhistoC_wtb_""" + syst + """->Clone("ttbar_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + "_ttbarMC_Cwtb" + systname + """"); 
    TH1 *ttbarhistoD_wtb_ttbarMC_Dwtb""" + systname + """ = (TH1*)ttbarhistoD_wtb_""" + syst + """->Clone("ttbar_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + "_ttbarMC_Dwtb" + systname + """"); 
    TH1 *ttbarhistoA_ntb_ttbarMC_Antb""" + systname + """ = (TH1*)ttbarhistoA_ntb_""" + syst + """->Clone("ttbar_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + "_ttbarMC_Antb" + systname + """"); 
    TH1 *ttbarhistoB_ntb_ttbarMC_Bntb""" + systname + """ = (TH1*)ttbarhistoB_ntb_""" + syst + """->Clone("ttbar_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + "_ttbarMC_Bntb" + systname + """"); 
    TH1 *ttbarhistoC_ntb_ttbarMC_Cntb""" + systname + """ = (TH1*)ttbarhistoC_ntb_""" + syst + """->Clone("ttbar_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + "_ttbarMC_Cntb" + systname + """"); 
    TH1 *ttbarhistoD_ntb_ttbarMC_Dntb""" + systname + """ = (TH1*)ttbarhistoD_ntb_""" + syst + """->Clone("ttbar_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + "_ttbarMC_Dntb" + systname + """"); 
    
    //std::cout<<"here 4"<<std::endl;       
    
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

    //std::cout<<"here 5"<<std::endl;       
    
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

    //std::cout<<"here 6"<<std::endl;       


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
    
    //std::cout<<"here 7"<<std::endl;       
    
    wspace.import(ttbar_histA_wtb_ttbarMC_Awtb""" + systname + """);
    wspace.import(ttbar_histB_wtb_ttbarMC_Bwtb""" + systname + """);
    wspace.import(ttbar_histC_wtb_ttbarMC_Cwtb""" + systname + """);
    wspace.import(ttbar_histD_wtb_ttbarMC_Dwtb""" + systname + """);
    wspace.import(ttbar_histA_ntb_ttbarMC_Antb""" + systname + """);
    wspace.import(ttbar_histB_ntb_ttbarMC_Bntb""" + systname + """);
    wspace.import(ttbar_histC_ntb_ttbarMC_Cntb""" + systname + """);
    wspace.import(ttbar_histD_ntb_ttbarMC_Dntb""" + systname + """);    

"""



    script+="""

    for(int j=0; j<datahistoA_wtb->GetNbinsX()+1;j++){

        //if(datahistoA_wtb->GetBinContent(j)-ttbarhistoA_wtb_nominal->GetBinContent(j)<0.5){datahistoA_wtb->SetBinContent(j,ttbarhistoA_wtb_nominal->GetBinContent(j)*1.5+0.01);};
        //if(datahistoB_wtb->GetBinContent(j)-ttbarhistoB_wtb_nominal->GetBinContent(j)<0.5){datahistoB_wtb->SetBinContent(j,ttbarhistoB_wtb_nominal->GetBinContent(j)*1.5+0.01);};
        //if(datahistoC_wtb->GetBinContent(j)-ttbarhistoC_wtb_nominal->GetBinContent(j)<0.5){datahistoC_wtb->SetBinContent(j,ttbarhistoC_wtb_nominal->GetBinContent(j)*1.5+0.01);};
        //if(datahistoD_wtb->GetBinContent(j)-ttbarhistoD_wtb_nominal->GetBinContent(j)<0.5){datahistoD_wtb->SetBinContent(j,ttbarhistoD_wtb_nominal->GetBinContent(j)*1.5+0.01);};
        //if(datahistoA_ntb->GetBinContent(j)-ttbarhistoA_ntb_nominal->GetBinContent(j)<0.5){datahistoA_ntb->SetBinContent(j,ttbarhistoA_ntb_nominal->GetBinContent(j)*1.5+0.01);};
        //if(datahistoB_ntb->GetBinContent(j)-ttbarhistoB_ntb_nominal->GetBinContent(j)<0.5){datahistoB_ntb->SetBinContent(j,ttbarhistoB_ntb_nominal->GetBinContent(j)*1.5+0.01);};
        //if(datahistoC_ntb->GetBinContent(j)-ttbarhistoC_ntb_nominal->GetBinContent(j)<0.5){datahistoC_ntb->SetBinContent(j,ttbarhistoC_ntb_nominal->GetBinContent(j)*1.5+0.01);};
        //if(datahistoD_ntb->GetBinContent(j)-ttbarhistoD_ntb_nominal->GetBinContent(j)<0.5){datahistoD_ntb->SetBinContent(j,ttbarhistoD_ntb_nominal->GetBinContent(j)*1.5+0.01);};
        
        //if((datahistoA_wtb->GetBinContent(j)-ttbarhistoA_wtb_nominal->GetBinContent(j))<0.0001){datahistoA_wtb->SetBinContent(j,ttbarhistoA_wtb_nominal->GetBinContent(j) + 0.0001);};
        //if((datahistoB_wtb->GetBinContent(j)-ttbarhistoB_wtb_nominal->GetBinContent(j))<0.0001){datahistoB_wtb->SetBinContent(j,ttbarhistoB_wtb_nominal->GetBinContent(j) + 0.0001);};
        //if((datahistoC_wtb->GetBinContent(j)-ttbarhistoC_wtb_nominal->GetBinContent(j))<0.0001){datahistoC_wtb->SetBinContent(j,ttbarhistoC_wtb_nominal->GetBinContent(j) + 0.0001);};
        //if((datahistoD_wtb->GetBinContent(j)-ttbarhistoD_wtb_nominal->GetBinContent(j))<0.0001){datahistoD_wtb->SetBinContent(j,ttbarhistoD_wtb_nominal->GetBinContent(j) + 0.0001);};
        //if((datahistoA_ntb->GetBinContent(j)-ttbarhistoA_ntb_nominal->GetBinContent(j))<0.0001){datahistoA_ntb->SetBinContent(j,ttbarhistoA_ntb_nominal->GetBinContent(j) + 0.0001);};
        //if((datahistoB_ntb->GetBinContent(j)-ttbarhistoB_ntb_nominal->GetBinContent(j))<0.0001){datahistoB_ntb->SetBinContent(j,ttbarhistoB_ntb_nominal->GetBinContent(j) + 0.0001);};
        //if((datahistoC_ntb->GetBinContent(j)-ttbarhistoC_ntb_nominal->GetBinContent(j))<0.0001){datahistoC_ntb->SetBinContent(j,ttbarhistoC_ntb_nominal->GetBinContent(j) + 0.0001);};
        //if((datahistoD_ntb->GetBinContent(j)-ttbarhistoD_ntb_nominal->GetBinContent(j))<0.0001){datahistoD_ntb->SetBinContent(j,ttbarhistoD_ntb_nominal->GetBinContent(j) + 0.0001);};
        
        if((datahistoA_wtb->GetBinContent(j))<0.0001){datahistoA_wtb->SetBinContent(j,0.0001);};
        if((datahistoB_wtb->GetBinContent(j))<0.0001){datahistoB_wtb->SetBinContent(j,0.0001);};
        if((datahistoC_wtb->GetBinContent(j))<0.0001){datahistoC_wtb->SetBinContent(j,0.0001);};
        if((datahistoD_wtb->GetBinContent(j))<0.0001){datahistoD_wtb->SetBinContent(j,0.0001);};
        if((datahistoA_ntb->GetBinContent(j))<0.0001){datahistoA_ntb->SetBinContent(j,0.0001);};
        if((datahistoB_ntb->GetBinContent(j))<0.0001){datahistoB_ntb->SetBinContent(j,0.0001);};
        if((datahistoC_ntb->GetBinContent(j))<0.0001){datahistoC_ntb->SetBinContent(j,0.0001);};
        if((datahistoD_ntb->GetBinContent(j))<0.0001){datahistoD_ntb->SetBinContent(j,0.0001);};        
            
        
    }
    
    RooDataHist data_histA_wtb("DATA_2016_ABCD5_withtopbtag_CatA_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoA_wtb);
    RooDataHist data_histB_wtb("DATA_2016_ABCD5_withtopbtag_CatB_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoB_wtb);
    RooDataHist data_histC_wtb("DATA_2016_ABCD5_withtopbtag_CatC_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoC_wtb);
    RooDataHist data_histD_wtb("DATA_2016_ABCD5_withtopbtag_CatD_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoD_wtb);
    RooDataHist data_histA_ntb("DATA_2016_ABCD5_notopbtag_CatA_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoA_ntb);
    RooDataHist data_histB_ntb("DATA_2016_ABCD5_notopbtag_CatB_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoB_ntb);
    RooDataHist data_histC_ntb("DATA_2016_ABCD5_notopbtag_CatC_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoC_ntb);
    RooDataHist data_histD_ntb("DATA_2016_ABCD5_notopbtag_CatD_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoD_ntb);


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

    
    RooRealVar QCD_ABCD_shape_ntb("QCD_ABCD_shape_ntb","QCD_ABCD_shape_ntb",0.0,-100,100);
    RooRealVar QCD_ABCD_rate_ntb("QCD_ABCD_rate_ntb","QCD_ABCD_rate_ntb",0.0,-100,100);

    //std::cout<<"here 8"<<std::endl;   
    
    float temp=1.0;
"""

   #for Region  in ['A','B','C','D']:
     #for Category in ['wtb','ntb']:
   #script+="""
   #for(int i=0; i<22; i++){
       #RooRealVar QCD_Cat""" + Region + """_""" + Category + """_bin("QCD_Cat""" + Region + """_""" + Category + """_bin" + std::str(i),"QCD Background yield in signal region with top-btag, bin1" + std::str(i),1,0,1000);
       #QCD_Cat""" + Region + """_""" + Category + """_bins.add(QCD_Cat""" + Region + """_""" + Category + """_bin); 
       
   #}
           
#"""


    for i in range(1,nbins):
        script+="""
    //RooRealVar Bin_Mass_bin""" +  str(i) + """("Bin_Mass_bin""" +  str(i) + '"' + ""","Bin Mass, bin""" +  str(i) + '"' + """,1,0,100000);
    //RooRealVar QCD_CatB_wtb_bin""" +  str(i) + """("QCD_CatB_wtb_bin""" +  str(i) + '"' + ""","QCD Background region B with top-btag, bin""" +  str(i) + '"' + """,""" + str(datahisto.GetBinContent(i)) + """,0.01,100000);
    //RooRealVar QCD_CatC_wtb_bin""" +  str(i) + """("QCD_CatC_wtb_bin""" +  str(i) + '"' + ""","QCD Background region C with top-btag, bin""" +  str(i) + '"' + """,""" + str(datahisto.GetBinContent(i)) + """,0.01,100000);
    //RooRealVar QCD_CatD_wtb_bin""" +  str(i) + """("QCD_CatD_wtb_bin""" +  str(i) + '"' + ""","QCD Background region D with top-btag, bin""" +  str(i) + '"' + """,""" + str(datahisto.GetBinContent(i)) + """,0.01,100000);
    //RooRealVar QCD_CatB_ntb_bin""" +  str(i) + """("QCD_CatB_ntb_bin""" +  str(i) + '"' + ""","QCD Background region B no top-btag, bin""" +  str(i) + '"' + """,""" + str(datahisto.GetBinContent(i)) + """,0.01,100000);
    //RooRealVar QCD_CatC_ntb_bin""" +  str(i) + """("QCD_CatC_ntb_bin""" +  str(i) + '"' + ""","QCD Background region C no top-btag, bin""" +  str(i) + '"' + """,""" + str(datahisto.GetBinContent(i)) + """,0.01,100000);
    //RooRealVar QCD_CatD_ntb_bin""" +  str(i) + """("QCD_CatD_ntb_bin""" +  str(i) + '"' + ""","QCD Background region D no top-btag, bin""" +  str(i) + '"' + """,""" + str(datahisto.GetBinContent(i)) + """,0.01,100000);
        

    if((datahistoB_wtb->GetBinContent(""" + str(i) + """)-ttbarhistoB_wtb_nominal->GetBinContent(""" + str(i) + """))<0){
        temp=0.001;
    } else {
        temp=datahistoB_wtb->GetBinContent(""" + str(i) + """)-ttbarhistoB_wtb_nominal->GetBinContent(""" + str(i) + """);
    }
    RooRealVar QCD_CatB_wtb_bin""" +  str(i) + """("QCD_CatB_wtb_bin""" +  str(i) + '"' + ""","QCD Background region B with top-btag, bin""" +  str(i) + '"' + """,temp,0.0000001,10000000.0);
    std::cout<<"QCD_RegB_wtb_bin""" + str(i) + """ :\"<<temp<<std::endl;


    if((datahistoC_wtb->GetBinContent(""" + str(i) + """)-ttbarhistoC_wtb_nominal->GetBinContent(""" + str(i) + """))<0){
        temp=0.001;
    } else {
        temp=datahistoC_wtb->GetBinContent(""" + str(i) + """)-ttbarhistoC_wtb_nominal->GetBinContent(""" + str(i) + """);
    }
    RooRealVar QCD_CatC_wtb_bin""" +  str(i) + """("QCD_CatC_wtb_bin""" +  str(i) + '"' + ""","QCD Background region C with top-btag, bin""" +  str(i) + '"' + """,temp,0.0000001,10000000.0);
    std::cout<<"QCD_RegC_wtb_bin""" + str(i) + """ :\"<<temp<<std::endl;
    
    
    if((datahistoD_wtb->GetBinContent(""" + str(i) + """)-ttbarhistoD_wtb_nominal->GetBinContent(""" + str(i) + """))<0){
        temp=0.001;
    } else {
        temp=datahistoD_wtb->GetBinContent(""" + str(i) + """)-ttbarhistoD_wtb_nominal->GetBinContent(""" + str(i) + """);
    }
    RooRealVar QCD_CatD_wtb_bin""" +  str(i) + """("QCD_CatD_wtb_bin""" +  str(i) + '"' + ""","QCD Background region D with top-btag, bin""" +  str(i) + '"' + """,temp,0.0000001,10000000.0);
    std::cout<<"QCD_RegD_wtb_bin""" + str(i) + """ :\"<<temp<<std::endl;
   
   
   
   
   
    if((datahistoB_ntb->GetBinContent(""" + str(i) + """)-ttbarhistoB_ntb_nominal->GetBinContent(""" + str(i) + """))<0){
        temp=0.001;
    } else {
        temp=datahistoB_ntb->GetBinContent(""" + str(i) + """)-ttbarhistoB_ntb_nominal->GetBinContent(""" + str(i) + """);
    }
    RooRealVar QCD_CatB_ntb_bin""" +  str(i) + """("QCD_CatB_ntb_bin""" +  str(i) + '"' + ""","QCD Background region B no top-btag, bin""" +  str(i) + '"' + """,temp,0.0000001,10000000.0);
    std::cout<<"QCD_RegB_ntb_bin""" + str(i) + """ :\"<<temp<<std::endl;

    
    if((datahistoC_ntb->GetBinContent(""" + str(i) + """)-ttbarhistoC_ntb_nominal->GetBinContent(""" + str(i) + """))<0){
        temp=0.001;
    } else {
        temp=datahistoC_ntb->GetBinContent(""" + str(i) + """)-ttbarhistoC_ntb_nominal->GetBinContent(""" + str(i) + """);
    }
    RooRealVar QCD_CatC_ntb_bin""" +  str(i) + """("QCD_CatC_ntb_bin""" +  str(i) + '"' + ""","QCD Background region C no top-btag, bin""" +  str(i) + '"' + """,temp,0.0000001,10000000.0);
    std::cout<<"QCD_RegC_ntb_bin""" + str(i) + """ :\"<<temp<<std::endl;
    
    
    if((datahistoD_ntb->GetBinContent(""" + str(i) + """)-ttbarhistoD_ntb_nominal->GetBinContent(""" + str(i) + """))<0){
        temp=0.001;
    } else {
        temp=datahistoD_ntb->GetBinContent(""" + str(i) + """)-ttbarhistoD_ntb_nominal->GetBinContent(""" + str(i) + """);
    }
    RooRealVar QCD_CatD_ntb_bin""" +  str(i) + """("QCD_CatD_ntb_bin""" +  str(i) + '"' + ""","QCD Background region D no top-btag, bin""" +  str(i) + '"' + """,temp,0.0000001,10000000.0);
    std::cout<<"QCD_RegD_ntb_bin""" + str(i) + """ :\"<<temp<<std::endl;
    
    
    
    
    //RooRealVar QCD_CatB_wtb_bin""" +  str(i) + """("QCD_CatB_wtb_bin""" +  str(i) + '"' + ""","QCD Background region B with top-btag, bin""" +  str(i) + '"' + """,datahistoB_wtb->GetBinContent(""" + str(i) + """)+0.0001,0.0000001,10000000.0);
    //std::cout<<"QCD_RegB_wtb_bin""" + str(i) + """ :\"<<datahistoB_wtb->GetBinContent(""" + str(i) + """)<<std::endl;
    //RooRealVar QCD_CatC_wtb_bin""" +  str(i) + """("QCD_CatC_wtb_bin""" +  str(i) + '"' + ""","QCD Background region C with top-btag, bin""" +  str(i) + '"' + """,datahistoC_wtb->GetBinContent(""" + str(i) + """)+0.0001,0.0000001,10000000.0);
    //std::cout<<"QCD_RegC_wtb_bin""" + str(i) + """ :\"<<datahistoC_wtb->GetBinContent(""" + str(i) + """)<<std::endl;
    //RooRealVar QCD_CatD_wtb_bin""" +  str(i) + """("QCD_CatD_wtb_bin""" +  str(i) + '"' + ""","QCD Background region D with top-btag, bin""" +  str(i) + '"' + """,datahistoD_wtb->GetBinContent(""" + str(i) + """)+0.0001,0.0000001,10000000.0);
    //std::cout<<"QCD_RegD_wtb_bin""" + str(i) + """ :\"<<datahistoD_wtb->GetBinContent(""" + str(i) + """)<<std::endl;
    //RooRealVar QCD_CatB_ntb_bin""" +  str(i) + """("QCD_CatB_ntb_bin""" +  str(i) + '"' + ""","QCD Background region B no top-btag, bin""" +  str(i) + '"' + """,datahistoB_ntb->GetBinContent(""" + str(i) + """)+0.0001,0.0000001,10000000.0);
    //std::cout<<"QCD_RegB_ntb_bin""" + str(i) + """ :\"<<datahistoB_ntb->GetBinContent(""" + str(i) + """)<<std::endl;
    //RooRealVar QCD_CatC_ntb_bin""" +  str(i) + """("QCD_CatC_ntb_bin""" +  str(i) + '"' + ""","QCD Background region C no top-btag, bin""" +  str(i) + '"' + """,datahistoC_ntb->GetBinContent(""" + str(i) + """)+0.0001,0.0000001,10000000.0);
    //std::cout<<"QCD_RegC_ntb_bin""" + str(i) + """ :\"<<datahistoC_ntb->GetBinContent(""" + str(i) + """)<<std::endl;
    //RooRealVar QCD_CatD_ntb_bin""" +  str(i) + """("QCD_CatD_ntb_bin""" +  str(i) + '"' + ""","QCD Background region D no top-btag, bin""" +  str(i) + '"' + """,datahistoD_ntb->GetBinContent(""" + str(i) + """)+0.0001,0.0000001,10000000.0);
    //std::cout<<"QCD_RegD_ntb_bin""" + str(i) + """ :\"<<datahistoD_ntb->GetBinContent(""" + str(i) + """)<<std::endl;
    
""" 




    script+="""

    RooRealVar QCD_CatB_wtb_bin""" +  str(nbins) + """("QCD_CatB_wtb_bin""" +  str(nbins) + '"' + ""","QCD Background region B with top-btag, bin""" +  str(nbins) + '"' + """,datahistoB_wtb->GetBinContent(""" + str(nbins) + """)+0.00000011,0.0000001,10000000.0);
    std::cout<<"QCD_RegB_wtb_bin""" + str(nbins) + """ :\"<<datahistoB_wtb->GetBinContent(""" + str(nbins) + """)<<std::endl;
    RooRealVar QCD_CatC_wtb_bin""" +  str(nbins) + """("QCD_CatC_wtb_bin""" +  str(nbins) + '"' + ""","QCD Background region C with top-btag, bin""" +  str(nbins) + '"' + """,datahistoC_wtb->GetBinContent(""" + str(nbins) + """)+0.00000011,0.0000001,10000000.0);
    std::cout<<"QCD_RegC_wtb_bin""" + str(nbins) + """ :\"<<datahistoC_wtb->GetBinContent(""" + str(nbins) + """)<<std::endl;
    RooRealVar QCD_CatD_wtb_bin""" +  str(nbins) + """("QCD_CatD_wtb_bin""" +  str(nbins) + '"' + ""","QCD Background region D with top-btag, bin""" +  str(nbins) + '"' + """,datahistoD_wtb->GetBinContent(""" + str(nbins) + """)+0.00000011,0.0000001,10000000.0);
    std::cout<<"QCD_RegD_wtb_bin""" + str(nbins) + """ :\"<<datahistoD_wtb->GetBinContent(""" + str(nbins) + """)<<std::endl;
    RooRealVar QCD_CatB_ntb_bin""" +  str(nbins) + """("QCD_CatB_ntb_bin""" +  str(nbins) + '"' + ""","QCD Background region B no top-btag, bin""" +  str(nbins) + '"' + """,datahistoB_ntb->GetBinContent(""" + str(nbins) + """)+0.00000011,0.0000001,10000000.0);
    std::cout<<"QCD_RegB_ntb_bin""" + str(nbins) + """ :\"<<datahistoB_ntb->GetBinContent(""" + str(nbins) + """)<<std::endl;
    RooRealVar QCD_CatC_ntb_bin""" +  str(nbins) + """("QCD_CatC_ntb_bin""" +  str(nbins) + '"' + ""","QCD Background region C no top-btag, bin""" +  str(nbins) + '"' + """,datahistoC_ntb->GetBinContent(""" + str(nbins) + """)+0.00000011,0.0000001,10000000.0);
    std::cout<<"QCD_RegC_ntb_bin""" + str(nbins) + """ :\"<<datahistoC_ntb->GetBinContent(""" + str(nbins) + """)<<std::endl;
    RooRealVar QCD_CatD_ntb_bin""" +  str(nbins) + """("QCD_CatD_ntb_bin""" +  str(nbins) + '"' + ""","QCD Background region D no top-btag, bin""" +  str(nbins) + '"' + """,datahistoD_ntb->GetBinContent(""" + str(nbins) + """)+0.00000011,0.0000001,10000000.0);
    std::cout<<"QCD_RegD_ntb_bin""" + str(nbins) + """ :\"<<datahistoD_ntb->GetBinContent(""" + str(nbins) + """)<<std::endl;


    //RooRealVar QCD_CatB_wtb_bin""" +  str(nbins) + """("QCD_CatB_wtb_bin""" +  str(nbins) + '"' + ""","QCD Background region B with top-btag, bin""" +  str(nbins) + '"' + """,datahistoB_wtb->GetBinContent(""" + str(nbins) + """)-ttbarhistoB_wtb_nominal->GetBinContent(""" + str(nbins) + """),0.0000001,0.000001);
    //std::cout<<"QCD_RegB_wtb_bin""" + str(nbins) + """ :\"<<datahistoB_wtb->GetBinContent(""" + str(nbins) + """)-ttbarhistoB_wtb_nominal->GetBinContent(""" + str(nbins) + """)<<std::endl;
    //RooRealVar QCD_CatC_wtb_bin""" +  str(nbins) + """("QCD_CatC_wtb_bin""" +  str(nbins) + '"' + ""","QCD Background region C with top-btag, bin""" +  str(nbins) + '"' + """,datahistoC_wtb->GetBinContent(""" + str(nbins) + """)-ttbarhistoC_wtb_nominal->GetBinContent(""" + str(nbins) + """),0.0000001,0.000001);
    //std::cout<<"QCD_RegC_wtb_bin""" + str(nbins) + """ :\"<<datahistoC_wtb->GetBinContent(""" + str(nbins) + """)-ttbarhistoC_wtb_nominal->GetBinContent(""" + str(nbins) + """)<<std::endl;
    //RooRealVar QCD_CatD_wtb_bin""" +  str(nbins) + """("QCD_CatD_wtb_bin""" +  str(nbins) + '"' + ""","QCD Background region D with top-btag, bin""" +  str(nbins) + '"' + """,datahistoD_wtb->GetBinContent(""" + str(nbins) + """)-ttbarhistoD_wtb_nominal->GetBinContent(""" + str(nbins) + """),0.0000001,0.000001);
    //std::cout<<"QCD_RegD_wtb_bin""" + str(nbins) + """ :\"<<datahistoD_wtb->GetBinContent(""" + str(nbins) + """)-ttbarhistoD_wtb_nominal->GetBinContent(""" + str(nbins) + """)<<std::endl;
  
    //RooRealVar QCD_CatB_ntb_bin""" +  str(nbins) + """("QCD_CatB_ntb_bin""" +  str(nbins) + '"' + ""","QCD Background region B no top-btag, bin""" +  str(nbins) + '"' + """,datahistoB_ntb->GetBinContent(""" + str(nbins) + """)-ttbarhistoB_ntb_nominal->GetBinContent(""" + str(nbins) + """),0.0000001,0.000001);
    //std::cout<<"QCD_RegB_ntb_bin""" + str(nbins) + """ :\"<<datahistoB_ntb->GetBinContent(""" + str(nbins) + """)-ttbarhistoB_ntb_nominal->GetBinContent(""" + str(nbins) + """)<<std::endl;
    //RooRealVar QCD_CatC_ntb_bin""" +  str(nbins) + """("QCD_CatC_ntb_bin""" +  str(nbins) + '"' + ""","QCD Background region C no top-btag, bin""" +  str(nbins) + '"' + """,datahistoC_ntb->GetBinContent(""" + str(nbins) + """)-ttbarhistoC_ntb_nominal->GetBinContent(""" + str(nbins) + """),0.0000001,0.000001);
    //std::cout<<"QCD_RegC_ntb_bin""" + str(nbins) + """ :\"<<datahistoC_ntb->GetBinContent(""" + str(nbins) + """)-ttbarhistoC_ntb_nominal->GetBinContent(""" + str(nbins) + """)<<std::endl;
    //RooRealVar QCD_CatD_ntb_bin""" +  str(nbins) + """("QCD_CatD_ntb_bin""" +  str(nbins) + '"' + ""","QCD Background region D no top-btag, bin""" +  str(nbins) + '"' + """,datahistoD_ntb->GetBinContent(""" + str(nbins) + """)-ttbarhistoD_ntb_nominal->GetBinContent(""" + str(nbins) + """),0.0000001,0.000001);
    //std::cout<<"QCD_RegD_ntb_bin""" + str(nbins) + """ :\"<<datahistoD_ntb->GetBinContent(""" + str(nbins) + """)-ttbarhistoD_ntb_nominal->GetBinContent(""" + str(nbins) + """)<<std::endl;
    
    
    
    
    RooRealVar QCD_CatA_wtb_bin""" +  str(nbins) + """("QCD_CatB_wtb_bin""" +  str(nbins) + '"' + ""","QCD Background region B with top-btag, bin""" +  str(nbins) + '"' + """,0.00000011,0.0000001,0.000001);
    RooRealVar QCD_CatA_ntb_bin""" +  str(nbins) + """("QCD_CatB_ntb_bin""" +  str(nbins) + '"' + ""","QCD Background region B no top-btag, bin""" +  str(nbins) + '"' + """,0.00000011,0.0000001,0.000001);

    
"""

    for i in range(1,nbins):
        script+="""

    //RooFormulaVar QCD_CatA_wtb_bin"""+  str(i) + """("QCD_CatA_wtb_bin"""+  str(i) + '"' + ""","QCD Background yield in signal region with top b-tag, bin"""+  str(i) + '"' + ""","(@0*@1/@2) * (1.0 +""" + str(Zprime_withtopbtag_systrate) + """*@4 + @3*("""+ str(Zprime_withtopbtag_systshape_m) +""") * (""" + str(datahisto.GetBinCenter(i))+"""-"""+str(x0_wtb) + """) )",RooArgList(QCD_CatB_wtb_bin""" +  str(i) + """,QCD_CatC_wtb_bin""" +  str(i) + """,QCD_CatD_wtb_bin""" +  str(i) + """, QCD_ABCD_shape_wtb, QCD_ABCD_rate_wtb));
    //RooFormulaVar QCD_CatA_ntb_bin"""+  str(i) + """("QCD_CatA_ntb_bin"""+  str(i) + '"' + ""","QCD Background yield in signal region no top b-tag, bin"""+  str(i) + '"' + ""","(@0*@1/@2) * (1.0 +""" + str(Zprime_notopbtag_systrate) + """*@4 + @3*(""" + str(Zprime_notopbtag_systshape_m) + """) * (""" + str(datahisto.GetBinCenter(i))+"""-"""+str(x0_ntb) + """) )",RooArgList(QCD_CatB_ntb_bin""" +  str(i) + """,QCD_CatC_ntb_bin""" +  str(i) + """,QCD_CatD_ntb_bin""" +  str(i) + """, QCD_ABCD_shape_ntb, QCD_ABCD_rate_ntb));
    

    RooFormulaVar QCD_CatA_wtb_bin"""+  str(i) + """("QCD_CatA_wtb_bin"""+  str(i) + '"' + ""","QCD Background yield in signal region with top b-tag, bin"""+  str(i) + '"' + ""","(@0*@1/@2) * (1.0 +""" + str(Zprime_withtopbtag_systrate) + """*@4 + @3*("""+ str(Zprime_withtopbtag_systshape_m) +""") * (""" + str(datahisto.GetBinCenter(i))+"""-"""+str(x0_wtb) + """) ) * ((1.0 +""" + str(Zprime_withtopbtag_systrate) + """*@4 + @3*("""+ str(Zprime_withtopbtag_systshape_m) +""") * (""" + str(datahisto.GetBinCenter(i))+"""-"""+str(x0_wtb) + """) )>0)",RooArgList(QCD_CatB_wtb_bin""" +  str(i) + """,QCD_CatC_wtb_bin""" +  str(i) + """,QCD_CatD_wtb_bin""" +  str(i) + """, QCD_ABCD_shape_wtb, QCD_ABCD_rate_wtb));
    RooFormulaVar QCD_CatA_ntb_bin"""+  str(i) + """("QCD_CatA_ntb_bin"""+  str(i) + '"' + ""","QCD Background yield in signal region no top b-tag, bin"""+  str(i) + '"' + ""","(@0*@1/@2) * (1.0 +""" + str(Zprime_notopbtag_systrate) + """*@4 + @3*(""" + str(Zprime_notopbtag_systshape_m) + """) * (""" + str(datahisto.GetBinCenter(i))+"""-"""+str(x0_ntb) + """) ) * ((1.0 +""" + str(Zprime_notopbtag_systrate) + """*@4 + @3*(""" + str(Zprime_notopbtag_systshape_m) + """) * (""" + str(datahisto.GetBinCenter(i))+"""-"""+str(x0_ntb) + """) )>0)",RooArgList(QCD_CatB_ntb_bin""" +  str(i) + """,QCD_CatC_ntb_bin""" +  str(i) + """,QCD_CatD_ntb_bin""" +  str(i) + """, QCD_ABCD_shape_ntb, QCD_ABCD_rate_ntb));"""
    


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
    f=open("combine_datacards/cscripts_for_wspace/createABCDCombineWorkspaceFile_DATA_BKG.cxx","w")
    f.write(script)
    f.close()
    st = os.stat("combine_datacards/cscripts_for_wspace/createABCDCombineWorkspaceFile_DATA_BKG.cxx")
    os.chmod("combine_datacards/cscripts_for_wspace/createABCDCombineWorkspaceFile_DATA_BKG.cxx", st.st_mode | stat.S_IEXEC)
   


def createCcode_Sig(pathToOutputRootFile,nbins,SignalNick,systlist=[]):



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
#include "../../../../../interface/RooParametricHist.h"
//#include <../../../../../interface/RooParametricHist.h>
#include <RooAddition.h>
#include <TFile.h>
#include <iostream>

    
void createABCDCombineWorkspaceFile_""" + SignalNick + """(){





    // As usual, load the combine library to get access to the RooParametricHist
    gSystem->Load("libHiggsAnalysisCombinedLimit.so");
    // Output file and workspace 
    TFile *fOut = new TFile("/nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_""" + SignalNick + """.root","RECREATE");
    RooWorkspace wspace("wspace","wspace");

    // A search in a MET tail, define MET as our variable
    RooRealVar Zprime_M("Zprime_M","m(Zp)",0,10000);
    RooArgList vars(Zprime_M);
    TFile* file=TFile::Open(""" + '"' + pathToOutputRootFile + '"' + """);
"""


    #for SignalNick in SignalNickList:
        #for syst in systlist:
    for syst in systlist:          #if syst is "nominal":
            #systname=syst
            #if ('renfac' in syst) or ('PDF' in syst):
            if ('PDF' in syst):
                #systname=syst+'_BKG'
                systname1=syst
                if ('Up' in syst):
                    systname2=syst.replace("Up","_SigUp")
                if ('Down' in syst):
                    systname2=syst.replace("Down","_SigDown")
            else:
                systname1=syst
                systname2=syst
            #print systname2        
            
            script+="""
            
    TH1 * """ + SignalNick + """_histoA_wtb_""" + systname1 + """ = 0;
    TH1 * """ + SignalNick + """_histoB_wtb_""" + systname1 + """ = 0;
    TH1 * """ + SignalNick + """_histoC_wtb_""" + systname1 + """ = 0;
    TH1 * """ + SignalNick + """_histoD_wtb_""" + systname1 + """ = 0;
    TH1 * """ + SignalNick + """_histoA_ntb_""" + systname1 + """ = 0;
    TH1 * """ + SignalNick + """_histoB_ntb_""" + systname1 + """ = 0;
    TH1 * """ + SignalNick + """_histoC_ntb_""" + systname1 + """ = 0;
    TH1 * """ + SignalNick + """_histoD_ntb_""" + systname1 + """ = 0;
    
   
    file->GetObject(\"""" + SignalNick + """_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_""" + systname1 + """\", """ + SignalNick + """_histoA_wtb_""" + systname1 + """);
    file->GetObject(\"""" + SignalNick + """_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """_""" + systname1 + """\", """ + SignalNick + """_histoB_wtb_""" + systname1 + """);
    file->GetObject(\"""" + SignalNick + """_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + """_""" + systname1 + """\", """ + SignalNick + """_histoC_wtb_""" + systname1 + """);
    file->GetObject(\"""" + SignalNick + """_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + """_""" + systname1 + """\", """ + SignalNick + """_histoD_wtb_""" + systname1 + """);
    file->GetObject(\"""" + SignalNick + """_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_""" + systname1 + """\", """ + SignalNick + """_histoA_ntb_""" + systname1 + """);
    file->GetObject(\"""" + SignalNick + """_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """_""" + systname1 + """\", """ + SignalNick + """_histoB_ntb_""" + systname1 + """);
    file->GetObject(\"""" + SignalNick + """_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + """_""" + systname1 + """\", """ + SignalNick + """_histoC_ntb_""" + systname1 + """);
    file->GetObject(\"""" + SignalNick + """_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + """_""" + systname1 + """\", """ + SignalNick + """_histoD_ntb_""" + systname1 + """);                
            
  
            
    RooDataHist """ + SignalNick + """_histA_wtb_""" + systname2 + """(\"""" + SignalNick + """_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + "_" + systname2 + """\",\"""" + SignalNick + """_""" + systname1 + """\",vars,""" + SignalNick + """_histoA_wtb_""" + systname1 + """);
    RooDataHist """ + SignalNick + """_histB_wtb_""" + systname2 + """(\"""" + SignalNick + """_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + "_" + systname2 + """\",\"""" + SignalNick + """_""" + systname1 + """\",vars,""" + SignalNick + """_histoB_wtb_""" + systname1 + """);
    RooDataHist """ + SignalNick + """_histC_wtb_""" + systname2 + """(\"""" + SignalNick + """_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + "_" + systname2 + """\",\"""" + SignalNick + """_""" + systname1 + """\",vars,""" + SignalNick + """_histoC_wtb_""" + systname1 + """);
    RooDataHist """ + SignalNick + """_histD_wtb_""" + systname2 + """(\"""" + SignalNick + """_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + "_" + systname2 + """\",\"""" + SignalNick + """_""" + systname1 + """\",vars,""" + SignalNick + """_histoD_wtb_""" + systname1 + """);
    RooDataHist """ + SignalNick + """_histA_ntb_""" + systname2 + """(\"""" + SignalNick + """_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + "_" + systname2 + """\",\"""" + SignalNick + """_""" + systname1 + """\",vars,""" + SignalNick + """_histoA_ntb_""" + systname1 + """);
    RooDataHist """ + SignalNick + """_histB_ntb_""" + systname2 + """(\"""" + SignalNick + """_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + "_" + systname2 + """\",\"""" + SignalNick + """_""" + systname1 + """\",vars,""" + SignalNick + """_histoB_ntb_""" + systname1 + """);
    RooDataHist """ + SignalNick + """_histC_ntb_""" + systname2 + """(\"""" + SignalNick + """_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + "_" + systname2 + """\",\"""" + SignalNick + """_""" + systname1 + """\",vars,""" + SignalNick + """_histoC_ntb_""" + systname1 + """);
    RooDataHist """ + SignalNick + """_histD_ntb_""" + systname2 + """(\"""" + SignalNick + """_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + "_" + systname2 + """\",\"""" + SignalNick + """_""" + systname1 + """\",vars,""" + SignalNick + """_histoD_ntb_""" + systname1 + """);
    
    
    wspace.import(""" + SignalNick + """_histA_wtb_""" + systname2 + """);
    wspace.import(""" + SignalNick + """_histB_wtb_""" + systname2 + """);
    wspace.import(""" + SignalNick + """_histC_wtb_""" + systname2 + """);
    wspace.import(""" + SignalNick + """_histD_wtb_""" + systname2 + """);
    wspace.import(""" + SignalNick + """_histA_ntb_""" + systname2 + """);
    wspace.import(""" + SignalNick + """_histB_ntb_""" + systname2 + """);
    wspace.import(""" + SignalNick + """_histC_ntb_""" + systname2 + """);
    wspace.import(""" + SignalNick + """_histD_ntb_""" + systname2 + """);

    
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
    fOut->cd();
    wspace.Write();    
}    
"""
    f=open("combine_datacards/cscripts_for_wspace/createABCDCombineWorkspaceFile_" + SignalNick + ".cxx","w")
    f.write(script)
    f.close()
    st = os.stat("combine_datacards/cscripts_for_wspace/createABCDCombineWorkspaceFile_" + SignalNick + ".cxx")
    os.chmod("combine_datacards/cscripts_for_wspace/createABCDCombineWorkspaceFile_" + SignalNick + ".cxx", st.st_mode | stat.S_IEXEC)
   
def createScript(ABCDversion,SignalNick, WP):


  script="""
imax * #number of bins/channels
jmax * #number of backgrounds
kmax *
---------------
"""

  script+="""
shapes data_obs CatA_wtb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:DATA_2016_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatB_wtb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:DATA_2016_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatC_wtb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:DATA_2016_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatD_wtb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:DATA_2016_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatA_ntb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:DATA_2016_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatB_ntb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:DATA_2016_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatC_ntb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:DATA_2016_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatD_ntb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:DATA_2016_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + """_nominal
"""




  script+="""

shapes Sig      CatA_wtb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_""" + SignalNick +""".root wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes Sig      CatB_wtb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_""" + SignalNick +""".root wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes Sig      CatC_wtb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_""" + SignalNick +""".root wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes Sig      CatD_wtb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_""" + SignalNick +""".root wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes Sig      CatA_ntb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_""" + SignalNick +""".root wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes Sig      CatB_ntb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_""" + SignalNick +""".root wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes Sig      CatC_ntb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_""" + SignalNick +""".root wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes Sig      CatD_ntb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_""" + SignalNick +""".root wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC

shapes tt       CatA_wtb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatB_wtb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatC_wtb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatD_wtb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatA_ntb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:ttbar_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatB_ntb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:ttbar_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatC_ntb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:ttbar_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatD_ntb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:ttbar_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC



shapes QCD      CatA_wtb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:QCD_CatA_wtb
shapes QCD      CatB_wtb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:QCD_CatB_wtb
shapes QCD      CatC_wtb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:QCD_CatC_wtb
shapes QCD      CatD_wtb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:QCD_CatD_wtb
shapes QCD      CatA_ntb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:QCD_CatA_ntb
shapes QCD      CatB_ntb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:QCD_CatB_ntb
shapes QCD      CatC_ntb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:QCD_CatC_ntb
shapes QCD      CatD_ntb /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_DATA_BKG.root wspace:QCD_CatD_ntb

#------------------------------
bin             CatA_ntb   CatB_ntb   CatC_ntb   CatD_ntb     CatA_wtb CatB_wtb CatC_wtb CatD_wtb 
observation     -1         -1         -1         -1           -1       -1       -1       -1
#------------------------------
bin                                CatA_ntb   CatB_ntb   CatC_ntb   CatD_ntb   CatA_wtb CatB_wtb CatC_wtb CatD_wtb     CatA_ntb   CatB_ntb   CatC_ntb   CatD_ntb   CatA_wtb CatB_wtb CatC_wtb CatD_wtb   CatA_ntb   CatB_ntb   CatC_ntb   CatD_ntb   CatA_wtb CatB_wtb CatC_wtb CatD_wtb
process                            Sig    Sig    Sig    Sig    Sig    Sig    Sig    Sig        QCD    QCD    QCD    QCD    QCD    QCD    QCD    QCD      tt     tt     tt     tt     tt     tt     tt     tt           
process                            0      0      0      0      0      0      0      0          1      1      1      1      1      1      1      1        2      2      2      2      2      2      2      2
#rate                               -1     0     0     0     -1     0     0     0         1      1      1      1      1      1      1      1        -1     -1     -1     -1     -1     -1     -1     -1
rate                               -1     -1     -1     -1     -1     -1     -1     -1         1      1      1      1      1      1      1      1        -1     -1     -1     -1     -1     -1     -1     -1
#--------------------------------
MCSF_CSVLF                shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_CSVLF                shape   0.1    0.1    0.1    0.1    0.1    0.1    0.1    0.1         -      -      -      -      -      -      -      -       0.1    0.1    0.1    0.1    0.1    0.1    0.1    0.1      #MCSF uncertainty from ttbar and SC
MCSF_CSVHF                shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_CSVHF                shape   0.1    0.1    0.1    0.1    0.1    0.1    0.1    0.1         -      -      -      -      -      -      -      -       0.1    0.1    0.1    0.1    0.1    0.1    0.1    0.1      #MCSF uncertainty from ttbar and SC
MCSF_CSVHFStats1          shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVLFStats1          shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVHFStats2          shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVLFStats2          shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVCErr1             shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVCErr2             shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_toptag               shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_Wtag                 shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_PU                   shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_PDF_BKG              shape    -      -      -      -      -      -      -      -          -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_PDF_Sig              shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -        -      -      -      -      -      -      -      -       #MCSF uncertainty from ttbar and SC
MCSF_Lumi                 shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_Trigger              shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_powheg_renfac_env    shape    -      -      -      -      -      -      -      -          -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_amc_renfac_env       shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_JetMassScale         shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_JetMassRes           shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
nominal_JER               shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
nominal_JES               shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
ttbarXS                   shape    -      -      -      -      -      -      -      -          -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar 
ST_tWXS                   shape    -      -      -      -      -      -      -      -          -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar 
ST_tchanXS                shape    -      -      -      -      -      -      -      -          -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar 
ST_schanXS                shape    -      -      -      -      -      -      -      -          -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar 

"""




  for i in range(1,nbins+1):
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
    


  script=script+"""
# QCD ABCD systematic uncertainties
QCD_ABCD_shape_wtb      param 0.0 1.0
QCD_ABCD_shape_ntb      param 0.0 1.0
QCD_ABCD_rate_wtb       param 0.0 1.0
QCD_ABCD_rate_ntb       param 0.0 1.0

# free floating parameters, we do not need to declare them, but its a good idea to 
"""
  
  for i in range(1,nbins+1):
    script=script+"""
QCD_CatB_wtb_bin""" + str(i) + """ flatParam
QCD_CatC_wtb_bin""" + str(i) + """ flatParam
QCD_CatD_wtb_bin""" + str(i) + """ flatParam
QCD_CatB_ntb_bin""" + str(i) + """ flatParam
QCD_CatC_ntb_bin""" + str(i) + """ flatParam
QCD_CatD_ntb_bin""" + str(i) + """ flatParam
"""
  
  
  
  f=open('combine_datacards/'+SignalNick+'_'+ABCDversion+'_Combine_datacard.txt','w')
  f.write(script)
  f.close()
  #st = os.stat(datacardname)
  #os.chmod(datacardname, st.st_mode | stat.S_IEXEC)

#def createScript(scriptname,programpath,processname,filenames,outfilename,maxevents,skipevents):


def make_submissionscripts_for_workspaces(SignalNick,ABCDversion,WP):
    
  cmsswpath='/nfs/dust/cms/user/skudella/CMSSW_8_1_0'
  
  script="#!/bin/bash \n"
  if cmsswpath!='':
    script+="export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch \n"
    script+="source $VO_CMS_SW_DIR/cmsset_default.sh \n"
    script+="export SCRAM_ARCH="+os.environ['SCRAM_ARCH']+"\n"
    script+="cd "+cmsswpath+"/src\neval `scram runtime -sh`\n"
    script+="cd - \n"
    script+="""export PROCESSNAME="workspaces_"""+SignalNick+"_"+ABCDversion+ """"\n"""


  script+="""
cd /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST
cd combine_datacards/cscripts_for_wspace
root -q -b createABCDCombineWorkspaceFile_""" + SignalNick +""".cxx

cd /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST
mkdir combine_workspaces 
cd /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces
mkdir """ + SignalNick+"_"+ABCDversion+"""
cd ../combine_datacards
text2workspace.py """ +SignalNick+"_"+ABCDversion+ """_Combine_datacard.txt -o ../combine_workspaces/""" +SignalNick+"_"+ABCDversion+"""/""" +SignalNick+"_"+ABCDversion+ """.root

"""  

  scriptname='submit_scripts/scripts/'+SignalNick+'_'+ABCDversion+'.sh'
  f=open(scriptname,'w')
  f.write(script)
  f.close()
  st = os.stat(scriptname)
  os.chmod(scriptname, st.st_mode | stat.S_IEXEC)


def make_submissionscripts_for_workspaces_DATA_BKG(ABCDversion):
    
  cmsswpath='/nfs/dust/cms/user/skudella/CMSSW_8_1_0'
  
  script="#!/bin/bash \n"
  if cmsswpath!='':
    script+="export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch \n"
    script+="source $VO_CMS_SW_DIR/cmsset_default.sh \n"
    script+="export SCRAM_ARCH="+os.environ['SCRAM_ARCH']+"\n"
    script+="cd "+cmsswpath+"/src\neval `scram runtime -sh`\n"
    script+="cd - \n"
    script+="""export PROCESSNAME="workspaces_DATA_BKG"\n"""


  script+="""
cd /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST
cd combine_datacards/cscripts_for_wspace
root -q -b createABCDCombineWorkspaceFile_DATA_BKG.cxx
"""
#cd /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST
#mkdir combine_workspaces 
#cd /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces
#mkdir DATA_BKG"""+"_"+ABCDversion+"""
#cd ../combine_datacards
#text2workspace.py DATA_BKG"""+"_"+ABCDversion+ """_Combine_datacard.txt -o ../combine_workspaces/DATA_BKG"""+"_"+ABCDversion+"""/DATA_BKG"""+"_"+ABCDversion+ """.root

#"""  

  scriptname='submit_scripts/scripts/DATA_BKG_'+ABCDversion+'.sh'
  f=open(scriptname,'w')
  f.write(script)
  f.close()
  st = os.stat(scriptname)
  os.chmod(scriptname, st.st_mode | stat.S_IEXEC)


def make_submissionscripts_for_MaxLikelyhoodFits(SignalNick,expectedSignal,ABCDversion):
    
  cmsswpath='/nfs/dust/cms/user/skudella/CMSSW_8_1_0'
  
  script="#!/bin/bash \n"
  if cmsswpath!='':
    script+="export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch \n"
    script+="source $VO_CMS_SW_DIR/cmsset_default.sh \n"
    script+="export SCRAM_ARCH="+os.environ['SCRAM_ARCH']+"\n"
    script+="cd "+cmsswpath+"/src\neval `scram runtime -sh`\n"
    script+="cd - \n"
    script+="""export PROCESSNAME="MaxlikelihoodFit_"""+SignalNick+"_"+ABCDversion+""""\n"""


  script+="""
cd /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/"""+SignalNick+"_"+ABCDversion+"""
mkdir MaxLikelihood_wAsimov_wSig
cd MaxLikelihood_wAsimov_wSig
combine -M FitDiagnostics --setRobustFitStrategy 0  --setRobustFitTolerance """+str(expectedSignal*0.0001)+""" --rMin -"""+str(expectedSignal)+""" --rMax """+str(expectedSignal*4)+""" -t -1 --expectSignal """+str(expectedSignal)+""" --saveWithUncertainties --saveOverallShapes --saveShapes --plots  --freezeParameters QCD_CatA_ntb_bin16,QCD_CatB_ntb_bin16,QCD_CatC_ntb_bin16,QCD_CatD_ntb_bin16,QCD_CatA_wtb_bin16,QCD_CatB_wtb_bin16,QCD_CatC_wtb_bin16,QCD_CatD_wtb_bin16 --verbose 3 -n _MaxLikelihood_wAsimov_wSig ../"""+SignalNick+"_"+ABCDversion+""".root
mkdir prepostfit
cd prepostfit
eval `python /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/Prepostfit/PrePostFitPlots.py ../fitDiagnostics_MaxLikelihood_wAsimov_wSig.root ../../../../combine_datacards/"""+SignalNick+"_"+ABCDversion+"""_Combine_datacard.txt """+str(expectedSignal)+"""`
cd ../..
mkdir MaxLikelihood_wAsimov_nSig
cd MaxLikelihood_wAsimov_nSig
combine -M FitDiagnostics --setRobustFitStrategy 0  --setRobustFitTolerance """+str(expectedSignal*0.0001)+""" --rMin -"""+str(expectedSignal)+""" --rMax """+str(expectedSignal*4)+""" -t -1 --expectSignal 0 --saveWithUncertainties --saveOverallShapes --saveShapes --plots  --freezeParameters QCD_CatA_ntb_bin16,QCD_CatB_ntb_bin16,QCD_CatC_ntb_bin16,QCD_CatD_ntb_bin16,QCD_CatA_wtb_bin16,QCD_CatB_wtb_bin16,QCD_CatC_wtb_bin16,QCD_CatD_wtb_bin16 --verbose 3  -n _MaxLikelihood_wAsimov_nSig ../"""+SignalNick+"_"+ABCDversion+""".root
mkdir prepostfit
cd prepostfit
eval `python /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/Prepostfit/PrePostFitPlots.py ../fitDiagnostics_MaxLikelihood_wAsimov_nSig.root ../../../../combine_datacards/"""+SignalNick+"_"+ABCDversion+"""_Combine_datacard.txt """+str(expectedSignal)+"""`
cd ../..


mkdir MaxLikelihood_nAsimov_nSig
cd MaxLikelihood_nAsimov_nSig
combine -M FitDiagnostics --setRobustFitStrategy 0  --setRobustFitTolerance """+str(expectedSignal*0.0001)+""" --rMin -"""+str(expectedSignal)+""" --rMax """+str(expectedSignal*4)+""" --saveWithUncertainties --saveOverallShapes --saveShapes --plots --freezeParameters QCD_CatA_ntb_bin16,QCD_CatB_ntb_bin16,QCD_CatC_ntb_bin16,QCD_CatD_ntb_bin16,QCD_CatA_wtb_bin16,QCD_CatB_wtb_bin16,QCD_CatC_wtb_bin16,QCD_CatD_wtb_bin16 --verbose 3  -n _MaxLikelihood_nAsimov_nSig ../"""+SignalNick+"_"+ABCDversion+""".root
mkdir prepostfit
cd prepostfit
eval `python /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/Prepostfit/PrePostFitPlots.py ../fitDiagnostics_MaxLikelihood_nAsimov_nSig.root ../../../../combine_datacards/"""+SignalNick+"_"+ABCDversion+"""_Combine_datacard.txt """+str(expectedSignal)+"""`
cd ../..

mkdir MaxLikelihood_nAsimov_wSig
cd MaxLikelihood_nAsimov_wSig
combine -M FitDiagnostics --setRobustFitStrategy 0  --setRobustFitTolerance """+str(expectedSignal*0.0001)+""" --rMin -1 --rMax 4 --saveWithUncertainties --saveOverallShapes --saveShapes --plots --freezeParameters QCD_CatA_ntb_bin16,QCD_CatB_ntb_bin16,QCD_CatC_ntb_bin16,QCD_CatD_ntb_bin16,QCD_CatA_wtb_bin16,QCD_CatB_wtb_bin16,QCD_CatC_wtb_bin16,QCD_CatD_wtb_bin16 --verbose 3  -n _MaxLikelihood_nAsimov_wSig ../"""+SignalNick+"_"+ABCDversion+ """.root
mkdir prepostfit
cd prepostfit
eval `python /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/Prepostfit/PrePostFitPlots.py ../fitDiagnostics_MaxLikelihood_nAsimov_wSig.root ../../../../combine_datacards/"""+SignalNick+"_"+ABCDversion+ """_Combine_datacard.txt """+str(expectedSignal)+"""`
cd ../..

"""

  #script+="""
#mkdir MaxLikelihood_Toy_wSig
#cd MaxLikelihood_Toy_wSig
#combine -M FitDiagnostics ----setRobustFitStrategy 0 --setRobustFitTolerance 0.0001 --rMin -"""+str(expectedSignal)+""" --rMax """+str(expectedSignal*4)+""" -t 1000 --expectSignal """+str(expectedSignal)+""" -- --saveShapes --plots --saveFitResult -n _MaxLikelihood_Toy_wSig ../"""+SignalNick+"_"+ABCDversion+"_"+WP+"""_noSignal.root`
#cd ..
#mkdir MaxLikelihood_Toy_nSig
#cd MaxLikelihood_Toy_nSig
#combine -M FitDiagnostics ----setRobustFitStrategy 0 --setRobustFitTolerance 0.0001 --rMin -"""+str(expectedSignal)+""" --rMax """+str(expectedSignal*4)+""" -t 1000 --expectSignal 0 -- --saveShapes --plots --saveFitResult -n _MaxLikelihood_Toy_nSig ../"""+SignalNick+"_"+ABCDversion+"_"+WP+"""_noSignal.root`
#cd ..
#"""  

  scriptname='submit_scripts/maxlikelihoodfit_scripts/MaxlikelihoodFit_'+SignalNick+'_'+ABCDversion+'_'+WP+'.sh'
  f=open(scriptname,'w')
  f.write(script)
  f.close()
  st = os.stat(scriptname)
  os.chmod(scriptname, st.st_mode | stat.S_IEXEC)

def make_submissionscripts_for_AsymptoticFits(SignalNick,expectedSignal,ABCDversion):
    
  cmsswpath='/nfs/dust/cms/user/skudella/CMSSW_8_1_0'
  
  script="#!/bin/bash \n"
  if cmsswpath!='':
    script+="export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch \n"
    script+="source $VO_CMS_SW_DIR/cmsset_default.sh \n"
    script+="export SCRAM_ARCH="+os.environ['SCRAM_ARCH']+"\n"
    script+="cd "+cmsswpath+"/src\neval `scram runtime -sh`\n"
    script+="cd - \n"
    script+="""export PROCESSNAME="AsymptoticFit_"""+SignalNick+"_"+ABCDversion+""""\n"""


  script+="""
cd /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/"""+SignalNick+"_"+ABCDversion+"""
mkdir Asymptotic
cd Asymptotic
eval `combine -M AsymptoticLimits --minosAlgo stepping   --rAbsAcc """ + str(expectedSignal*0.0001) + """  --rMin -""" + str(expectedSignal) + """ --rMax """ + str(expectedSignal*4) + """ -n _Asymptotic ../"""+SignalNick+"_"+ABCDversion+""".root`

cp /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/impact_tab.py .

mkdir no_ABCD
cd no_ABCD
eval `combine -M AsymptoticLimits --minosAlgo stepping   --rAbsAcc """ + str(expectedSignal*0.0001) + """  --rMin -""" + str(expectedSignal) + """ --rMax """ + str(expectedSignal*4) + """ -n _Asymptotic --freezeParameters QCD_ABCD_shape_wtb,QCD_ABCD_shape_ntb,QCD_ABCD_rate_wtb,QCD_ABCD_rate_ntb ../../"""+SignalNick+"_"+ABCDversion+""".root`
cd ..

mkdir no_btag
cd no_btag
eval `combine -M AsymptoticLimits --minosAlgo stepping   --rAbsAcc """ + str(expectedSignal*0.0001) + """  --rMin -""" + str(expectedSignal) + """ --rMax """ + str(expectedSignal*4) + """ -n _Asymptotic --freezeParameters MCSF_CSVLF,MCSF_CSVHF,MCSF_CSVHFStats1,MCSF_CSVLFStats1,MCSF_CSVHFStats2,MCSF_CSVLFStats2,MCSF_CSVCErr1,MCSF_CSVCErr2 ../../"""+SignalNick+"_"+ABCDversion+""".root`
cd ..

mkdir no_ttag
cd no_ttag
eval `combine -M AsymptoticLimits --minosAlgo stepping   --rAbsAcc """ + str(expectedSignal*0.0001) + """  --rMin -""" + str(expectedSignal) + """ --rMax """ + str(expectedSignal*4) + """ -n _Asymptotic --freezeParameters MCSF_toptag ../../"""+SignalNick+"_"+ABCDversion+""".root`
cd ..

mkdir no_Wtag
cd no_Wtag
eval `combine -M AsymptoticLimits --minosAlgo stepping   --rAbsAcc """ + str(expectedSignal*0.0001) + """  --rMin -""" + str(expectedSignal) + """ --rMax """ + str(expectedSignal*4) + """ -n _Asymptotic --freezeParameters MCSF_Wtag, ../../"""+SignalNick+"_"+ABCDversion+""".root`
cd ..

mkdir no_theory
cd no_theory
eval `combine -M AsymptoticLimits --minosAlgo stepping   --rAbsAcc """ + str(expectedSignal*0.0001) + """  --rMin -""" + str(expectedSignal) + """ --rMax """ + str(expectedSignal*4) + """ -n _Asymptotic --freezeParameters MCSF_PDF_Sig,MCSF_PDF_BKG,MCSF_renfac_env_Sig,MCSF_renfac_env_BKG,ttbarXS ../../"""+SignalNick+"_"+ABCDversion+""".root`
cd ..

mkdir no_JEC
cd no_JEC
eval `combine -M AsymptoticLimits --minosAlgo stepping   --rAbsAcc """ + str(expectedSignal*0.0001) + """  --rMin -""" + str(expectedSignal) + """ --rMax """ + str(expectedSignal*4) + """ -n _Asymptotic --freezeParameters nominal_JER,nominal_JES ../../"""+SignalNick+"_"+ABCDversion+""".root`
cd ..

mkdir no_exp
cd no_exp
eval `combine -M AsymptoticLimits --minosAlgo stepping   --rAbsAcc """ + str(expectedSignal*0.0001) + """  --rMin -""" + str(expectedSignal) + """ --rMax """ + str(expectedSignal*4) + """ -n _Asymptotic --freezeParameters MCSF_PU,MCSF_Lumi,MCSF_Trigger ../../"""+SignalNick+"_"+ABCDversion+""".root`
cd ..

mkdir no_MCstat
cd no_MCstat
eval `combine -M AsymptoticLimits --minosAlgo stepping   --rAbsAcc """ + str(expectedSignal*0.0001) + """  --rMin -""" + str(expectedSignal) + """ --rMax """ + str(expectedSignal*4) + """ -n _Asymptotic --freezeParameters *tb_stat_bin* ../../"""+SignalNick+"_"+ABCDversion+""".root`
cd ..

mkdir no_syst
cd no_syst
eval `combine -M AsymptoticLimits --minosAlgo stepping   --rAbsAcc """ + str(expectedSignal*0.0001) + """  --rMin -""" + str(expectedSignal) + """ --rMax """ + str(expectedSignal*4) + """ -n _Asymptotic --freezeParameters MCSF_PU,MCSF_Lumi,MCSF_Trigger,QCD_ABCD_shape_wtb,QCD_ABCD_shape_ntb,QCD_ABCD_rate_wtb,QCD_ABCD_rate_ntb,MCSF_CSVLF,MCSF_CSVHF,MCSF_CSVHFStats1,MCSF_CSVLFStats1,MCSF_CSVHFStats2,MCSF_CSVLFStats2,MCSF_CSVCErr1,MCSF_CSVCErr2,MCSF_toptag,nominal_JER,nominal_JES,MCSF_PDF_BKG,MCSF_PDF_Sig,MCSF_renfac_env_Sig,MCSF_renfac_env_BKG,ttbarXS,MCSF_Wtag ../../"""+SignalNick+"_"+ABCDversion+""".root`
cd ..



python impact_tab.py

cp Influence_of_Systsgroups_on_Limit.txt Influence_of_Systsgroups_on_Limit"""+WPsname+""".txt 

"""  

  scriptname='submit_scripts/asymptoticfit_scripts/AsymptoticFit_'+SignalNick+'_'+ABCDversion+'.sh'
  f=open(scriptname,'w')
  f.write(script)
  f.close()
  st = os.stat(scriptname)
  os.chmod(scriptname, st.st_mode | stat.S_IEXEC)



def make_submissionscripts_for_resultplots(SignalNick,expectedSignal,ABCDversion):
    
  cmsswpath='/nfs/dust/cms/user/skudella/CMSSW_8_1_0'
  
  script="#!/bin/bash \n"
  if cmsswpath!='':
    script+="export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch \n"
    script+="source $VO_CMS_SW_DIR/cmsset_default.sh \n"
    script+="export SCRAM_ARCH="+os.environ['SCRAM_ARCH']+"\n"
    script+="cd "+cmsswpath+"/src\neval `scram runtime -sh`\n"
    script+="cd - \n"
    script+="""export PROCESSNAME="FitAnalysis_"""+SignalNick+"_"+ABCDversion+""""\n"""


  script+="""
cd /nfs/dust/cms/user/skudella/CombineFitTests/PseudosaveWithUncertaintiesDataTests/scripts/
./runPlotResults.sh /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/"""+SignalNick+"_"+ABCDversion+"""/MaxLikelihood_nAsimov_nSig/fitDiagnostics_MaxLikelihood_nAsimov_nSig.root "" "1" 
cd /nfs/dust/cms/user/skudella/CombineFitTests/PseudoDataTests/scripts/
./runPlotResults.sh /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/"""+SignalNick+"_"+ABCDversion+"""/MaxLikelihood_nAsimov_wSig/fitDiagnostics_MaxLikelihood_nAsimov_wSig.root "" "1" 

./runPlotResults.sh /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/"""+SignalNick+"_"+ABCDversion+"""/MaxLikelihood_wAsimov_nSig/fitDiagnostics_MaxLikelihood_wAsimov_nSig.root "" "1" 
./runPlotResults.sh /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/"""+SignalNick+"_"+ABCDversion+"""/MaxLikelihood_wAsimov_wSig/fitDiagnostics_MaxLikelihood_wAsimov_wSig.root "" "1"  

cd /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/"""+SignalNick+"_"+ABCDversion+"""
cd MaxLikelihood_nAsimov_nSig; 
python /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/scripts/diffNuisances.py -g nAsimov_nSig_minosall_"""+SignalNick+"_"+ABCDversion+""" fitDiagnostics_MaxLikelihood_nAsimov_nSig.root
cd .. 
cd MaxLikelihood_nAsimov_wSig; 
python /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/scripts/diffNuisances.py -g nAsimov_wSig_minosall_"""+SignalNick+"_"+ABCDversion+""" fitDiagnostics_MaxLikelihood_nAsimov_wSig.root
cd .. 



cd MaxLikelihood_wAsimov_nSig
python /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/scripts/diffNuisances.py -g wAsimov_nSig_minosall_"""+SignalNick+"_"+ABCDversion+""" fitDiagnostics_MaxLikelihood_wAsimov_nSig.root
cd ..
cd MaxLikelihood_wAsimov_wSig
python /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/scripts/diffNuisances.py -g wAsimov_wSig_minosall_"""+SignalNick+"_"+ABCDversion+""" fitDiagnostics_MaxLikelihood_wAsimov_wSig.root
cd ..



"""  



  script+="""
cd /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/"""+SignalNick+"_"+ABCDversion+"""/MaxLikelihood_nAsimov_nSig
python /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/scripts/removeBBBfromCovMat.py fitDiagnostics_MaxLikelihood_nAsimov_nSig.root
python /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/scripts/diffNuisances.py -g nAsimov_nSig_minosall_"""+SignalNick+"_"+ABCDversion+""" fitDiagnostics_MaxLikelihood_nAsimov_nSig.root

cd /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/"""+SignalNick+"_"+ABCDversion+"""/MaxLikelihood_nAsimov_wSig
python /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/scripts/removeBBBfromCovMat.py fitDiagnostics_MaxLikelihood_nAsimov_wSig.root
python /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/scripts/diffNuisances.py -g nAsimov_nSig_minosall_"""+SignalNick+"_"+ABCDversion+""" fitDiagnostics_MaxLikelihood_nAsimov_nSig.root

cd /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/"""+SignalNick+"_"+ABCDversion+"""/MaxLikelihood_wAsimov_nSig
python /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/scripts/removeBBBfromCovMat.py fitDiagnostics_MaxLikelihood_wAsimov_nSig.root
python /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/scripts/diffNuisances.py -g wAsimov_nSig_minosall_"""+SignalNick+"_"+ABCDversion+""" fitDiagnostics_MaxLikelihood_wAsimov_nSig.root

cd /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/"""+SignalNick+"_"+ABCDversion+"""/MaxLikelihood_wAsimov_wSig
python /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/scripts/removeBBBfromCovMat.py fitDiagnostics_MaxLikelihood_wAsimov_wSig.root
python /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/scripts/diffNuisances.py -g wAsimov_wSig_minosall_"""+SignalNick+"_"+ABCDversion+""" fitDiagnostics_MaxLikelihood_wAsimov_wSig.root



cd /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/"""+SignalNick+"_"+ABCDversion+"""
cd MaxLikelihood_nAsimov_nSig 
python /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/scripts/diffNuisances.py -g nAsimov_nSig_minosall_"""+SignalNick+"_"+ABCDversion+""" fitDiagnostics_MaxLikelihood_nAsimov_nSig.root
cd .. 
cd MaxLikelihood_nAsimov_wSig 
python /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/scripts/diffNuisances.py -g nAsimov_wSig_minosall_"""+SignalNick+"_"+ABCDversion+""" fitDiagnostics_MaxLikelihood_nAsimov_wSig.root
cd .. 



cd MaxLikelihood_wAsimov_nSig
python /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/scripts/diffNuisances.py -g wAsimov_nSig_minosall_"""+SignalNick+"_"+ABCDversion+""" fitDiagnostics_MaxLikelihood_wAsimov_nSig.root
cd ..
cd MaxLikelihood_wAsimov_wSig
python /nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/scripts/diffNuisances.py -g wAsimov_wSig_minosall_"""+SignalNick+"_"+ABCDversion+""" fitDiagnostics_MaxLikelihood_wAsimov_wSig.root
cd ..


"""  


  scriptname='submit_scripts/finanalysis_scripts/FitAnalysis_'+SignalNick+'_'+ABCDversion+'_'+WP+'.sh'
  f=open(scriptname,'w')
  f.write(script)
  f.close()
  st = os.stat(scriptname)
  os.chmod(scriptname, st.st_mode | stat.S_IEXEC)





def make_submissionscripts_for_impact_on_limits_plots(SignalNick,expectedSignal,ABCDversion,WP):
    
  cmsswpath='/nfs/dust/cms/user/skudella/CMSSW_8_1_0'
  
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

cmsswpath="/nfs/dust/cms/user/skudella/CMSSW_8_1_0"

indir = "/nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/"
outdir= "/nfs/dust/cms/user/skudella/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/"





   
systlist=["nominal","MCSF_CSVLFUp","MCSF_CSVHFUp","MCSF_CSVHFStats1Up","MCSF_CSVLFStats1Up","MCSF_CSVHFStats2Up","MCSF_CSVLFStats2Up","MCSF_CSVCErr1Up","MCSF_CSVCErr2Up","MCSF_toptagUp","MCSF_WtagUp","MCSF_PUUp","MCSF_PDFUp","MCSF_LumiUp","MCSF_TriggerUp","MCSF_powheg_renfac_envUp","MCSF_amc_renfac_envUp","nominal_JERUp","nominal_JESUp","ttbarXSUp","ST_tWXSUp","ST_tchanXSUp","ST_schanXSUp","MCSF_JetMassScaleUp","MCSF_JetMassResUp","MCSF_CSVLFDown","MCSF_CSVHFDown","MCSF_CSVHFStats1Down","MCSF_CSVLFStats1Down","MCSF_CSVHFStats2Down","MCSF_CSVLFStats2Down","MCSF_CSVCErr1Down","MCSF_CSVCErr2Down","MCSF_toptagDown","MCSF_WtagDown","MCSF_PUDown","MCSF_PDFDown","MCSF_LumiDown","MCSF_TriggerDown","MCSF_powheg_renfac_envDown","MCSF_amc_renfac_envDown","nominal_JERDown","nominal_JESDown","ttbarXSDown","ST_tWXSDown","ST_tchanXSDown","ST_schanXSDown","MCSF_JetMassScaleDown","MCSF_JetMassResDown"]
    
    

print 'Creating datacards'

cmsswpath='/nfs/dust/cms/user/skudella/CMSSW_8_1_0'

#SignalNickList=["SigRho15001200_tWb"]
#expectedSignals=[8.6]
#SignalNickList=["SigRho25001200_tWb"]
#expectedSignals=[0.33]


SignalNickList=["SigRho15001200_tWb","SigRho20001200_tWb","SigRho25001200_tWb","SigRho1500700_tWb","SigRho1500900_tWb","SigRho2000900_tWb","SigRho20001500_tWb","SigRho25001500_tWb"]+["SigRho15001200_ttZ","SigRho20001200_ttZ","SigRho25001200_ttZ","SigRho1500700_ttZ","SigRho1500900_ttZ","SigRho2000900_ttZ","SigRho20001500_ttZ","SigRho25001500_ttZ"]+["SigRho15001200_ttH","SigRho20001200_ttH","SigRho25001200_ttH","SigRho1500700_ttH","SigRho1500900_ttH","SigRho2000900_ttH","SigRho20001500_ttH","SigRho25001500_ttH"]
SignalNickList=SignalNickList+["SigRho15001200_BR00_50_50","SigRho20001200_BR00_50_50","SigRho25001200_BR00_50_50","SigRho1500700_BR00_50_50","SigRho1500900_BR00_50_50","SigRho2000900_BR00_50_50","SigRho20001500_BR00_50_50","SigRho25001500_BR00_50_50"]
#SignalNickList=SignalNickList+["SigRho15001200_BR05_025_025","SigRho20001200_BR05_025_025","SigRho25001200_BR05_025_025","SigRho1500700_BR05_025_025","SigRho1500900_BR05_025_025","SigRho2000900_BR05_025_025","SigRho20001500_BR05_025_025","SigRho25001500_BR05_025_025"]

expectedSignals=[8.6,0.27,0.33,0.8,1.5,0.21,0.9,0.29]+[3.1,0.29,0.18,3.1,2.4,0.4,0.33,0.13]+[11,0.54,0.26,3.5,2.6,0.56,0.59,0.22]+[8.6,0.27,0.33,0.8,1.5,0.21,0.9,0.29]



#Truesignallist=[]
#for i in SignalNickList:
    #print i[3:]
    #if "BR05_025_025" in i:
        #Truesignallist.append(i[3:]+"_1pb")
    #else:
        #Truesignallist.append(i[3:]+"_1_0pb")

Signals=["SigGstar1500800","SigGstar15001000","SigGstar15001300","SigGstar17501300","SigGstar20001000","SigGstar20001300","SigGstar20001500","SigGstar22501300","SigGstar22501500","SigGstar25001300","SigGstar25001500","SigGstar25001800","SigGstar27501500","SigGstar30001500","SigGstar30001800","SigGstar30002100","SigGstar35001800","SigGstar35002100","SigGstar35002500","SigGstar40002100","SigGstar40002500","SigGstar40003000"]

SignalNickList2=[]
expectedSignals2=[]
for i in Signals:
    for channel in ["tWb","ttZ","ttH","BR05_025_025"]:
        for width in ["Nar","Wid"]:
            SignalNickList2.append(i+"_"+channel+width)
            #expectedSignals2.append(1.0)
            if "star15" in i:
                expectedSignals2.append(1.0)
            else:
                expectedSignals2.append(0.1)
SignalNickList=SignalNickList+   SignalNickList2
expectedSignals=expectedSignals+expectedSignals2
            


ABCDversion='ABCD5'
    
    
#for WP in ['CMS_WP','Anna_WP','CMS_WP_nodynEvtHT','Anna_WP_nodynEvtHT']:
#for WP in ['CMS_WP','Anna_WP','CMS_WP_nodynEvtHT']:
for WP in ['CMS_WP']:
    
    bottomWP='medium'
    #bottomWP='loose'
    #topWP='medium'
    topWP='loose'
              
    WPsname='_'+topWP+'_ttagging_'+bottomWP+'_btagging'
    #pathToOutputRootFile_DATA_BKG=indir + "rootfiles/DATA_BKG.root"
    pathToOutputRootFile_DATA_BKG=indir + "rootfiles/all_final.root"
    
    
    if "Rho" in SignalNickList[0]:
        #pathToOutputRootFile_Sig=indir + "rootfiles/Rho.root"
        pathToOutputRootFile_Sig=indir + "rootfiles/all_final.root"
    
    if "Gstar" in SignalNickList[0]:
        #pathToOutputRootFile_Sig=indir + "rootfiles/Gstar.root"
        pathToOutputRootFile_Sig=indir + "rootfiles/all_final.root"
    
    if WP=='CMS_WP':        

              
              if bottomWP=='medium':
                  if topWP=='loose':
                    Zprime_withtopbtag_systrate=0.100533388233
                    Zprime_withtopbtag_systshape_m=0.0001950250116
                    Zprime_withtopbtag_systshape_c=1.12496
                    Zprime_notopbtag_systrate=0.0485657524616 
                    Zprime_notopbtag_systshape_m=7.03893690402e-05
                    Zprime_notopbtag_systshape_c=1.09896 
                                          
                    #Zprime_withtopbtag_systrate=0.0749051446309
                    #Zprime_withtopbtag_systshape_m=0.000213573364769
                    #Zprime_withtopbtag_systshape_c=1.12496
                    #Zprime_notopbtag_systrate=0.0425434656187 
                    #Zprime_notopbtag_systshape_m=7.04048390432e-05
                    #Zprime_notopbtag_systshape_c=1.09896 
                    #Zprime_withtopbtag_systrate=0.0736834218346
                    #Zprime_withtopbtag_systshape_m=0.000157325109262
                    #Zprime_withtopbtag_systshape_c=1.12496
                    #Zprime_notopbtag_systrate=0.0428972485948 
                    #Zprime_notopbtag_systshape_m=6.92106626942e-05
                    #Zprime_notopbtag_systshape_c=1.09896                         
                    #pathToOutputRootFile=indir + "rootfiles/output_rebinned_added_CMS_WP_loose_ttagging_medium_btagging.root"

                  if topWP=='medium':
                    Zprime_withtopbtag_systrate=0.0556968382142
                    Zprime_withtopbtag_systshape_m=4.83210624517e-05
                    Zprime_withtopbtag_systshape_c=1.12496
                    Zprime_notopbtag_systrate=0.107405141995 
                    Zprime_notopbtag_systshape_m=0.000162216814803
                    Zprime_notopbtag_systshape_c=1.09896   
                    #pathToOutputRootFile=indir + "rootfiles/output_rebinned_added_CMS_WP_medium_ttagging_medium_btagging.root"
              else:
                  if topWP=='loose':
                    Zprime_withtopbtag_systrate=0.0662402661262
                    Zprime_withtopbtag_systshape_m=4.92325674899e-05
                    Zprime_withtopbtag_systshape_c=1.12496
                    Zprime_notopbtag_systrate=0.0677149795161
                    Zprime_notopbtag_systshape_m=3.54398759094e-05
                    Zprime_notopbtag_systshape_c=1.09896  
                    #pathToOutputRootFile=indir + "rootfiles/output_rebinned_added_CMS_WP_loose_ttagging_loose_btagging.root"
                  if topWP=='medium':
                    Zprime_withtopbtag_systrate=0.0711833960603
                    Zprime_withtopbtag_systshape_m=2.10852089666e-06
                    Zprime_withtopbtag_systshape_c=1.12496
                    Zprime_notopbtag_systrate=0.0756599436301 
                    Zprime_notopbtag_systshape_m=1.89854920597e-05
                    Zprime_notopbtag_systshape_c=1.09896               
                    #pathToOutputRootFile=indir + "rootfiles/output_rebinned_added_CMS_WP_medium_ttagging_loose_btagging.root"
                #Zprime_withtopbtag_systrate=0.0736834218346
                #Zprime_withtopbtag_systshape_m=0.000157325109262
                #Zprime_withtopbtag_systshape_c=1.12496
                #Zprime_notopbtag_systrate=0.0428972485948 
                #Zprime_notopbtag_systshape_m=6.92106626942e-05
                #Zprime_notopbtag_systshape_c=1.09896     
                
                ##Zprime_withtopbtag_systrate=0.0662402661262
                ##Zprime_withtopbtag_systshape_m=4.92325674899e-05
                ##Zprime_withtopbtag_systshape_c=1.12496
                ##Zprime_notopbtag_systrate=0.0677149795161
                ##Zprime_notopbtag_systshape_m=3.54398759094e-05
                ##Zprime_notopbtag_systshape_c=1.09896       
                
    elif WP=='CMS_WP_medium_ttag':               
                Zprime_withtopbtag_systrate=0.0556968382142
                Zprime_withtopbtag_systshape_m=4.83210624517e-05
                Zprime_withtopbtag_systshape_c=1.12496
                Zprime_notopbtag_systrate=0.107405141995 
                Zprime_notopbtag_systshape_m=0.000162216814803
                Zprime_notopbtag_systshape_c=1.09896      
                WP='CMS_WP'
                
    else:
        print "heyo sucker"    
    print "pathToOutputRootFile_DATA_BKG  ", pathToOutputRootFile_DATA_BKG
    #pathToOutputRootFile=indir + "/rootfiles/output_rebinned_added_"+ WP + ".root"
    f=ROOT.TFile(pathToOutputRootFile_DATA_BKG, "readonly")
    #print "looking at file ", 
    keyList = f.GetKeyNames()    
    for key in keyList:
        if ("DATA_2016" in key) and ("ABCD" in key) and ("nominal" in key) and ("Tprime" not in key) and ("inclusive" not in key) and ("Zprime_M" in key) and ("CatA" in key):
            datahisto=f.Get(key)
            print key, " selected to extract binning"
            break
    
    datahisto
    nbins=datahisto.GetNbinsX()

    rebin=1
    print "number of mass bins=", nbins    
    nbins=nbins/rebin
    print "rebinning to ", nbins


    createCcode_DATA_BKG(pathToOutputRootFile_DATA_BKG,nbins,systlist)
    make_submissionscripts_for_workspaces_DATA_BKG(ABCDversion)
    
    for SignalNick,expectedSignal in zip(SignalNickList,expectedSignals):    
        make_submissionscripts_for_MaxLikelyhoodFits(SignalNick,expectedSignal,ABCDversion)
        make_submissionscripts_for_AsymptoticFits(SignalNick,expectedSignal,ABCDversion)
        make_submissionscripts_for_resultplots(SignalNick,expectedSignal,ABCDversion)
        
    
    
        if "Rho" in SignalNick:
            #pathToOutputRootFile_Sig=indir + "rootfiles/Rho.root"
            pathToOutputRootFile_Sig=indir + "rootfiles/all_final.root"
    
        if "Gstar" in SignalNick:
            #pathToOutputRootFile_Sig=indir + "rootfiles/Gstar.root"        
            pathToOutputRootFile_Sig=indir + "rootfiles/all_final.root"        
        
        createScript(ABCDversion,SignalNick,WP)
        #createCcode(pathToOutputRootFile,nbins,rebin,SignalNick,WP,systlist)
        #print SignalNick
        #print pathToOutputRootFile_Sig
        createCcode_Sig(pathToOutputRootFile_Sig,nbins,SignalNick,systlist)
        make_submissionscripts_for_workspaces(SignalNick,ABCDversion,WP)        
