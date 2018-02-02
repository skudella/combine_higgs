import sys
import os
import subprocess
import time
import datetime
import stat


print 'Creating datacards'

cmsswpath='/nfs/dust/cms/user/skudella/CMSSW_7_4_7'
Signal_nick="Zprime15001200"


def createScript(datacardname,ABCDversion,Signal_nick):
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
imax 2 #number of bins/channels
jmax 3 #number of backgrounds
kmax *
---------------
shapes * * """ + datacardname + """.root $PROCESS_nominal $PROCESS_$SYSTEMATIC
---------------
bin ZprimeM_nottopbtag	ZprimeM_withtopbtag
observation -1 -1
------------------------------
bin             ZprimeM_nottopbtag ZprimeM_nottopbtag ZprimeM_nottopbtag ZprimeM_nottopbtag ZprimeM_withtopbtag ZprimeM_withtopbtag ZprimeM_withtopbtag ZprimeM_withtopbtag
process         """ +  Signal_nick + "_" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """ ttbar_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """ QCD_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """ SC_""" + Signal_nick + "_" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """ """ +  Signal_nick + "_" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """ ttbar_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """ QCD_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """ SC_""" + Signal_nick + "_" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """
process         0 1 2 3 0 1 2 3
rate            -1 -1 -1 -1 -1 -1 -1 -1 

--------------------------------
_notopbtag_ZprimeM_syst	   shape    -   -  1.0  -   -   -   -   -       ABCD uncertainty on QCDbackground
_withtopbtag_ZprimeM_syst  shape    -   -   -   -   -   -  1.0  -       ABCD uncertainty on QCDbackground 
_MCSF_CSVLF                shape   1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0      MCSF uncertainty from ttbar and SC influencing also QCD
_MCSF_CSVHF                shape   1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0      MCSF uncertainty from ttbar and SC influencing also QCD
_MCSF_CSVHFStats1          shape   1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0      MCSF uncertainty from ttbar and SC influencing also QCD
_MCSF_CSVLFStats1          shape   1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0      MCSF uncertainty from ttbar and SC influencing also QCD
_MCSF_CSVHFStats2          shape   1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0      MCSF uncertainty from ttbar and SC influencing also QCD
_MCSF_CSVLFStats2          shape   1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0      MCSF uncertainty from ttbar and SC influencing also QCD
_MCSF_CSVCErr1             shape   1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0      MCSF uncertainty from ttbar and SC influencing also QCD
_MCSF_CSVCErr2             shape   1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0      MCSF uncertainty from ttbar and SC influencing also QCD
_MCSF_toptag               shape   1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0      MCSF uncertainty from ttbar and SC influencing also QCD
_MCSF_Wtag                 shape   1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0      MCSF uncertainty from ttbar and SC influencing also QCD
_MCSF_PU                   shape   1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0      MCSF uncertainty from ttbar and SC influencing also QCD
_MCSF_PDF                  shape    -  1.0 1.0 1.0  -  1.0 1.0 1.0      MCSF uncertainty from ttbar and SC influencing also QCD
_MCSF_Lumi                 shape   1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0      MCSF uncertainty from ttbar and SC influencing also QCD
_MCSF_renfac_env           shape    -  1.0 1.0 1.0  -  1.0 1.0 1.0      MCSF uncertainty from ttbar and SC influencing also QCD
_nominal_JER               shape   1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0      MCSF uncertainty from ttbar and SC influencing also QCD
_nominal_JES               shape   1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0      MCSF uncertainty from ttbar and SC influencing also QCD
_ttbarXSUp                 shape   1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0      MCSF uncertainty from ttbar and SC influencing also QCD
_ttbarXSDown               shape   1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0      MCSF uncertainty from ttbar and SC influencing also QCD
"""
  
 
  
  
  
  
  f=open(datacardname+'_datacard.txt','w')
  f.write(script)
  f.close()
  #st = os.stat(datacardname)
  #os.chmod(datacardname, st.st_mode | stat.S_IEXEC)

indir = '/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic'
outdir= '/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic'
#scriptdir= '/nfs/dust/cms/user/skudella/processed_MC/flat_trees_new/birdscripts/scripts/'
#scalefunctionsdir='/nfs/dust/cms/user/skudella/addBranch/TreeAnalyzer/'
#scalefunctions='Zprime_SBSSSFs_Graphs.root'

#os.chdir(scriptdir)



for root, dirs, filenames in os.walk(indir):
    for f in filenames:
        if f.find('.root')>0 and f.find('ABCD')>0:
            ABCDversion='ABCDfail'
            if 'ABCD1' in f:
                ABCDversion='ABCD1'
            if 'ABCD2' in f:
                ABCDversion='ABCD2'
            if 'ABCD3' in f:
                ABCDversion='ABCD3'
            if 'ABCD4' in f:
                ABCDversion='ABCD4'
            if 'ABCD5' in f:
                ABCDversion='ABCD5'
            if 'ABCD6' in f:
                ABCDversion='ABCD6'
            if 'ABCD7' in f:
                ABCDversion='ABCD7'
                
            createScript(f[:f.find('.root')],ABCDversion,Signal_nick)


#indir = '/nfs/dust/cms/user/skudella/processed_MC/flat_trees_new/BKG_TTbar/'

##os.chdir(scriptdir)

#for root, dirs, filenames in os.walk(indir):
    #for f in filenames:
        #if f.find('.root')>0:
            #createScript(f[:f.find('.root')]+'_subscript.sh',scalefunctionsdir+'bin/test','renaming',indir+f,outdir+f[:f.find('.root')]+'_out',9999999999,0)

#indir = '/nfs/dust/cms/user/skudella/processed_MC/flat_trees_new/Signal_Zprime/'

##os.chdir(scriptdir)

#for root, dirs, filenames in os.walk(indir):
    #for f in filenames:
        #if f.find('.root')>0:
            #createScript(f[:f.find('.root')]+'_subscript.sh',scalefunctionsdir+'bin/test','renaming',indir+f,outdir+f[:f.find('.root')]+'_out',9999999999,0)
