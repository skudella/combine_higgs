from ROOT import *
#from tdrStyle import *
#setTDRStyle()
        
import os,sys,glob
from array import array

gStyle.SetOptStat(0)

unsortedmass = []

mass = array('d',[])
zeros = array('d',[])

exp_tWb = array('d',[])
exp_ttZ = array('d',[])
exp_ttH = array('d',[])



#files=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/plotutils_workspaces/Sig*1200*ABCD3_plotutils/higgs*.root")
filestWb=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/Sig*1200*tWb*ABCD5_CMS_WP/Asymptotic/higgs*.root")
filesttZ=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/Sig*1200*ttZ*ABCD5_CMS_WP/Asymptotic/higgs*.root")
filesttH=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/Sig*1200*ttH*ABCD5_CMS_WP/Asymptotic/higgs*.root")
filesBR=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/Sig*1200*BR*ABCD5_CMS_WP/Asymptotic/higgs*.root")


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


        #f = TFile("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigZprime"+str(m)+"1200_tWb_ABCD5_CMS_WP/Asymptotic/higgsCombine_Asymptotic.Asymptotic.mH120.root","READ")
        #f_ttZ = TFile("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigZprime"+str(m)+"1200_ttZ_ABCD5_CMS_WP/Asymptotic/higgsCombine_Asymptotic.Asymptotic.mH120.root","READ")
        #f_ttH = TFile("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigZprime"+str(m)+"1200_ttH_ABCD5_CMS_WP/Asymptotic/higgsCombine_Asymptotic.Asymptotic.mH120.root","READ")

        #filename=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/plotutils_workspaces/SigZprime"+str(m)+"1200*"+decaymode+"*ABCD5_CMS_WP/higgsCombine_Asymptotic.Asymptotic.mH120.root")
        #print decaymode,"  ", filename
        #f = TFile(filename[0],"READ")
        
        #t = f.Get("limit")
        #t.Print()
        zeros.append(0.0)
        
        #t_tWb.GetEntry(2)
        #thisexp_tWb = t_tWb.limit
        #exp_tWb.append((thisexp_tWb)*emanueles_limit)
        

    
    x_theory= array('d', [1500.0,1600.0,1700.0,1800.0,1900.0,2000.0,2050.0,2100.0,2200.0,2300.0,2400.0,2450.0,2500.0])
    theory =  array('d', [1.4,1.87,1.57,1.28,1.01,0.38,0.34,0.258,0.18,0.132,0.106,0.042,0.021]) # Gstar
    x_theory2= array('d', [1500,1550,1600,1650,1700,1750,1800,1850,1900,1950,2000,2050,2100,2150,2200,2250,2300,2350,2400,2450,2500])
    theory2  = array('d', [0.1096, 0.0941941, 0.0812049, 0.0702895,  0.0610887, 0.0531233, 0.0462985, 0.040349, 0.035255, 0.0309674, 0.0272837, 0.0239634, 0.0210468, 0.018506,0.0162989, 0.0143873, 0.0127257,0.0112562, 0.00997291,0.00885648,    0.00788735]) # Gstar
    
    #em_p2  = array('d', []) # Gstar
    #em_p1  = array('d', []) # Gstar
    #em  = array('d', []) # Gstar
    #em_m1  = array('d', []) # Gstar
    #em_m2  = array('d', []) # Gstar

    
    twb  = array('d', [3.7,0.098,0.061])
    ttZ  = array('d', [0.74,0.128,0.083])
    ttH  = array('d', [2.2,0.38,0.21])

    anna_twb  = array('d', [0.64,0.226,0.13])
    anna_ttZ  = array('d', [0.166,0.0541,0.031])
    anna_ttH  = array('d', [0.0863,0.0345,0.0222])    
    
    v_mass = TVectorD(len(mass),mass)
    v_zeros = TVectorD(len(zeros),zeros)
    
    #v_exp = TVectorD(len(exp),exp)

    v_anna_exp_btW =TVectorD(len(anna_twb),anna_twb)
    v_anna_exp_ttZ =TVectorD(len(anna_ttZ),anna_ttZ)
    v_anna_exp_ttH =TVectorD(len(anna_ttH),anna_ttH)

    v_twb =TVectorD(len(twb),twb)
    v_ttZ =TVectorD(len(ttZ),ttZ)
    v_ttH =TVectorD(len(ttH),ttH)
    


    
    
    c = TCanvas("c","c",800, 600)
    c.SetLogy()
    
    c.SetGridx()
    c.SetGridy()
    
    c.SetRightMargin(0.06)
    c.SetLeftMargin(0.2)
    
    dummy = TH1D("","", 1, 1400,2600)
    dummy.SetBinContent(10,0.0)
    dummy.GetXaxis().SetTitle("m(Z') in GeV")   
    dummy.GetXaxis().SetTitleSize(0.05)   
    dummy.GetYaxis().SetTitle("#sigma (pp #rightarrow Z' #rightarrow tT) #times BR [pb]")   
    dummy.GetYaxis().SetTitleSize(0.05)   
    
    #dummy.GetYaxis().SetLogy()   
    
    dummy.SetLineColor(kRed+2)
    dummy.SetLineWidth(0)
    dummy.SetFillColor(0)
    #dummy.SetMinimum(0.01)
    #dummy.SetMaximum(10.0)
    dummy.GetYaxis().SetRangeUser(0.01,20)   
    
    dummy.Draw()

    
    gr_exp_twb = TGraphAsymmErrors(v_mass,v_twb,v_zeros,v_zeros,v_zeros,v_zeros)
    gr_exp_twb.SetLineColor(kRed+2)
    gr_exp_twb.SetLineWidth(2)
    #gr_exp_twb.SetLineStyle(2)
    gr_exp_twb.Draw("Lsame")

    gr_exp_ttZ = TGraphAsymmErrors(v_mass,v_ttZ,v_zeros,v_zeros,v_zeros,v_zeros)
    gr_exp_ttZ.SetLineColor(kBlue+2)
    gr_exp_ttZ.SetLineWidth(2)
    #gr_exp_ttZ.SetLineStyle(2)
    gr_exp_ttZ.Draw("Lsame")
    
    gr_exp_ttH = TGraphAsymmErrors(v_mass,v_ttH,v_zeros,v_zeros,v_zeros,v_zeros)
    gr_exp_ttH.SetLineColor(kGreen+2)
    gr_exp_ttH.SetLineWidth(2)
    #gr_exp_ttH.SetLineStyle(2)
    gr_exp_ttH.Draw("Lsame")
    
    gr_v_anna_exp_btW = TGraphAsymmErrors(v_mass,v_anna_exp_btW,v_zeros,v_zeros,v_zeros,v_zeros)
    gr_v_anna_exp_btW.SetLineColor(kRed-7)
    gr_v_anna_exp_btW.SetLineWidth(2)
    #gr_v_anna_exp_btW.SetLineStyle(2)
    gr_v_anna_exp_btW.Draw("Lsame")
    
    gr_v_anna_exp_ttZ = TGraphAsymmErrors(v_mass,v_anna_exp_ttZ,v_zeros,v_zeros,v_zeros,v_zeros)
    gr_v_anna_exp_ttZ.SetLineColor(kBlue-7)
    gr_v_anna_exp_ttZ.SetLineWidth(2)
    #gr_v_anna_exp_ttZ.SetLineStyle(2)
    gr_v_anna_exp_ttZ.Draw("Lsame")
    
    gr_v_anna_exp_ttH = TGraphAsymmErrors(v_mass,v_anna_exp_ttH,v_zeros,v_zeros,v_zeros,v_zeros)
    gr_v_anna_exp_ttH.SetLineColor(kGreen-7)
    gr_v_anna_exp_ttH.SetLineWidth(2)
    #gr_v_anna_exp_ttH.SetLineStyle(2)
    gr_v_anna_exp_ttH.Draw("Lsame")

    
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
    legend.SetTextSize(0.03)

        
    #legend.AddEntry("BR(T'#rightarrow Wb,Ht,Zt)=100%,0%,0%, y=c_{2}=c_{3}=1, g_{#rho}=3", "l")
    #if decaymode is "BR":
        #legend.AddEntry(gr_theory , "G^{*} #rightarrow tT', tan #theta=0.44, sin #Phi_{tR}=0.6, Y_{*}=3","L")
        #legend.AddEntry(gr_theory2 , "#rho_{L}^{0} #rightarrow tT', y_{L}=c_{2}=c_{3}=1,g_{#rho_{L}}=3","L")
    #legend.AddEntry(gr_em , "Observed Limit B2G-16-013","L")
    #legend.AddEntry(gr_em_exp , "Expected Limit B2G-16-013","L")
    legend.AddEntry(gr_exp_twb , "bW vollhadronisch (95% limit)", "l")
    legend.AddEntry(gr_exp_ttZ , "tZ vollhadronisch (95% limit)", "l")
    legend.AddEntry(gr_exp_ttH , "tH vollhadronisch (95% limit)", "l")
    legend.AddEntry(gr_v_anna_exp_btW , "bW semileptonisch (95% limit)", "l")
    legend.AddEntry(gr_v_anna_exp_ttZ , "tZ semileptonisch (95% limit)", "l")
    legend.AddEntry(gr_v_anna_exp_ttH , "tH semileptonisch (95% limit)", "l")
    legend.SetShadowColor(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)            
    legend.Draw("same")
                                                            
    gPad.RedrawAxis()

    c.SaveAs("limit_comp.pdf")



#for files,decaymode in zip([filestWb,filesttZ,filesttH,filesBR],["tWb","ttZ","ttH","BR"]):
for files,decaymode in zip([filestWb],["tWb"]):
#for files,decaymode in zip([filesttZ],["ttZ"]):
#for files,decaymode in zip([filesttH],["ttH"]):
#for files,decaymode in zip([filesBR],["BR"]):
    drawlimits(files,decaymode)