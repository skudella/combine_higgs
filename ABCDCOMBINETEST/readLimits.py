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
#filestWb_Rho=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*tWb*ABCD5_CMS_WP/Asymptotic/higgs*.root")
#filesttZ_Rho=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*ttZ*ABCD5_CMS_WP/Asymptotic/higgs*.root")
#filesttH_Rho=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*ttH*ABCD5_CMS_WP/Asymptotic/higgs*.root")Figure~\ref{fig_limits-rho}
#filesBR_Rho=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*BR*ABCD5_CMS_WP/Asymptotic/higgs*.root")

#filestWb_Gstar=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*tWb*ABCD5_CMS_WP/Asymptotic/higgs*.root")
#filesttZ_Gstar=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*ttZ*ABCD5_CMS_WP/Asymptotic/higgs*.root")
#filesttH_Gstar=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*ttH*ABCD5_CMS_WP/Asymptotic/higgs*.root")
#filesBR_Gstar=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*BR*ABCD5_CMS_WP/Asymptotic/higgs*.root")


#filestWb_Rho=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*tWb*ABCD5/Asymptotic/higgs*.root")
#filesttZ_Rho=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*ttZ*ABCD5/Asymptotic/higgs*.root")
#filesttH_Rho=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*ttH*ABCD5/Asymptotic/higgs*.root")
#filesBR_Rho=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*BR*ABCD5/Asymptotic/higgs*.root")

#filestWb_GstarNar=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*tWbNar*ABCD5/Asymptotic/higgs*.root")
#filesttZ_GstarNar=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*ttZNar*ABCD5/Asymptotic/higgs*.root")
#filesttH_GstarNar=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*ttHNar*ABCD5/Asymptotic/higgs*.root")
#filesBR_GstarNar=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*BR05_025_025Nar*ABCD5/Asymptotic/higgs*.root")

#filestWb_GstarWid=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*tWbWid*ABCD5/Asymptotic/higgs*.root")
#filesttZ_GstarWid=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*ttZWid*ABCD5/Asymptotic/higgs*.root")
#filesttH_GstarWid=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*ttHWid*ABCD5/Asymptotic/higgs*.root")
#filesBR_GstarWid=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*BR05_025_025Wid*ABCD5/Asymptotic/higgs*.root")


#files=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*tWb*ABCD5/Asymptotic/higgs*.root")
filestWb=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*tWbNar*ABCD5/Asymptotic/higgs*.root")
filestWb.sort()

filesttZ=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*ttZNar*ABCD5/Asymptotic/higgs*.root")
filesttZ.sort()

filesttH=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*ttHNar*ABCD5/Asymptotic/higgs*.root")
filesttH.sort()

filestWbWid=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*tWbWid*ABCD5/Asymptotic/higgs*.root")
filestWbWid.sort()

filesttZWid=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*ttZWid*ABCD5/Asymptotic/higgs*.root")
filesttZWid.sort()

filesttHWid=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigGstar*ttHWid*ABCD5/Asymptotic/higgs*.root")
filesttHWid.sort()


#files=filestWb


#files=filestWb+filesttH+filestWbWid+filesttZWid+filesttHWid
files=filestWb+filesttZ+filesttH+filestWbWid+filesttZWid+filesttHWid


#filestWb=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*tWb*ABCD5/Asymptotic/higgs*.root")
#filestWb.sort()

#filesttZ=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*ttZ*ABCD5/Asymptotic/higgs*.root")
#filesttZ.sort()

#filesttH=glob.glob("/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/ABCDCOMBINETEST/combine_workspaces/SigRho*ttH*ABCD5/Asymptotic/higgs*.root")
#filesttH.sort()

#files=filestWb+filesttZ+filesttH


#def drawlimits(files):
text="""mZ' & width &mT$decaymode& obs & -2s & -1s & median & +1s & +2s \\\\
"""
for filename in files:
        if "SigGstar40003000_ttZNar" in filename:
            continue
        if "SigZprime" in filename:
            continue
        if "BR" in filename:
            continue
        if(os.path.isfile(filename)): 
            
            f = TFile(filename,"READ")
        
        
            t = f.Get("limit")
            print "filename ",filename
            print t
            t.Print()
        
            t.GetEntry(2)
            thisexp = t.limit
        
            t.GetEntry(0)
            thisexp_m2=t.limit
    
            t.GetEntry(1)
            thisexp_m1=t.limit
    
            t.GetEntry(3)
            thisexp_p1=t.limit
    
            t.GetEntry(4)
            thisexp_p2=t.limit
    
            t.GetEntry(5)
            obs=t.limit
            
            mZ="Test"
            mT="Test"
            if "Wid" in filename:
                width=str(30)
            else:
                width=str(1)
            roundigit0=0
            roundlimit0=obs
            for i in range(10):
                if roundlimit0<1.0:
                    roundlimit0=roundlimit0*10
                    roundigit0+=1
            
            roundigit1=0
            roundlimit1=thisexp
            for i in range(10):
                if roundlimit1<1.0:
                    roundlimit1=roundlimit1*10
                    roundigit1+=1
                    
            roundigit2=0
            roundlimit2=thisexp_m2
            for i in range(10):
                if roundlimit2<1.0:
                    roundlimit2=roundlimit2*10
                    roundigit2+=1
                    
                    
            roundigit3=0
            roundlimit3=thisexp_m1
            for i in range(10):
                if roundlimit3<1.0:
                    roundlimit3=roundlimit3*10
                    roundigit3+=1
                    
            roundigit4=0
            roundlimit4=thisexp_p1
            for i in range(10):
                if roundlimit4<1.0:
                    roundlimit4=roundlimit4*10
                    roundigit4+=1
                    
            roundigit5=0
            roundlimit5=thisexp_p2
            for i in range(10):
                if roundlimit5<1.0:
                    roundlimit5=roundlimit5*10
                    roundigit5+=1
            
            if "Rho" in filename:
                mZtZ=filename[filename.find("SigRho")+6:filename.find("_",filename.find("SigRho")+6)]
                print mZtZ
                mZ=mZtZ[0:4]
                mT=mZtZ[4:]
                print mZ
                print mT
            if "Gstar" in filename:
                mZtZ=filename[filename.find("SigGstar")+8:filename.find("_",filename.find("SigGstar")+8)]
                print mZtZ
                mZ=mZtZ[0:4]
                mT=mZtZ[4:]
                print mZ
                print mT
                                
                                      
            if "tWb" in filename:
                decay="$\\text{T}\\rightarrow\\text{Wb}$"
            elif "ttZ" in filename:
                decay="$\\text{T}\\rightarrow\\text{Zt}$"
            else:
                decay="$\\text{T}\\rightarrow\\text{Ht}$"
            #print   roundigit
        
            text=text+mZ+"&"+width+"&"+mT+"&"+decay+"&"+str(round(obs,roundigit0+1))+"&"+str(round(thisexp_m2,roundigit1+1))+"&"+str(round(thisexp_m1,roundigit3+1))+"&"+str(round(thisexp,roundigit3+1))+"&"+str(round(thisexp_p1,roundigit4+1))+"&"+str(round(thisexp_p2,roundigit5+1))+"""\\\\
"""
            
            
scriptname='alllimits.txt'
f=open(scriptname,'w')
f.write(text)
f.close()
            
     