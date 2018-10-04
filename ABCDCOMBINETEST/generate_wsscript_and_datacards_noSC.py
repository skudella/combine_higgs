import sys
import os
import subprocess
import time
import datetime
import stat
import ROOT

sys.path.append(os.path.abspath("/nfs/dust/cms/user/skudella/pyroot-plotscripts/"))
from plot_additional_Zprime_MC import *


def GetKeyNames( self, dir = "" ):
    self.cd(dir)
    return [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
ROOT.TFile.GetKeyNames = GetKeyNames




def createCcode(pathToOutputRootFile,nbins,rebin,SignalNick,systlist=[]):

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

    
void createABCDCombineWorkspaceFile_""" + SignalNick + """(){





    // As usual, load the combine library to get access to the RooParametricHist
    gSystem->Load("libHiggsAnalysisCombinedLimit.so");
    // Output file and workspace 
    TFile *fOut = new TFile("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_datacards/rootfiles/param_ws_""" + SignalNick + """.root","RECREATE");
    RooWorkspace wspace("wspace","wspace");

    // A search in a MET tail, define MET as our variable
    RooRealVar Zprime_M("Zprime_M","m(Zp)",-5000,10000);
    RooArgList vars(Zprime_M);
    
    
    //TH1F data_obs_th1("data_obs_withtbt","Data observed in signal region",4,200,1000);
    TH1 * datahistoA_wtb = 0;
    TH1 * datahistoB_wtb = 0;
    TH1 * datahistoC_wtb = 0;
    TH1 * datahistoD_wtb = 0;
    TH1 * datahistoA_ntb = 0;
    TH1 * datahistoB_ntb = 0;
    TH1 * datahistoC_ntb = 0;
    TH1 * datahistoD_ntb = 0;

    
    TFile* file=TFile::Open(""" + '"' + pathToOutputRootFile + '"' + """);
    file->GetObject("DATA_noSignal_ABCD5_withtopbtag_CatA_Zprime_M_ABCD5_nominal", datahistoA_wtb);
    file->GetObject("DATA_noSignal_ABCD5_withtopbtag_CatB_Zprime_M_ABCD5_nominal", datahistoB_wtb);
    file->GetObject("DATA_noSignal_ABCD5_withtopbtag_CatC_Zprime_M_ABCD5_nominal", datahistoC_wtb);
    file->GetObject("DATA_noSignal_ABCD5_withtopbtag_CatD_Zprime_M_ABCD5_nominal", datahistoD_wtb);
    file->GetObject("DATA_noSignal_ABCD5_notopbtag_CatA_Zprime_M_ABCD5_nominal", datahistoA_ntb);
    file->GetObject("DATA_noSignal_ABCD5_notopbtag_CatB_Zprime_M_ABCD5_nominal", datahistoB_ntb);
    file->GetObject("DATA_noSignal_ABCD5_notopbtag_CatC_Zprime_M_ABCD5_nominal", datahistoC_ntb);
    file->GetObject("DATA_noSignal_ABCD5_notopbtag_CatD_Zprime_M_ABCD5_nominal", datahistoD_ntb);

    

    
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
            print systname
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
    wspace.import(""" + SignalNick + """_histD_ntb_""" + systname + """);"""


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
        
        if(datahistoA_wtb->GetBinContent(j)-ttbarhistoA_wtb_nominal->GetBinContent(j)<0.01){datahistoA_wtb->SetBinContent(j,ttbarhistoA_wtb_nominal->GetBinContent(j)+0.01);};
        if(datahistoB_wtb->GetBinContent(j)-ttbarhistoB_wtb_nominal->GetBinContent(j)<0.01){datahistoB_wtb->SetBinContent(j,ttbarhistoB_wtb_nominal->GetBinContent(j)+0.01);};
        if(datahistoC_wtb->GetBinContent(j)-ttbarhistoC_wtb_nominal->GetBinContent(j)<0.01){datahistoC_wtb->SetBinContent(j,ttbarhistoC_wtb_nominal->GetBinContent(j)+0.01);};
        if(datahistoD_wtb->GetBinContent(j)-ttbarhistoD_wtb_nominal->GetBinContent(j)<0.01){datahistoD_wtb->SetBinContent(j,ttbarhistoD_wtb_nominal->GetBinContent(j)+0.01);};
        if(datahistoA_ntb->GetBinContent(j)-ttbarhistoA_ntb_nominal->GetBinContent(j)<0.01){datahistoA_ntb->SetBinContent(j,ttbarhistoA_ntb_nominal->GetBinContent(j)+0.01);};
        if(datahistoB_ntb->GetBinContent(j)-ttbarhistoB_ntb_nominal->GetBinContent(j)<0.01){datahistoB_ntb->SetBinContent(j,ttbarhistoB_ntb_nominal->GetBinContent(j)+0.01);};
        if(datahistoC_ntb->GetBinContent(j)-ttbarhistoC_ntb_nominal->GetBinContent(j)<0.01){datahistoC_ntb->SetBinContent(j,ttbarhistoC_ntb_nominal->GetBinContent(j)+0.01);};
        if(datahistoD_ntb->GetBinContent(j)-ttbarhistoD_ntb_nominal->GetBinContent(j)<0.01){datahistoD_ntb->SetBinContent(j,ttbarhistoD_ntb_nominal->GetBinContent(j)+0.01);};
    }
    
    RooDataHist data_histA_wtb("DATA_noSignal_ABCD5_withtopbtag_CatA_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoA_wtb);
    RooDataHist data_histB_wtb("DATA_noSignal_ABCD5_withtopbtag_CatB_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoB_wtb);
    RooDataHist data_histC_wtb("DATA_noSignal_ABCD5_withtopbtag_CatC_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoC_wtb);
    RooDataHist data_histD_wtb("DATA_noSignal_ABCD5_withtopbtag_CatD_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoD_wtb);
    RooDataHist data_histA_ntb("DATA_noSignal_ABCD5_notopbtag_CatA_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoA_ntb);
    RooDataHist data_histB_ntb("DATA_noSignal_ABCD5_notopbtag_CatB_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoB_ntb);
    RooDataHist data_histC_ntb("DATA_noSignal_ABCD5_notopbtag_CatC_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoC_ntb);
    RooDataHist data_histD_ntb("DATA_noSignal_ABCD5_notopbtag_CatD_Zprime_M_ABCD5_nominal","Data observed",vars,datahistoD_ntb);


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
    //RooRealVar QCD_ABCD_shape_wtb_m("QCD_ABCD_shape_wtb_m","QCD_ABCD_shape_wtb_m",""" + str(Zprime_withtopbtag_systshape_m) + """,-100,100);
    //RooRealVar QCD_ABCD_shape_wtb_y("QCD_ABCD_shape_wtb_y","QCD_ABCD_shape_wtb_y",""" + str(Zprime_withtopbtag_systshape_c) + """,-100,100);
    RooRealVar QCD_ABCD_shape_ntb("QCD_ABCD_shape_ntb","QCD_ABCD_shape_ntb",0.0,-100,100);
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
    RooFormulaVar QCD_CatA_wtb_bin"""+  str(i) + """("QCD_CatA_wtb_bin"""+  str(i) + '"' + ""","QCD Background yield in signal region with top b-tag, bin"""+  str(i) + '"' + ""","@0*@1/@2*(1+(("""+ str(Zprime_withtopbtag_systshape_m) +""") * """ + str(datahisto.GetBinCenter(i)) + """ + (""" + str(Zprime_withtopbtag_systshape_c) + """) ) * @3 )",RooArgList(QCD_CatB_wtb_bin""" +  str(i) + """,QCD_CatC_wtb_bin""" +  str(i) + """,QCD_CatD_wtb_bin""" +  str(i) + """, QCD_ABCD_shape_wtb));
    RooFormulaVar QCD_CatA_ntb_bin"""+  str(i) + """("QCD_CatA_ntb_bin"""+  str(i) + '"' + ""","QCD Background yield in signal region no top b-tag, bin"""+  str(i) + '"' + ""","@0*@1/@2*(1+((""" + str(Zprime_notopbtag_systshape_m) + """) * """ + str(datahisto.GetBinCenter(i)) + """ + (""" + str(Zprime_notopbtag_systshape_c) + """) ) * @3 )",RooArgList(QCD_CatB_ntb_bin""" +  str(i) + """,QCD_CatC_ntb_bin""" +  str(i) + """,QCD_CatD_ntb_bin""" +  str(i) + """, QCD_ABCD_shape_ntb));
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
    f=open("combine_datacards/cscripts_for_wspace/createABCDCombineWorkspaceFile_" + SignalNick + ".cxx","w")
    f.write(script)
    f.close()
    st = os.stat("combine_datacards/cscripts_for_wspace/createABCDCombineWorkspaceFile_" + SignalNick + ".cxx")
    os.chmod("combine_datacards/cscripts_for_wspace/createABCDCombineWorkspaceFile_" + SignalNick + ".cxx", st.st_mode | stat.S_IEXEC)
   

def createScript(ABCDversion,SignalNick):
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

shapes data_obs CatA_wtb rootfiles/param_ws_""" + SignalNick + """.root wspace:DATA_noSignal_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatB_wtb rootfiles/param_ws_""" + SignalNick + """.root wspace:DATA_noSignal_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatC_wtb rootfiles/param_ws_""" + SignalNick + """.root wspace:DATA_noSignal_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatD_wtb rootfiles/param_ws_""" + SignalNick + """.root wspace:DATA_noSignal_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatA_ntb rootfiles/param_ws_""" + SignalNick + """.root wspace:DATA_noSignal_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatB_ntb rootfiles/param_ws_""" + SignalNick + """.root wspace:DATA_noSignal_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatC_ntb rootfiles/param_ws_""" + SignalNick + """.root wspace:DATA_noSignal_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatD_ntb rootfiles/param_ws_""" + SignalNick + """.root wspace:DATA_noSignal_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + """_nominal

shapes Sig      CatA_wtb rootfiles/param_ws_""" + SignalNick + """.root wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
//shapes Sig      CatB_wtb rootfiles/param_ws_""" + SignalNick + """.root wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
//shapes Sig      CatC_wtb rootfiles/param_ws_""" + SignalNick + """.root wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
//shapes Sig      CatD_wtb rootfiles/param_ws_""" + SignalNick + """.root wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes Sig      CatA_ntb rootfiles/param_ws_""" + SignalNick + """.root wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
//shapes Sig      CatB_ntb rootfiles/param_ws_""" + SignalNick + """.root wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
//shapes Sig      CatC_ntb rootfiles/param_ws_""" + SignalNick + """.root wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
//shapes Sig      CatD_ntb rootfiles/param_ws_""" + SignalNick + """.root wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + """_nominal  wspace:""" + SignalNick + "_"  + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC




shapes tt       CatA_wtb rootfiles/param_ws_""" + SignalNick + """.root wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatB_wtb rootfiles/param_ws_""" + SignalNick + """.root wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatC_wtb rootfiles/param_ws_""" + SignalNick + """.root wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatC_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatD_wtb rootfiles/param_ws_""" + SignalNick + """.root wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_withtopbtag_CatD_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatA_ntb rootfiles/param_ws_""" + SignalNick + """.root wspace:ttbar_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatB_ntb rootfiles/param_ws_""" + SignalNick + """.root wspace:ttbar_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatC_ntb rootfiles/param_ws_""" + SignalNick + """.root wspace:ttbar_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_notopbtag_CatC_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatD_ntb rootfiles/param_ws_""" + SignalNick + """.root wspace:ttbar_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + """_nominal  wspace:ttbar_""" + ABCDversion + """_notopbtag_CatD_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC



shapes QCD      CatA_wtb rootfiles/param_ws_""" + SignalNick + """.root wspace:QCD_CatA_wtb
shapes QCD      CatB_wtb rootfiles/param_ws_""" + SignalNick + """.root wspace:QCD_CatB_wtb
shapes QCD      CatC_wtb rootfiles/param_ws_""" + SignalNick + """.root wspace:QCD_CatC_wtb
shapes QCD      CatD_wtb rootfiles/param_ws_""" + SignalNick + """.root wspace:QCD_CatD_wtb
shapes QCD      CatA_ntb rootfiles/param_ws_""" + SignalNick + """.root wspace:QCD_CatA_ntb
shapes QCD      CatB_ntb rootfiles/param_ws_""" + SignalNick + """.root wspace:QCD_CatB_ntb
shapes QCD      CatC_ntb rootfiles/param_ws_""" + SignalNick + """.root wspace:QCD_CatC_ntb
shapes QCD      CatD_ntb rootfiles/param_ws_""" + SignalNick + """.root wspace:QCD_CatD_ntb

#------------------------------
bin             CatA_ntb   CatB_ntb   CatC_ntb   CatD_ntb     CatA_wtb CatB_wtb CatC_wtb CatD_wtb 
observation     -1         -1         -1         -1           -1       -1       -1       -1
------------------------------
#bin                                CatA_ntb   CatB_ntb   CatC_ntb   CatD_ntb   CatA_wtb CatB_wtb CatC_wtb CatD_wtb     CatA_ntb   CatB_ntb   CatC_ntb   CatD_ntb   CatA_wtb CatB_wtb CatC_wtb CatD_wtb   CatA_ntb   CatB_ntb   CatC_ntb   CatD_ntb   CatA_wtb CatB_wtb CatC_wtb CatD_wtb
bin                                CatA_ntb  CatA_wtb    CatA_ntb   CatB_ntb   CatC_ntb   CatD_ntb   CatA_wtb CatB_wtb CatC_wtb CatD_wtb   CatA_ntb   CatB_ntb   CatC_ntb   CatD_ntb   CatA_wtb CatB_wtb CatC_wtb CatD_wtb
#process                            Sig    Sig    Sig    Sig    Sig    Sig    Sig    Sig        QCD    QCD    QCD    QCD    QCD    QCD    QCD    QCD      tt     tt     tt     tt     tt     tt     tt     tt           
process                            Sig    Sig     QCD    QCD    QCD    QCD    QCD    QCD    QCD    QCD      tt     tt     tt     tt     tt     tt     tt     tt           
#process                            0      0      0      0      0      0      0      0          1      1      1      1      1      1      1      1        2      2      2      2      2      2      2      2
process                            0      0      1      1      1      1      1      1      1      1        2      2      2      2      2      2      2      2
#rate                               -1     -1     -1     -1     -1     -1     -1     -1         1      1      1      1      1      1      1      1        -1     -1     -1     -1     -1     -1     -1     -1
rate                               -1     -1         1      1      1      1      1      1      1      1        -1     -1     -1     -1     -1     -1     -1     -1

--------------------------------
ABCD_wtb_rate       	  lnN      -      -      """+ str(1.0+Zprime_withtopbtag_systrate) +"""  -      -      -      -      -      -      -        -      -      -      -      -      -      -      -       #ABCD uncertainty on QCDbackground
ABCD_ntb_rate             lnN      -      -      -      -      -      -     """+ str(1.0+Zprime_notopbtag_systrate) +"""  -      -      -        -      -      -      -      -      -      -      -       #ABCD uncertainty on QCDbackground 
MCSF_CSVLF                shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVHF                shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVHFStats1          shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVLFStats1          shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVHFStats2          shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVLFStats2          shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVCErr1             shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVCErr2             shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_toptag               shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_Wtag                 shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_PU                   shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_PDF                  shape    -      -      -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar
MCSF_Lumi                 shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_Trigger              shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
MCSF_renfac_env           shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar
nominal_JER               shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
nominal_JES               shape   1.0    1.0     -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
ttbarXS                   shape    -      -      -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC

#ABCD_wtb_rate       	  lnN      -      -      -      -      -      -      -      -         """+ str(1.0+Zprime_withtopbtag_systrate) +"""  -      -      -      -      -      -      -        -      -      -      -      -      -      -      -       #ABCD uncertainty on QCDbackground
#ABCD_ntb_rate             lnN      -      -      -      -      -      -      -      -          -      -      -      -     """+ str(1.0+Zprime_notopbtag_systrate) +"""  -      -      -        -      -      -      -      -      -      -      -       #ABCD uncertainty on QCDbackground 
#MCSF_CSVLF                shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_CSVHF                shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_CSVHFStats1          shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_CSVLFStats1          shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_CSVHFStats2          shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_CSVLFStats2          shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_CSVCErr1             shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_CSVCErr2             shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_toptag               shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_Wtag                 shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_PU                   shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_PDF                  shape    -      -      -      -      -      -      -      -          -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar
#MCSF_Lumi                 shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_Trigger              shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#MCSF_renfac_env           shape    -      -      -      -      -      -      -      -          -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar
#nominal_JER               shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#nominal_JES               shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC
#ttbarXS                   shape   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0         -      -      -      -      -      -      -      -       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0      #MCSF uncertainty from ttbar and SC

#art_rate_un                lnN     1.01   1.01   1.01   1.01   1.01   1.01   1.01   1.01        -      -      -      -      -      -      -      -       1.02   1.02   1.02   1.02   1.02   1.02   1.02   1.02     


# free floating parameters, we do not need to declare them, but its a good idea to 

QCD_ABCD_shape_wtb      param 0.0 1.0
QCD_ABCD_shape_ntb      param 0.0 1.0

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
  
  
  
  f=open('combine_datacards/'+SignalNick+'_'+ABCDversion+'Combine_datacard.txt','w')
  f.write(script)
  f.close()
  #st = os.stat(datacardname)
  #os.chmod(datacardname, st.st_mode | stat.S_IEXEC)




##################################################### Script starts here ######################


print "Creating Ccode for Workspacefiles"

cmsswpath="/nfs/dust/cms/user/skudella/CMSSW_7_4_7"

indir = "/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST"
outdir= "/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST"

pathToOutputRootFile=indir + "/rootfiles/output_rebinned_added_CMSSW_WP.root"




f=ROOT.TFile(pathToOutputRootFile, "readonly")
#print "looking at file ", 
keyList = f.GetKeyNames()    
for key in keyList:
    #if ("Zprime_M" in key) and ("ABCD" in key) and ("nominal" in key) and ("Tprime" not in key) and ("CatA" in key):
    #print key
    if ("DATA_noSignal" in key) and ("ABCD" in key) and ("nominal" in key) and ("Tprime" not in key) and ("inclusive" not in key) and ("Zprime_M" in key) and ("CatA" in key):
        datahisto=f.Get(key)
        print key, " selected to extract binning"
        break

nbins=datahisto.GetNbinsX()

rebin=1
print "number of mass bins=", nbins    
nbins=nbins/rebin
print "rebinning to ", nbins
   
systlist=["nominal","MCSF_CSVLFUp","MCSF_CSVHFUp","MCSF_CSVHFStats1Up","MCSF_CSVLFStats1Up","MCSF_CSVHFStats2Up","MCSF_CSVLFStats2Up","MCSF_CSVCErr1Up","MCSF_CSVCErr2Up","MCSF_toptagUp","MCSF_WtagUp","MCSF_PUUp","MCSF_PDFUp","MCSF_LumiUp","MCSF_TriggerUp","MCSF_renfac_envUp","nominal_JERUp","nominal_JESUp","ttbarXSUp","MCSF_CSVLFDown","MCSF_CSVHFDown","MCSF_CSVHFStats1Down","MCSF_CSVLFStats1Down","MCSF_CSVHFStats2Down","MCSF_CSVLFStats2Down","MCSF_CSVCErr1Down","MCSF_CSVCErr2Down","MCSF_toptagDown","MCSF_WtagDown","MCSF_PUDown","MCSF_PDFDown","MCSF_LumiDown","MCSF_TriggerDown","MCSF_renfac_envDown","nominal_JERDown","nominal_JESDown","ttbarXSDown"]
    
    

print 'Creating datacards'

cmsswpath='/nfs/dust/cms/user/skudella/CMSSW_7_4_7'
#SignalNickList=["SigZprime15001200_tWb"]
SignalNickList=["SigZprime15001200_tWb","SigZprime20001200_tWb","SigZprime25001200_tWb","SigZprime1500700_tWb","SigZprime1500900_tWb","SigZprime2000900_tWb","SigZprime20001500_tWb","SigZprime25001500_tWb"]+["SigZprime15001200_ttZ","SigZprime20001200_ttZ","SigZprime25001200_ttZ","SigZprime1500700_ttZ","SigZprime1500900_ttZ","SigZprime2000900_ttZ","SigZprime20001500_ttZ","SigZprime25001500_ttZ"]+["SigZprime15001200_ttH","SigZprime20001200_ttH","SigZprime25001200_ttH","SigZprime1500900_ttH","SigZprime2000900_ttH","SigZprime20001500_ttH","SigZprime25001500_ttH"]+["SigZprime15001200_BR05_025_025","SigZprime20001200_BR05_025_025","SigZprime25001200_BR05_025_025","SigZprime1500700_BR05_025_025","SigZprime1500900_BR05_025_025","SigZprime2000900_BR05_025_025","SigZprime20001500_BR05_025_025","SigZprime25001500_BR05_025_025"]
#SignalNickList=["SigZprime25001500_tWb"]

#SignalNickList=["SigZprime15001200_tWb","SigZprime20001200_tWb","SigZprime25001200_tWb","SigZprime1500700_tWb","SigZprime1500900_tWb","SigZprime2000900_tWb","SigZprime20001500_tWb","SigZprime25001500_tWb"]+["SigZprime15001200_ttZ","SigZprime20001200_ttZ","SigZprime25001200_ttZ","SigZprime1500700_ttZ","SigZprime1500900_ttZ","SigZprime2000900_ttZ","SigZprime20001500_ttZ","SigZprime25001500_ttZ"]+["SigZprime15001200_ttH","SigZprime20001200_ttH","SigZprime25001200_ttH","SigZprime1500700_ttH","SigZprime1500900_ttH","SigZprime2000900_ttH","SigZprime20001500_ttH","SigZprime25001500_ttH"]+["SigZprime15001200_BR05_025_025","SigZprime20001200_BR05_025_025","SigZprime25001200_BR05_025_025","SigZprime1500700_BR05_025_025","SigZprime1500900_BR05_025_025","SigZprime2000900_BR05_025_025","SigZprime20001500_BR05_025_025","SigZprime25001500_BR05_025_025"]

#SignalNickList=["SigZprime15001200","SigZprime20001200","SigZprime25001200","SigZprime1500700","SigZprime1500900","SigZprime2000900","SigZprime20001500","SigZprime25001500","SigGstar1500800Nar","SigGstar15001000Nar","SigGstar15001300Nar","SigGstar20001000Nar","SigGstar20001300Nar","SigGstar20001500Nar","SigGstar25001300Nar","SigGstar25001500Nar","SigGstar25001800Nar","SigGstar30001500Nar","SigGstar30001800Nar","SigGstar30002100Nar","SigGstar35001800Nar","SigGstar35002100Nar","SigGstar35002500Nar","SigGstar40002100Nar","SigGstar40002500Nar","SigGstar40003000Nar","SigGstar1500800Wid","SigGstar15001000Wid","SigGstar15001300Wid","SigGstar20001000Wid","SigGstar20001300Wid","SigGstar20001500Wid","SigGstar25001300Wid","SigGstar25001500Wid","SigGstar25001800Wid","SigGstar30001500Wid","SigGstar30001800Wid","SigGstar30002100Wid","SigGstar35001800Wid","SigGstar35002100Wid","SigGstar35002500Wid","SigGstar40002100Wid","SigGstar40002500Wid","SigGstar40003000Wid","SigGstar17501300Nar","SigGstar22501300Nar","SigGstar22501500Nar","SigGstar27501500Nar","SigGstar17501300Wid","SigGstar22501300Wid","SigGstar22501500Wid","SigGstar27501500Wid"]
ABCDversion='ABCD5'
    
    
    
    
    
for SignalNick in SignalNickList:    
    createCcode(pathToOutputRootFile,nbins,rebin,SignalNick,systlist)





for SignalNick in SignalNickList:
    createScript(ABCDversion,SignalNick)
