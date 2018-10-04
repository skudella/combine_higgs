from ROOT import *
#from tdrStyle import *
#setTDRStyle()
        
import os,sys,glob
from array import array

#import TColor

gStyle.SetOptStat(0)

gROOT.SetBatch(kTRUE)
unsortedmass = []

mass = array('d',[])
zeros = array('d',[])
exp_p2 = array('d',[])
exp_p1 = array('d',[])
exp = array('d',[])
exp_m1 = array('d',[])
exp_m2 = array('d',[])
obs = array('d',[])


#files=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/plotutils_workspaces/Sig*1200*ABCD3_plotutils/higgs*.root")
#filestWb_Rho=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*tWb*ABCD5_CMS_WP/Asymptotic/higgs*.root")
#filesttZ_Rho=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*ttZ*ABCD5_CMS_WP/Asymptotic/higgs*.root")
#filesttH_Rho=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*ttH*ABCD5_CMS_WP/Asymptotic/higgs*.root")Figure~\ref{fig_limits-rho}
#filesBR_Rho=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*BR*ABCD5_CMS_WP/Asymptotic/higgs*.root")

#filestWb_Gstar=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*tWb*ABCD5_CMS_WP/Asymptotic/higgs*.root")
#filesttZ_Gstar=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*ttZ*ABCD5_CMS_WP/Asymptotic/higgs*.root")
#filesttH_Gstar=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*ttH*ABCD5_CMS_WP/Asymptotic/higgs*.root")
#filesBR_Gstar=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*BR*ABCD5_CMS_WP/Asymptotic/higgs*.root")


filestWb_Rho=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*tWb*ABCD5/Asymptotic/higgs*.root")
filesttZ_Rho=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*ttZ*ABCD5/Asymptotic/higgs*.root")
filesttH_Rho=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*ttH*ABCD5/Asymptotic/higgs*.root")
filesBR_Rho=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*BR*ABCD5/Asymptotic/higgs*.root")

filestWb_GstarNar=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*tWbNar*ABCD5/Asymptotic/higgs*.root")
filesttZ_GstarNar=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*ttZNar*ABCD5/Asymptotic/higgs*.root")
filesttH_GstarNar=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*ttHNar*ABCD5/Asymptotic/higgs*.root")
filesBR_GstarNar=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*BR05_025_025Nar*ABCD5/Asymptotic/higgs*.root")

filestWb_GstarWid=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*tWbWid*ABCD5/Asymptotic/higgs*.root")
filesttZ_GstarWid=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*ttZWid*ABCD5/Asymptotic/higgs*.root")
filesttH_GstarWid=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*ttHWid*ABCD5/Asymptotic/higgs*.root")
filesBR_GstarWid=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*BR05_025_025Wid*ABCD5/Asymptotic/higgs*.root")


