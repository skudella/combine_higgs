from ROOT import *
#from tdrStyle import *
#setTDRStyle()
        
import os,sys,glob
from array import array

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
filestWbNar=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*1300*tWbNar*ABCD5/Asymptotic/higgs*.root")
filesttZNar=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*1300*ttZNar*ABCD5/Asymptotic/higgs*.root")
filesttHNar=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*1300*ttHNar*ABCD5/Asymptotic/higgs*.root")
filesBRNar=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*1300*BR05_025_025Nar*ABCD5/Asymptotic/higgs*.root")

filestWbWid=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*1300*tWbWid*ABCD5/Asymptotic/higgs*.root")
filesttZWid=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*1300*ttZWid*ABCD5/Asymptotic/higgs*.root")
filesttHWid=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*1300*ttHWid*ABCD5/Asymptotic/higgs*.root")
filesBRWid=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*1300*BR05_025_025Wid*ABCD5/Asymptotic/higgs*.root")


def drawlimits(files,decaymode):
     
    
    unsortedmass=[]
    for afile in files:
      print afile
      if ("Nar" in decaymode):  
        for zm in [1500,1750,2000,2250,2500]:
            if str(zm) in afile:
                print zm, " in ", afile
                unsortedmass.append(zm)
      if ("Wid" in decaymode):  
        for zm in [1500,2000,2500]:
            if str(zm) in afile:
                print zm, " in ", afile
                unsortedmass.append(zm)
                                
                
    unsortedmass.sort()
    print unsortedmass
    for m in unsortedmass:
        
        filename="/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar"+str(m)+"1300_"+decaymode+"_ABCD5/Asymptotic/higgsCombine_Asymptotic.Asymptotic.mH120.root"
        if(os.path.isfile(filename)): 
            if decaymode in ("BR05_025_025Nar") and (m>1900):
                decaymode="BR05_025_025Wid"
            
            if decaymode in ("BR05_025_025Nar") and (m==2000):
                continue
            
            if decaymode in ("BR05_025_025Wid") and (m==2250):
                continue
                        
            emanueles_limit=1

        #if m is 1500:
            #emanueles_limit=8.6
            #emanueles_limit=8.6
        #if m is 2000:
            #emanueles_limit=0.29
            #emanueles_limit=0.29
        #if m is 2500:
            #emanueles_limit=0.3
            #emanueles_limit=0.3
    
        #if decaymode is "BR":
            f = TFile("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar"+str(m)+"1300_"+decaymode+"_ABCD5/Asymptotic/higgsCombine_Asymptotic.Asymptotic.mH120.root","READ")
        
            print m
            #m=float(m)/1000.0    
            mass.append(m)    

        #elif decaymode is "tWb":
            #f = TFile("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar"+str(m)+"1300_"+decaymode+"_ABCD5/Asymptotic/higgsCombine_Asymptotic.Asymptotic.mH120.root","READ")
        ##elif decaymode is "ttZ":
            #f = TFile("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar"+str(m)+"1300_"+decaymode+"_ABCD5/Asymptotic/higgsCombine_Asymptotic.Asymptotic.mH120.root","READ")
        ##elif decaymode is "ttH":
            #f = TFile("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar"+str(m)+"1300_"+decaymode+"_ABCD5/Asymptotic/higgsCombine_Asymptotic.Asymptotic.mH120.root","READ")
        #else:
            #print "hihi"

        #filename=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/plotutils_workspaces/SigZprime"+str(m)+"1200*"+decaymode+"*ABCD5/higgsCombine_Asymptotic.Asymptotic.mH120.root")
        #print decaymode,"  ", filename
        #f = TFile(filename[0],"READ")
            t = f.Get("limit")
            print f
            #print "/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar"+str(m)+"1300_"+decaymode+"_ABCD5/Asymptotic/higgsCombine_Asymptotic.Asymptotic.mH120.root"  
            t.Print()
            zeros.append(0.0)
        
            t.GetEntry(2)
            thisexp = t.limit
            print "thisexp ",thisexp
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
            print "thisobs ",t.limit
            obs.append((t.limit)*emanueles_limit)
            
        
    
    x_theory=       array('d', [1500.0 ,1600.0 ,1700.0 ,1800.0 ,1900.0 ,2000.0   ,2050.0  ,2100.0  ,2200.0  ,2300.0 ,2400.0 ,2450.0   ,2500.0])
    #x_theory=       array('d', [1.500 ,1.600 ,1.700 ,1.800 ,1.900 ,2.000   ,2.050  ,2.100  ,2.200  ,2.300 ,2.400 ,2.450   ,2.5000])
    theory =        array('d', [1.4    ,1.87   ,1.57   ,1.28   ,1.01    ,0.38    ,0.34    ,0.258   ,0.18    ,0.132  ,0.106  ,0.042    ,0.021]) # Gstar
    theory_mT1300 = array('d', [1.24465,1.74839,1.50185,1.23982,0.985793,0.372771,0.334172,0.253989,0.177661,0.13054,0.104987,0.114843,0.0707403])#gstar
    x_theory2= array('d', [1500  ,1550      ,1600      ,1650      ,1700       ,1750      ,1800      ,1850     ,1900     ,1950      ,2000      ,2050      ,2100      ,2150     ,2200     ,2250      ,2300      ,2350     ,2400       ,2450      ,  2500])
    theory2  = array('d', [0.1096, 0.0941941, 0.0812049, 0.0702895,  0.0610887, 0.0531233, 0.0462985, 0.040349, 0.035255, 0.0309674, 0.0272837, 0.0239634, 0.0210468, 0.018506,0.0162989, 0.0143873, 0.0127257,0.0112562, 0.00997291,0.00885648,    0.00788735]) # rho
    
    
    #em_p2  = array('d', []) # Gstar
    #em_p1  = array('d', []) # Gstar
    #em  = array('d', []) # Gstar
    #em_m1  = array('d', []) # Gstar
    #em_m2  = array('d', []) # Gstar
    #if decaymode is "BR":
        #em_obs  = array('d', [8.6,0.27,0.33]) # Gstar
    #if decaymode is "tWb":
        #em_obs  = array('d', [8.6,0.4,0.3]) # Gstar
    #if decaymode is "ttZ":
        #em_obs  = array('d', [3.1,0.29,0.18]) # Gstar
    #if decaymode is "ttH":
        #em_obs  = array('d', [11.0,0.54,0.26]) # Gstar
    #if decaymode is "BR":
        #em_exp  = array('d', [8.0,0.45,0.2]) # Gstar
    #if decaymode is "tWb":
        #em_exp  = array('d', [7.7,0.48,0.23]) # Gstar
    #if decaymode is "ttZ":
        #em_exp  = array('d', [3.1,0.29,0.18]) # Gstar
    #if decaymode is "ttH":
        #em_exp  = array('d', [2.6,0.48,0.29]) # Gstar
            
    v_mass = TVectorD(len(mass),mass)
    v_zeros = TVectorD(len(zeros),zeros)
    v_exp_p2 = TVectorD(len(exp_p2),exp_p2)
    v_exp_p1 = TVectorD(len(exp_p1),exp_p1)
    v_exp = TVectorD(len(exp),exp)
    v_exp_m1 = TVectorD(len(exp_m1),exp_m1)
    v_exp_m2 = TVectorD(len(exp_m2),exp_m2)
    
    v_obs = TVectorD(len(obs),obs)
    
    #v_em_p2 = TVectorD(len(em_p2),em_p2)
    #v_em_p1 = TVectorD(len(em_p1),em_p1)
    #v_em = TVectorD(len(em),em)
    #v_em_m1 = TVectorD(len(em_m1),em_m1)
    #v_em_m2 = TVectorD(len(em_m2),em_m2)
    #v_em_obs = TVectorD(len(em_obs),em_obs)
    #v_em_exp = TVectorD(len(em_exp),em_exp)
    
    
    
    v_theory = TVectorD(len(theory_mT1300),theory_mT1300)
    v_theory_masses = TVectorD(len(x_theory),x_theory)
    v_theory2 = TVectorD(len(theory2),theory2)
    v_theory_masses2 = TVectorD(len(x_theory2),x_theory2)
    
    
    c = TCanvas("c","c",650, 600)
    c.SetLogy()
    
    c.SetGridx()
    c.SetGridy()

    c.SetRightMargin(0.05)
    c.SetLeftMargin(0.15)
    c.SetTopMargin(0.10)
    c.SetBottomMargin(0.11)
    #dummy = TH1D("","", 1, 1.400,2.600)
    dummy = TH1D("","", 1, 1400,2600)
    dummy.SetBinContent(10,0.0)
    dummy.GetXaxis().SetTitle("m_{Z'} in TeV")   
    dummy.GetXaxis().SetTitleSize(0.05)   
    dummy.GetXaxis().SetLabelSize(0.05)   
    
    
    dummy.GetYaxis().SetTitle("#sigma (pp #rightarrow Z' #rightarrow tT) #times BR in pb")   
    dummy.GetYaxis().SetTitleSize(0.05)   
    dummy.GetYaxis().SetLabelSize(0.05)   
    dummy.GetYaxis().SetTitleOffset(1.3)   
    #dummy.GetYaxis().SetLogy()   
    
    dummy.SetLineColor(0)
    dummy.SetLineWidth(0)
    dummy.SetFillColor(0)
    #dummy.SetMinimum(0.01)
    #dummy.SetMaximum(10.0)
    dummy.GetYaxis().SetRangeUser(0.009,30)   
    
    dummy.Draw()
    
    gr_exp2 = TGraphAsymmErrors(v_mass,v_exp,v_zeros,v_zeros,v_exp_m2,v_exp_p2)
    gr_exp2.SetLineColor(kOrange)
    gr_exp2.SetFillColor(kOrange)
    gr_exp2.Draw("e3same")
    
    gr_exp1 = TGraphAsymmErrors(v_mass,v_exp,v_zeros,v_zeros,v_exp_m1,v_exp_p1)
    gr_exp1.SetLineColor(kGreen+1)
    gr_exp1.SetFillColor(kGreen+1)
    gr_exp1.Draw("e3same")
    
    gr_exp = TGraphAsymmErrors(v_mass,v_exp,v_zeros,v_zeros,v_zeros,v_zeros)
    gr_exp.SetLineColor(1)
    gr_exp.SetLineWidth(2)
    gr_exp.SetLineStyle(2)
    gr_exp.Draw("Lsame")
    
    gr_obs = TGraphAsymmErrors(v_mass,v_obs,v_zeros,v_zeros,v_zeros,v_zeros)
    gr_obs.SetLineColor(1)
    gr_obs.SetLineWidth(2)
    #gr_obs.SetLineStyle(2)
    gr_obs.Draw("Lsame")
        
    
    if (decaymode is "BR05_025_025Nar") or (decaymode is "BR05_025_025Wid"):
        #gr_theory = TGraphAsymmErrors(v_theory_masses,v_theory,v_zeros,v_zeros,v_zeros,v_zeros)
        gr_theory = TGraph(v_theory_masses,v_theory)
        gr_theory.SetLineColor(kRed+1)
        gr_theory.SetLineWidth(2)
        gr_theory.SetLineStyle(9)
        gr_theory.Draw("CPsame")
    
        #gr_theory2 = TGraphAsymmErrors(v_theory_masses2,v_theory2,v_zeros,v_zeros,v_zeros,v_zeros)
        gr_theory2 = TGraph(v_theory_masses2,v_theory2)
        gr_theory2.SetLineColor(kRed+1)
        gr_theory2.SetLineWidth(2)
        gr_theory2.SetLineStyle(6)
    
        #gr_theory2.Draw("CPsame")
    
    
    #gr_em = TGraphAsymmErrors(v_mass,v_em_obs,v_zeros,v_zeros,v_zeros,v_zeros)
    #gr_em.SetLineColor(1)
    #gr_em.SetLineWidth(2)
    #gr_em.Draw("Lsame")

    #gr_em_exp = TGraphAsymmErrors(v_mass,v_em_exp,v_zeros,v_zeros,v_zeros,v_zeros)
    #gr_em_exp.SetLineStyle(1)
    #gr_em_exp.SetLineColor(1)
    #gr_em_exp.SetLineWidth(2)
    #gr_em_exp.Draw("Lsame")
    #gr_obs = TGraphAsymmErrors(v_theory_masses,v_theory,v_zeros,v_zeros,v_zeros,v_zeros)
    #gr_obs.SetLineColor(1)
    #gr_obs.SetLineWidth(2)
    #gr_obs.Draw("CPsame")
    

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
    
    
    #legend = TLegend(.35,.60,.98,.92)
    legend = TLegend(.45,.60,.98,.92)
    #legend.SetHeader("                    m_{T} = 1.3 TeV   ")
    #legend.SetTextSize(0.036)
    legend.SetTextSize(0.03)
    if decaymode is "BR05_025_025Nar":
        legend.SetHeader("#Gamma_{Z'}/m_{Z'}=1%, m_{T}=1.3 TeV, BR(T #rightarrow Wb/Ht/Zt)=50%/25%/25%")
    elif decaymode is "tWbNar":
        legend.SetHeader("#Gamma_{Z'}/m_{Z'}=1%, m_{T}=1.3 TeV, BR(T #rightarrow Wb/Ht/Zt)=100%/0%/0%")
    elif decaymode is "ttZNar":
        legend.SetHeader("#Gamma_{Z'}/m_{Z'}=1%, m_{T}=1.3 TeV, BR(T #rightarrow Wb/Ht/Zt)=0%/0%/100%")
    elif decaymode is "ttHNar":
        legend.SetHeader("#Gamma_{Z'}/m_{Z'}=1%, m_{T}=1.3 TeV, BR(T #rightarrow Wb/Ht/Zt)=0%/100%/0%")
    if decaymode is "BR05_025_025Wid":
        legend.SetHeader("m_{T}=1.3 TeV, BR(T #rightarrow Wb/Ht/Zt)=50%/25%/25%")
    elif decaymode is "tWbWid":
        legend.SetHeader("#Gamma_{Z'}/m_{Z'}=30%, m_{T}=1.3 TeV, BR(T #rightarrow Wb/Ht/Zt)=100%/0%/0%")
    elif decaymode is "ttZWid":
        legend.SetHeader("#Gamma_{Z'}/m_{Z'}=30%, m_{T}=1.3 TeV, BR(T #rightarrow Wb/Ht/Zt)=0%/0%/100%")
    elif decaymode is "ttHWid":
        legend.SetHeader("#Gamma_{Z'}/m_{Z'}=30%, m_{T}=1.3 TeV, BR(T #rightarrow Wb/Ht/Zt)=0%/100%/0%")
    else:
        print "hihi"
   
    #legend.AddEntry("BR(T'#rightarrow Wb,Ht,Zt)=100%,0%,0%, y=c_{2}=c_{3}=1, g_{#rho}=3", "l")
    if (decaymode is "BR05_025_025Nar") or (decaymode is "BR05_025_025Wid"):
        legend.AddEntry(gr_theory , "G^{*} #rightarrow tT, tan #theta=0.44, sin #Phi_{tR}=0.6, Y_{*}=3","L")
        #legend.AddEntry(gr_theory , "Theorievorhersage","L")
        #legend.AddEntry(gr_theory2 , "#rho_{L}^{0} #rightarrow tT, y_{L}=c_{2}=c_{3}=1,g_{#rho_{L}}=3","L")
    #legend.AddEntry(gr_em , "Observed Limit B2G-16-013","L")
    #legend.AddEntry(gr_em_exp , "Expected Limit B2G-16-013","L")
    
    
    legend.AddEntry(gr_obs , "Observed Limit 95% CL", "l")
    legend.AddEntry(gr_exp , "Expected Limit 95% CL", "l")    
    #legend.AddEntry(gr_obs , "Beobachtet 95% CL", "l")
    #legend.AddEntry(gr_exp , "Erwartet 95% CL", "l")
    legend.AddEntry(gr_exp1 , "#pm 1#sigma", "f")
    legend.AddEntry(gr_exp2 , "#pm 2#sigma", "f")
    legend.SetShadowColor(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)            
    legend.Draw("same")
                                                            
    gPad.RedrawAxis()

    c.SaveAs("limit_Gstar1300_"+decaymode+".pdf")



#for files,decaymode in zip([filestWb,filesttZ,filesttH,filesBR],["tWb","ttZ","ttH","BR"]):
#for files,decaymode in zip([filestWbNar],["tWbNar"]):
#for files,decaymode in zip([filesttZNar],["ttZNar"]):
#for files,decaymode in zip([filesttHNar],["ttHNar"]):
for files,decaymode in zip([filesBRNar],["BR05_025_025Nar"]):
    
#for files,decaymode in zip([filestWbWid],["tWbWid"]):
#for files,decaymode in zip([filesttZWid],["ttZWid"]):
#for files,decaymode in zip([filesttHWid],["ttHWid"]):
#for files,decaymode in zip([filesBRWid],["BR05_025_025Wid"]):
    drawlimits(files,decaymode)