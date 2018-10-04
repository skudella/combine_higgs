from ROOT import *
#from tdrStyle import *
#setTDRStyle()
        
import os,sys,glob
from array import array

gStyle.SetOptStat(0)

unsortedmass = []

mass = array('d',[])
zeros = array('d',[])
exp_p2 = array('d',[])
exp_p1 = array('d',[])
exp = array('d',[])
exp_m1 = array('d',[])
exp_m2 = array('d',[])
obs = array('d',[])


files=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/plotutils_workspaces/Sig*1200*ABCD3_plotutils/higgs*.root")

print files

for afile in files:
    print afile
    for zm in [1500,1750,2000,2250,2500,2750,3000,3500,4000]:
        if str(zm) in afile:
            unsortedmass.append(zm)
unsortedmass.sort()

for m in unsortedmass:
    
    emanueles_limit=1
    print m
    if m is 1500:
        emanueles_limit=8.6
    if m is 2000:
        emanueles_limit=0.29
    if m is 2500:
        emanueles_limit=0.3
        
    mass.append(m)

    f = TFile("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/plotutils_workspaces/SigZprime"+str(m)+"1200_ABCD3plotutils/higgsCombine_Asymptotic.Asymptotic.mH120.root","READ")
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


x_theory= array('d', [1500,1600,1700,1800,1900,2000,2050,2100,2200,2300,2400,2450,2500])
theory =  array('d', [1.4,1.87,1.57,1.28,1.01,0.38,0.34,0.258,0.18,0.132,0.106,0.042,0.021]) # Gstar
x_theory2= array('d', [1500,1550,1600,1650,1700,1750,1800,1850,1900,1950,2000,2050,2100,2150,2200,2250,2300,2350,2400,2450,2500])
theory2  = array('d', [0.1096, 0.0941941, 0.0812049, 0.0702895,  0.0610887, 0.0531233, 0.0462985, 0.040349, 0.035255, 0.0309674, 0.0272837, 0.0239634, 0.0210468, 0.018506,0.0162989, 0.0143873, 0.0127257,0.0112562, 0.00997291,0.00885648, 0.00788735]) # Gstar



v_mass = TVectorD(len(mass),mass)
v_zeros = TVectorD(len(zeros),zeros)
v_exp_p2 = TVectorD(len(exp_p2),exp_p2)
v_exp_p1 = TVectorD(len(exp_p1),exp_p1)
v_exp = TVectorD(len(exp),exp)
v_exp_m1 = TVectorD(len(exp_m1),exp_m1)
v_exp_m2 = TVectorD(len(exp_m2),exp_m2)
v_theory = TVectorD(len(theory),theory)
v_theory_masses = TVectorD(len(x_theory),x_theory)
v_theory2 = TVectorD(len(theory2),theory2)
v_theory_masses2 = TVectorD(len(x_theory2),x_theory2)


c = TCanvas("c","c",800, 600)
c.SetLogy()

c.SetGridx()
c.SetGridy()

c.SetRightMargin(0.06)
c.SetLeftMargin(0.2)

dummy = TH1D("","", 1, 1400,2600)
dummy.SetBinContent(10,0.0)
dummy.GetXaxis().SetTitle("m(Z') in GeV")   
dummy.GetYaxis().SetTitle("#sigma (pp #rightarrow Z' #rightarrow tT') #times BR [pb]")   
#dummy.GetYaxis().SetLogy()   

dummy.SetLineColor(0)
dummy.SetLineWidth(0)
dummy.SetFillColor(0)
#dummy.SetMinimum(0.01)
#dummy.SetMaximum(10.0)
dummy.GetYaxis().SetRangeUser(0.01,10)   

dummy.Draw()

gr_exp2 = TGraphAsymmErrors(v_mass,v_exp,v_zeros,v_zeros,v_exp_m2,v_exp_p2)
gr_exp2.SetLineColor(kYellow)
gr_exp2.SetFillColor(kYellow)
gr_exp2.Draw("e3same")

gr_exp1 = TGraphAsymmErrors(v_mass,v_exp,v_zeros,v_zeros,v_exp_m1,v_exp_p1)
gr_exp1.SetLineColor(kGreen)
gr_exp1.SetFillColor(kGreen)
gr_exp1.Draw("e3same")

gr_exp = TGraphAsymmErrors(v_mass,v_exp,v_zeros,v_zeros,v_zeros,v_zeros)
gr_exp.SetLineColor(1)
gr_exp.SetLineWidth(2)
gr_exp.SetLineStyle(2)
gr_exp.Draw("Lsame")

gr_theory = TGraphAsymmErrors(v_theory_masses,v_theory,v_zeros,v_zeros,v_zeros,v_zeros)
gr_theory.SetLineColor(1)
gr_theory.SetLineWidth(2)
gr_theory.Draw("CPsame")

gr_theory2 = TGraphAsymmErrors(v_theory_masses2,v_theory2,v_zeros,v_zeros,v_zeros,v_zeros)
gr_theory2.SetLineColor(1)
gr_theory2.SetLineWidth(2)
gr_theory2.SetLineStyle(6)

gr_theory2.Draw("CPsame")
#gr_obs = TGraphAsymmErrors(v_theory_masses,v_theory,v_zeros,v_zeros,v_zeros,v_zeros)
#gr_obs.SetLineColor(1)
#gr_obs.SetLineWidth(2)
#gr_obs.Draw("CPsame")

latex2 = TLatex()
latex2.SetNDC()
latex2.SetTextSize(0.5*c.GetTopMargin())
latex2.SetTextFont(42)
latex2.SetTextAlign(35) # align right
latex2.DrawLatex(0.95, 0.95,"35.9 fb^{-1} (13 TeV)")
latex2.SetTextSize(0.5*c.GetTopMargin())
latex2.SetTextFont(20)
latex2.SetTextAlign(11) # align right
latex2.DrawLatex(0.10, 0.95, "CMS")
latex2.SetTextSize(0.5*c.GetTopMargin())
latex2.SetTextFont(20)
latex2.SetTextAlign(11)
latex2.DrawLatex(0.23, 0.95, "private work")

legend = TLegend(.55,.60,.95,.90)
#legend.SetHeader("                    M_{T'} = 1.2 TeV   ")
legend.SetHeader("M_{T'} = 1.2 TeV, BR(T' #rightarrow Wb,Ht,Zt)=100%,0%,0%")
#legend.AddEntry("BR(T'#rightarrow Wb,Ht,Zt)=100%,0%,0%, y=c_{2}=c_{3}=1, g_{#rho}=3", "l")
legend.AddEntry(gr_theory , "G^{*} #rightarrow tT', tan #theta=0.44, sin #Phi_{tR}=0.6, Y_{*}=3","L")
legend.AddEntry(gr_theory2 , "#rho_{L}^{0} #rightarrow tT', y_{L}=c_{2}=c_{3}=1,g_{#rho_{L}}=3","L")
legend.AddEntry(gr_exp , "Expected 95% CL", "l")
legend.AddEntry(gr_exp1 , "#pm 1#sigma", "f")
legend.AddEntry(gr_exp2 , "#pm 2#sigma", "f")
legend.SetShadowColor(0)
legend.SetFillColor(0)
legend.SetLineColor(0)            
legend.Draw("same")
                                                            
gPad.RedrawAxis()

c.SaveAs("limit.pdf")