def drawhisto(Zp_mass,Tp_mass,originalZmass,originalTmass,limits,exp,exp_p2,exp_p1,exp_m1,exp_m2,model,label=""):
    
    print Zp_mass,Tp_mass,exp
    #raw_input()
    
    c = TCanvas("c","c",800, 650)
    nbinsX=len(originalZmass)
    nbinsY=len(originalTmass)
    xbinslist=[]
    ybinslist=[]

    
    for i in range(len(originalZmass)):
        if i==0:
            xbinslist.append(originalZmass[i]-(originalZmass[i+1]-originalZmass[i])/2.0)
            xbinslist.append(originalZmass[i]+(originalZmass[i+1]-originalZmass[i])/2.0)
        elif i==len(originalZmass)-1:
            xbinslist.append(originalZmass[i]+(originalZmass[i]-originalZmass[i-1])/2.0)
        else:
            xbinslist.append(originalZmass[i]+(originalZmass[i+1]-originalZmass[i])/2.0)


    for i in range(len(originalTmass)):
        if i==0:
            ybinslist.append(originalTmass[i]-(originalTmass[i+1]-originalTmass[i])/2.0)
            ybinslist.append(originalTmass[i]+(originalTmass[i+1]-originalTmass[i])/2.0)
        elif i==len(originalTmass)-1:
            ybinslist.append(originalTmass[i]+(originalTmass[i]-originalTmass[i-1])/2.0)
        else:
            ybinslist.append(originalTmass[i]+(originalTmass[i+1]-originalTmass[i])/2.0)
            
    print xbinslist
    print ybinslist
    
    xbins=array('d',xbinslist)
    ybins=array('d',ybinslist)
    
    hist=TH2D("","",len(xbins)-1,xbins,len(ybins)-1,ybins)
    hist2=TH2D("","",len(xbins)-1,xbins,len(ybins)-1,ybins)
    hist2_red=TH2D("","",len(xbins)-1,xbins,len(ybins)-1,ybins)
    hist2_p2=TH2D("","",len(xbins)-1,xbins,len(ybins)-1,ybins)
    hist2_p1=TH2D("","",len(xbins)-1,xbins,len(ybins)-1,ybins)
    hist2_m1=TH2D("","",len(xbins)-1,xbins,len(ybins)-1,ybins)
    hist2_m2=TH2D("","",len(xbins)-1,xbins,len(ybins)-1,ybins)
    print nbinsX
    minlimit=1.0
    maxlimit=1.0
    for i in range(1,nbinsX+1):
        hist.GetXaxis().SetBinLabel(i, str(originalZmass[i-1]/1000.0))
        print "ix",i,"  ",str(originalZmass[i-1])
    for i in range(1,nbinsY+1):
        hist.GetYaxis().SetBinLabel(i, str(originalTmass[i-1]/1000.0))
        print "iy",i,"  ",str(originalTmass[i-1])
    for mZ,mT,limit,lexp,lexp_p2,lexp_p1,lexp_m1,lexp_m2 in zip(Zp_mass,Tp_mass,limits,exp,exp_p2,exp_p1,exp_m1,exp_m2):
        hist.GetXaxis()
        hist.SetBinContent(hist.GetXaxis().FindBin(mZ),hist.GetYaxis().FindBin(mT),limit)
        print "xbin",hist.GetXaxis().FindBin(mZ),"ybin",hist.GetYaxis().FindBin(mZ),"limit",limit
        if limit<minlimit:
            minlimit=minlimit/10.0
        if limit>maxlimit:
            maxlimit=limit*10.0
        roundlimit=limit
        roundigit=0
        for i in range(10):
            if roundlimit<1.0:
                roundlimit=roundlimit*10
                roundigit+=1
        print   roundigit
        #raw_input()
        hist2.SetBinContent(hist.GetXaxis().FindBin(mZ),hist.GetYaxis().FindBin(mT),round(limit,roundigit+1))
        hist2_p2.SetBinContent(hist.GetXaxis().FindBin(mZ),hist.GetYaxis().FindBin(mT),round(lexp_p2,roundigit+1))
        hist2_p1.SetBinContent(hist.GetXaxis().FindBin(mZ),hist.GetYaxis().FindBin(mT),round(lexp_p1,roundigit+1))
        hist2_m1.SetBinContent(hist.GetXaxis().FindBin(mZ),hist.GetYaxis().FindBin(mT),round(lexp_m1,roundigit+1))
        hist2_m2.SetBinContent(hist.GetXaxis().FindBin(mZ),hist.GetYaxis().FindBin(mT),round(lexp_m2,roundigit+1))
    
        if(limit>(lexp_p2+lexp)):
        #if (label=="obs") and ((limit>0.5) or (limit<0.025)):
            
            hist2_red.SetBinContent(hist.GetXaxis().FindBin(mZ),hist.GetYaxis().FindBin(mT),round(limit,roundigit+1))
            print "WTF ",limit,"  lexp_p2" ,lexp_p2," lexp_p1",lexp_p1, "  lexp_m1",lexp_m1,"  lexp_m2",lexp_m2
        
    hist.GetXaxis().SetTitle("m_{Z'} in TeV")   
    hist.GetXaxis().SetTitleSize(0.05)   
    hist.GetXaxis().SetNdivisions(0)  
    hist.GetXaxis().SetTickLength(0.0)  
    hist2.GetXaxis().SetTickLength(0.0)  
    
    hist2.GetXaxis().SetNdivisions(0)   
    hist.GetYaxis().SetTitle("m_{T} in TeV")   
    hist.GetYaxis().SetTitleSize(0.05) 
    hist.GetYaxis().SetNdivisions(0)      
    hist.GetYaxis().SetTickLength(0.0)  
    hist2.GetYaxis().SetTickLength(0.0)  
    hist2.GetYaxis().SetNdivisions(0)  
    hist.GetZaxis().SetTitle("expected limit (95% CL) in pb")   
    if (label=="obs"):
        #hist.GetZaxis().SetTitle("observed limit (95% CL) in pb")  
        hist.GetZaxis().SetTitle("beobachtetes limit (95% CL) in pb")  
        
    if decaymode is "BR05_025_025Nar":
        hist.GetZaxis().SetRangeUser(0.01,5.0)   
    if decaymode is "BR05_025_025Wid":
        hist.GetZaxis().SetRangeUser(0.01,1.0)   
   
    
    hist.GetZaxis().SetTitleSize(0.05)   
    hist.GetZaxis().SetLabelSize(0.04)  

    hist.GetXaxis().SetLabelSize(0.07)  
    hist.GetYaxis().SetLabelSize(0.07)  
    
    
    c.SetLogz()

    c.SetRightMargin(0.15)
    c.SetLeftMargin(0.11)
    c.SetTopMargin(0.15)
    c.SetBottomMargin(0.11)
    
    MyPalette=[]
    r=array('d',[0.0,0.0, 1.0])
    g=array('d',[1.0,0.0, 0.0])
    b=array('d',[1.0,1.0, 0.5])
    stop=array('d',[.00,0.5, 1.0])    
    
    FI = TColor.CreateGradientColorTable(3, stop, r, g, b, 50)
    for i in range(0,50):
        MyPalette.append( FI+i)
    
    print MyPalette
    a=array('i',MyPalette)
    
    gStyle.SetPalette(50,a)
    
    #hist.Draw("CONTZ")
    
    hist.Draw("colz")
    hist2.SetMarkerSize(2)
    hist2_red.SetMarkerSize(1.5)
    hist2_p2.SetMarkerSize(1.5)
    hist2_p2.SetBarOffset(0.4)
    hist2_p1.SetMarkerSize(1.5)
    hist2_p1.SetBarOffset(0.2)
    hist2_m1.SetMarkerSize(1.5)
    hist2_m1.SetBarOffset(-0.2)
    hist2_m2.SetMarkerSize(1.5)
    hist2_m2.SetBarOffset(-0.4)
    #if (label=="obs"):
        #hist2.SetMarkerColor(kRed)
        
    
    if model=="Rho":
    
        hist2.Draw("TEXT SAME")
    
    if (label=="obs"):
        hist2_red.SetMarkerColor(kRed)
        hist2_red.Draw("TEXT SAME")
        
    #hist2_p2.Draw("TEXT SAME")
    #hist2_p1.Draw("TEXT SAME")
    #hist2_m1.Draw("TEXT SAME")
    #hist2_m2.Draw("TEXT SAME")
    
  
    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.4*0.15)
    latex2.SetTextFont(42)
    latex2.SetTextAlign(35) # align right
    latex2.DrawLatex(0.98, 0.94,"35.9 fb^{-1} (13 TeV)")
    latex2.SetTextSize(0.4*0.15)
    latex2.SetTextFont(42)
    latex2.SetTextAlign(11) # align right
    latex2.DrawLatex(0.02, 0.94, "CMS")
    latex2.SetTextSize(0.4*0.15)
    latex2.SetTextFont(42)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.15, 0.94, "private work")
    
    latex3 = TLatex()
    latex3.SetNDC()
    latex3.SetTextSize(0.35*c.GetTopMargin())
    latex3.SetTextFont(42)
    
    if decaymode is "BR05_025_025":
        latex3.DrawLatex(0.115, 0.87, "#Gamma_{Z'}/m_{Z'}=1%, BR(T#rightarrow Wb/Ht/Zt)=50%/25%/25%")
    elif decaymode is "tWb":
        latex3.DrawLatex(0.115, 0.87, "#Gamma_{Z'}/m_{Z'}=1%, BR(T#rightarrow Wb/Ht/Zt)=100%/0%/0%")
    elif decaymode is "ttZ":
        latex3.DrawLatex(0.115, 0.87, "#Gamma_{Z'}/m_{Z'}=1%, BR(T#rightarrow Wb/Ht/Zt)=0%/100%/0%")
    elif decaymode is "ttH":
        latex3.DrawLatex(0.115, 0.87, "#Gamma_{Z'}/m_{Z'}=1%, BR(T#rightarrow Wb/Ht/Zt)=0%/0%/100%")

    
    if decaymode is "BR05_025_025Nar":
        latex3.DrawLatex(0.115, 0.87, "#Gamma_{Z'}/m_{Z'}=1%, BR(T#rightarrow Wb/Ht/Zt)=50%/25%/25%")
    elif decaymode is "tWbNar":
        latex3.DrawLatex(0.115, 0.87, "#Gamma_{Z'}/m_{Z'}=1%, BR(T#rightarrow Wb/Ht/Zt)=100%/0%/0%")
    elif decaymode is "ttZNar":
        latex3.DrawLatex(0.115, 0.87, "#Gamma_{Z'}/m_{Z'}=1%, BR(T#rightarrow Wb/Ht/Zt)=0%/100%/0%")
    elif decaymode is "ttHNar":
        latex3.DrawLatex(0.115, 0.87, "#Gamma_{Z'}/m_{Z'}=1%, BR(T#rightarrow Wb/Ht/Zt)=0%/0%/100%")

    if decaymode is "BR05_025_025Wid":
        latex3.DrawLatex(0.115, 0.87, "#Gamma_{Z'}/m_{Z'}=30%, BR(T#rightarrow Wb/Ht/Zt)=50%/25%/25%")
    elif decaymode is "tWbWid":
        latex3.DrawLatex(0.115, 0.87, "#Gamma_{Z'}/m_{Z'}=30%, BR(T#rightarrow Wb/Ht/Zt)=100%/0%/0%")
    elif decaymode is "ttZWid":
        latex3.DrawLatex(0.115, 0.87, "#Gamma_{Z'}/m_{Z'}=30%, BR(T#rightarrow Wb/Ht/Zt)=0%/100%/0%")
    elif decaymode is "ttHWid":
        latex3.DrawLatex(0.115, 0.87, "#Gamma_{Z'}/m_{Z'}=30%, BR(T#rightarrow Wb/Ht/Zt)=0%/0%/100%")


    latex4 = TLatex()
    latex4.SetNDC()
    latex4.SetTextSize(0.35*c.GetTopMargin())
    latex4.SetTextFont(42)    
    latex4.DrawLatex(0.2, 0.7, "m_{Z'} < m_{T}")
    
    latex5 = TLatex()
    latex5.SetNDC()
    latex5.SetTextSize(0.35*c.GetTopMargin())
    latex5.SetTextFont(42)    
    latex5.DrawLatex(0.2, 0.63, "Z' #rightarrow t#bar{t}")

    latex6 = TLatex()
    latex6.SetNDC()
    latex6.SetTextSize(0.35*c.GetTopMargin())
    latex6.SetTextFont(42)    
    latex6.DrawLatex(0.6, 0.25, "m_{Z'} > 2m_{T}")
    
    latex7 = TLatex()
    latex7.SetNDC()
    latex7.SetTextSize(0.35*c.GetTopMargin())
    latex7.SetTextFont(42)    
    latex7.DrawLatex(0.6, 0.18, "Z' #rightarrow T#bar{T}")

    
    c.SaveAs("limit_2D_"+model+"_"+decaymode+"_"+label+".pdf")
    

