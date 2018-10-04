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
filestWb=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*1200*tWb*ABCD5/Asymptotic/higgs*.root")
filesttZ=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*1200*ttZ*ABCD5/Asymptotic/higgs*.root")
filesttH=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*1200*ttH*ABCD5/Asymptotic/higgs*.root")
filesBR=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*1200*BR*ABCD5/Asymptotic/higgs*.root")


def drawlimits(files,decaymode):
     
    
    unsortedmass=[]
    for afile in files:
        print afile
        for zm in [1500,1750,2000,2250,2500,2750,3000,3500,4000]:
            if str(zm) in afile:
                print zm, " in ", afile
                unsortedmass.append(zm)
    unsortedmass.sort()
    print unsortedmass
    for m in unsortedmass:
        
        emanueles_limit=1
        print m
        #if m is 1500:
            #emanueles_limit=8.6
            #emanueles_limit=8.6
        #if m is 2000:
            #emanueles_limit=0.29
            #emanueles_limit=0.29
        #if m is 2500:
            #emanueles_limit=0.3
            #emanueles_limit=0.3
            
        mass.append(m)

        if decaymode is "BR":
            f = TFile("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho"+str(m)+"1200_BR00_50_50_ABCD5/Asymptotic/higgsCombine_Asymptotic.Asymptotic.mH120.root","READ")
        elif decaymode is "tWb":
            f = TFile("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho"+str(m)+"1200_tWb_ABCD5/Asymptotic/higgsCombine_Asymptotic.Asymptotic.mH120.root","READ")
        elif decaymode is "ttZ":
            f = TFile("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho"+str(m)+"1200_ttZ_ABCD5/Asymptotic/higgsCombine_Asymptotic.Asymptotic.mH120.root","READ")
        elif decaymode is "ttH":
            f = TFile("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho"+str(m)+"1200_ttH_ABCD5/Asymptotic/higgsCombine_Asymptotic.Asymptotic.mH120.root","READ")
        else:
            print "hihi"

        #filename=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/plotutils_workspaces/SigRho"+str(m)+"1200*"+decaymode+"*ABCD5_CMS_WP/higgsCombine_Asymptotic.Asymptotic.mH120.root")
        #print decaymode,"  ", filename
        #f = TFile(filename[0],"READ")
        t = f.Get("limit")
        print t
        print m
        #t.Print()
        zeros.append(0.0)
        
        t.GetEntry(2)
        thisexp = t.limit
        exp.append((thisexp)*emanueles_limit)
        print "expected ", (thisexp)*emanueles_limit
        
        t.GetEntry(0)
        exp_m2.append((thisexp-t.limit)*emanueles_limit)
        print "m2sigma", (t.limit)
        t.GetEntry(1)
        exp_m1.append((thisexp-t.limit)*emanueles_limit)
        print  "m1sigma",(t.limit)
        t.GetEntry(3)
        exp_p1.append((t.limit-thisexp)*emanueles_limit)
        print "p1sigma",(t.limit)
        t.GetEntry(4)
        exp_p2.append((t.limit-thisexp)*emanueles_limit)
        print "p2sigma",(t.limit)
        t.GetEntry(5)
        obs.append((t.limit))
        print "obs",(t.limit)
    
    x_theory= array('d', [1500.0,1600.0,1700.0,1800.0,1900.0,2000.0,2050.0,2100.0,2200.0,2300.0,2400.0,2450.0,2500.0])
    theory =  array('d', [1.4,1.87,1.57,1.28,1.01,0.38,0.34,0.258,0.18,0.132,0.106,0.042,0.021]) # Gstar
    x_theory2= array('d', [1500,1550,1600,1650,1700,1750,1800,1850,1900,1950,2000,2050,2100,2150,2200,2250,2300,2350,2400,2450,2500])
    theory2  = array('d', [0.1096, 0.0941941, 0.0812049, 0.0702895,  0.0610887, 0.0531233, 0.0462985, 0.040349, 0.035255, 0.0309674, 0.0272837, 0.0239634, 0.0210468, 0.018506,0.0162989, 0.0143873, 0.0127257,0.0112562, 0.00997291,0.00885648,    0.00788735]) # Gstar
    
    #em_p2  = array('d', []) # Gstar
    #em_p1  = array('d', []) # Gstar
    #em  = array('d', []) # Gstar
    #em_m1  = array('d', []) # Gstar
    #em_m2  = array('d', []) # Gstar
    if decaymode is "BR":
        em_obs  = array('d', [8.6,0.27,0.33]) # Gstar
    if decaymode is "tWb":
        em_obs  = array('d', [8.6,0.4,0.3]) # Gstar
    if decaymode is "ttZ":
        em_obs  = array('d', [3.1,0.29,0.18]) # Gstar
    if decaymode is "ttH":
        em_obs  = array('d', [11.0,0.54,0.26]) # Gstar
    if decaymode is "BR":
        em_exp  = array('d', [8.0,0.45,0.2]) # Gstar
    if decaymode is "tWb":
        em_exp  = array('d', [7.7,0.48,0.23]) # Gstar
    if decaymode is "ttZ":
        em_exp  = array('d', [3.1,0.29,0.18]) # Gstar
    if decaymode is "ttH":
        em_exp  = array('d', [2.6,0.48,0.29]) # Gstar
            
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
    v_em_obs = TVectorD(len(em_obs),em_obs)
    v_em_exp = TVectorD(len(em_exp),em_exp)
    
    
    
    v_theory = TVectorD(len(theory),theory)
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
    dummy = TH1D("","", 1, 1400,2600)
    dummy.SetBinContent(10,0.0)
    dummy.GetXaxis().SetTitle("m_{Z'} in GeV")   
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
    
    #dummy.GetYaxis().SetLogy()   
      
    
    dummy.Draw()
    
    gr_exp2 = TGraphAsymmErrors(v_mass,v_exp,v_zeros,v_zeros,v_exp_m2,v_exp_p2)
    gr_exp2.SetLineColor(kOrange)
    gr_exp2.SetFillColor(kOrange)
    #gr_obs.SetLineStyle(2)
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
    
    if decaymode is "BR":
        #gr_theory = TGraphAsymmErrors(v_theory_masses,v_theory,v_zeros,v_zeros,v_zeros,v_zeros)
        gr_theory = TGraph(v_theory_masses,v_theory)
        gr_theory.SetLineColor(kBlue+1)
        gr_theory.SetLineWidth(2)
        gr_theory.SetLineStyle(9)
        #gr_theory.Draw("CPsame")
    
        #gr_theory2 = TGraphAsymmErrors(v_theory_masses2,v_theory2,v_zeros,v_zeros,v_zeros,v_zeros)
        gr_theory2 = TGraph(v_theory_masses2,v_theory2)
        gr_theory2.SetLineColor(kBlue+1)
        gr_theory2.SetLineWidth(2)
        gr_theory2.SetLineStyle(6)
    
        gr_theory2.Draw("CPsame")
    
    
    gr_em = TGraphAsymmErrors(v_mass,v_em_obs,v_zeros,v_zeros,v_zeros,v_zeros)
    gr_em.SetLineColor(1)
    gr_em.SetLineWidth(2)
    #gr_em.Draw("Lsame")

    gr_em_exp = TGraphAsymmErrors(v_mass,v_em_exp,v_zeros,v_zeros,v_zeros,v_zeros)
    gr_em_exp.SetLineStyle(1)
    gr_em_exp.SetLineColor(1)
    gr_em_exp.SetLineWidth(2)
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
    
    legend = TLegend(.45,.60,.98,.92)
    #legend.SetHeader("                    m_{T}=1.2TeV   ")
    legend.SetTextSize(0.03)
    if decaymode is "BR":
        legend.SetHeader("m_{T}=1.2TeV, BR(T #rightarrow Wb/Zt/Ht)=0%/50%/50%")
    elif decaymode is "tWb":
        legend.SetHeader("m_{T}=1.2TeV, BR(T #rightarrow Wb/Zt/Ht)=100%,0%,0%")
    elif decaymode is "ttZ":
        legend.SetHeader("m_{T}=1.2TeV, BR(T #rightarrow Wb/Zt/Ht)=0%,0%,100%")
    elif decaymode is "ttH":
        legend.SetHeader("m_{T}=1.2TeV, BR(T #rightarrow Wb/Zt/Ht)=0%,100%,0%")
    else:
        print "hihi"
        
    #legend.AddEntry("BR(T'#rightarrow Wb,Ht,Zt)=100%,0%,0%, y=c_{2}=c_{3}=1, g_{#rho}=3", "l")
    if decaymode is "BR":
        #legend.AddEntry(gr_theory , "G^{*} #rightarrow tT', tan #theta=0.44, sin #Phi_{tR}=0.6, Y_{*}=3","L")
        legend.AddEntry(gr_theory2 , "#rho_{L}^{0} #rightarrow tT', y_{L}=c_{2}=c_{3}=1,g_{#rho_{L}}=3","L")
    #legend.AddEntry(gr_em , "Observed Limit B2G-16-013","L")
    #legend.AddEntry(gr_em_exp , "Expected Limit B2G-16-013","L")
    legend.AddEntry(gr_obs , "Observed 95% CL", "l")
    legend.AddEntry(gr_exp , "Expected 95% CL", "l")
    legend.AddEntry(gr_exp1 , "#pm 1#sigma", "f")
    legend.AddEntry(gr_exp2 , "#pm 2#sigma", "f")
    legend.SetShadowColor(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)            
    legend.Draw("same")
                                                            
    gPad.RedrawAxis()

    c.SaveAs("limit_rho"+decaymode+".pdf")



#for files,decaymode in zip([filestWb,filesttZ,filesttH,filesBR],["tWb","ttZ","ttH","BR"]):
#for files,decaymode in zip([filestWb],["tWb"]):
#for files,decaymode in zip([filesttZ],["ttZ"]):
#for files,decaymode in zip([filesttH],["ttH"]):
for files,decaymode in zip([filesBR],["BR"]):
    drawlimits(files,decaymode)