def drawlimits(files,decaymode,model):
    print files
    if model=="Rho":
        originalZmass=[1500,2000,2500]
        originalTmass=[700,900,1200,1500]
    if model=="Gstar":
        #originalZmass=[1500,1750,2000,2250,2500,2750,3000,3500,4000]
        originalZmass=[1500,2000,2500,3000,3500,4000]
        originalTmass=[800,1000,1300,1500,1800,2100,2500,3000]
        if "Wid" in decaymode:
            originalZmass=[1500,2000,2500,3000,3500,4000]
            originalTmass=[800,1000,1300,1500,1800,2100,2500,3000]        
    unsortedZmass=[]
    unsortedTmass=[]
    for afile in files:
        print afile
        #for zm in [1500,1750,2000,2250,2500,2750,3000,3500,4000]:
        for zm in originalZmass:
          for tm in originalTmass:  
            if (zm!=tm) and (str(zm) in afile) and (str(tm) in afile):
                print zm," and ",tm, " in ", afile
                unsortedZmass.append(zm)
                unsortedTmass.append(tm)
    #unsortedZmass.sort()
    #unsortedTmass.sort()
    
    #print unsortedmass
    Zp_mass=[]
    Tp_mass=[]
    
    print "here"
    print unsortedZmass,unsortedTmass
    #raw_input()
    
    for zm,tm in zip(unsortedZmass,unsortedTmass):
      #for tm in unsortedTmass:
        print "here3"
        thisexp=0.0
        
        if model=="Rho":
            filename="/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho"+str(zm)+str(tm)+"_"+decaymode+"_ABCD5/Asymptotic/higgsCombine_Asymptotic.Asymptotic.mH120.root"
        if model=="Gstar":
            filename="/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar"+str(zm)+str(tm)+"_"+decaymode+"_ABCD5/Asymptotic/higgsCombine_Asymptotic.Asymptotic.mH120.root"
            
        if(os.path.isfile(filename)): 
            emanueles_limit=1
            print "m_{Z'}=",zm,"  m(T)=",tm

            
            Zp_mass.append(zm)
            Tp_mass.append(tm)

        #if decaymode is "BR":
            #f = TFile("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigZprime"+str(zm)+str(tm)+"_BR05_025_025_ABCD5_CMS_WP/Asymptotic/higgsCombine_Asymptotic.Asymptotic.mH120.root","READ")
        #elif decaymode is "tWb":
            #f = TFile("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigZprime"+str(zm)+str(tm)+"_tWb_ABCD5_CMS_WP/Asymptotic/higgsCombine_Asymptotic.Asymptotic.mH120.root","READ")
        #elif decaymode is "ttZ":
            #f = TFile("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigZprime"+str(zm)+str(tm)+"_ttZ_ABCD5_CMS_WP/Asymptotic/higgsCombine_Asymptotic.Asymptotic.mH120.root","READ")
        #elif decaymode is "ttH":
            #f = TFile("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigZprime"+str(zm)+str(tm)+"_ttH_ABCD5_CMS_WP/Asymptotic/higgsCombine_Asymptotic.Asymptotic.mH120.root","READ")
        #else:
            #print "hihi"
            f = TFile(filename,"READ")

        #filename=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/plotutils_workspaces/SigZprime"+str(m)+"1200*"+decaymode+"*ABCD5_CMS_WP/higgsCombine_Asymptotic.Asymptotic.mH120.root")
        #print decaymode,"  ", filename
        #f = TFile(filename[0],"READ")
            t = f.Get("limit")
            print t
            t.Print()
            zeros.append(0.0)
        
            t.GetEntry(2)
            thisexp = t.limit
            exp.append((thisexp)*emanueles_limit)
        
            t.GetEntry(0)
            exp_m2.append((thisexp-t.limit)*emanueles_limit)
    
            t.GetEntry(1)
            exp_m1.append((thisexp-t.limit)*emanueles_limit)
    
            t.GetEntry(3)
            exp_p1.append((t.limit-thisexp)*emanueles_limit)
    
            t.GetEntry(4)
            exp_p2.append((t.limit-thisexp)*emanueles_limit)
    
            t.GetEntry(5)
            obs.append((t.limit)*emanueles_limit)
        
        
    print "Zp_mass" ,Zp_mass   
    print "Tp_mass" ,Tp_mass   
    print "obs", obs
    print "exp_p2",exp_p2
    print "exp_p1",exp_p1
    print "exp",exp
    print "exp_m1",exp_m1
    print "exp_m2",exp_m2
    
    drawhisto(Zp_mass,Tp_mass,originalZmass,originalTmass,exp,exp,exp_p2,exp_p1,exp_m1,exp_m2,model,"exp")
    drawhisto(Zp_mass,Tp_mass,originalZmass,originalTmass,obs,exp,exp_p2,exp_p1,exp_m1,exp_m2,model,"obs")
    


#for files,decaymode,model in zip([filestWb_GstarNar],["tWbNar"],["Gstar"]):
#for files,decaymode,model in zip([filesttZ_GstarNar],["ttZNar"],["Gstar"]):
#for files,decaymode,model in zip([filesttH_GstarNar],["ttHNar"],["Gstar"]):
for files,decaymode,model in zip([filesBR_GstarNar],["BR05_025_025Nar"],["Gstar"]):


#for files,decaymode,model in zip([filestWb_GstarWid],["tWbWid"],["Gstar"]):
#for files,decaymode,model in zip([filesttZ_GstarWid],["ttZWid"],["Gstar"]):
#for files,decaymode,model in zip([filesttH_GstarWid],["ttHWid"],["Gstar"]):
#for files,decaymode,model in zip([filesBR_GstarWid],["BR05_025_025Wid"],["Gstar"]):



#for files,decaymode,model in zip([filestWb_Rho],["tWb"],["Rho"]):
#for files,decaymode,model in zip([filesttZ_Rho],["ttZ"],["Rho"]):
#for files,decaymode,model in zip([filesttH_Rho],["ttH"],["Rho"]):
#for files,decaymode,model in zip([filesBR_Rho],["BR05_025_025"],["Rho"]):
    drawlimits(files,decaymode,model)