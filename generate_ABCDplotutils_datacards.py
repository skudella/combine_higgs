import sys
import os
import subprocess
import time
import datetime
import stat


print 'Creating datacards'

cmsswpath='/nfs/dust/cms/user/skudella/CMSSW_7_4_7'
#SignalNick="SigZprime15001200"
#SignalNickList=["SigZprime15001200","SigZprime20001200","SigZprime25001200","SigZprime1500700","SigZprime1500900","SigZprime2000900","SigZprime20001500","SigZprime25001500","SigGstar1500800Nar","SigGstar15001000Nar","SigGstar15001300Nar","SigGstar20001000Nar","SigGstar20001300Nar","SigGstar20001500Nar","SigGstar25001300Nar","SigGstar25001500Nar","SigGstar25001800Nar","SigGstar30001500Nar","SigGstar30001800Nar","SigGstar30002100Nar","SigGstar35001800Nar","SigGstar35002100Nar","SigGstar35002500Nar","SigGstar40002100Nar","SigGstar40002500Nar","SigGstar40003000Nar","SigGstar1500800Wid","SigGstar15001000Wid","SigGstar15001300Wid","SigGstar20001000Wid","SigGstar20001300Wid","SigGstar20001500Wid","SigGstar25001300Wid","SigGstar25001500Wid","SigGstar25001800Wid","SigGstar30001500Wid","SigGstar30001800Wid","SigGstar30002100Wid","SigGstar35001800Wid","SigGstar35002100Wid","SigGstar35002500Wid","SigGstar40002100Wid","SigGstar40002500Wid","SigGstar40003000Wid","SigGstar17501300Nar","SigGstar22501300Nar","SigGstar22501500Nar","SigGstar27501500Nar","SigGstar17501300Wid","SigGstar22501300Wid","SigGstar22501500Wid","SigGstar27501500Wid"]
SignalNickList=["SigZprime15001200_tWb","SigZprime20001200_tWb","SigZprime25001200_tWb","SigZprime1500700_tWb","SigZprime1500900_tWb","SigZprime2000900_tWb","SigZprime20001500_tWb","SigZprime25001500_tWb","SigZprime15001200_ttZ","SigZprime20001200_ttZ","SigZprime25001200_ttZ","SigZprime1500700_ttZ","SigZprime1500900_ttZ","SigZprime2000900_ttZ","SigZprime20001500_ttZ","SigZprime25001500_ttZ","SigZprime15001200_ttH","SigZprime20001200_ttH","SigZprime25001200_ttH","SigZprime1500700_ttH","SigZprime1500900_ttH","SigZprime2000900_ttH","SigZprime20001500_ttH","SigZprime25001500_ttH"]
#ABCDversion='ABCD2'

SignalNickList=[]

for Masses in ["SigZprime15001200","SigZprime20001200","SigZprime25001200","SigZprime1500700","SigZprime1500900","SigZprime2000900","SigZprime20001500","SigZprime25001500"]:
    for BR in ["_tWb","_ttZ","_ttH","_BR05_025_025"]:
        SignalNickList.append(Masses+BR)

def createScript(ABCDversion,WWP,SignalNick):
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
shapes data_obs CatA_wtb rootfiles/output_rebinned_added_""" + ABCDversion + WWP + """.root DATA_noSignal_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal
shapes data_obs CatA_ntb rootfiles/output_rebinned_added_""" + ABCDversion + WWP + """.root DATA_noSignal_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal

shapes Sig      CatA_wtb rootfiles/output_rebinned_added_""" + ABCDversion + WWP + """.root """ + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal  """ + SignalNick + "_"  + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes Sig      CatA_ntb rootfiles/output_rebinned_added_""" + ABCDversion + WWP + """.root """ + SignalNick + "_"  + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal  """ + SignalNick + "_"  + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC

shapes tt       CatA_wtb rootfiles/output_rebinned_added_""" + ABCDversion + WWP + """.root ttbar_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal  ttbar_""" + ABCDversion + """_withtopbtag_CatA_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes tt       CatA_ntb rootfiles/output_rebinned_added_""" + ABCDversion + WWP + """.root ttbar_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_nominal  ttbar_""" + ABCDversion + """_notopbtag_CatA_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC

shapes QCD      CatA_wtb rootfiles/DATA_noSignalQCDMadgraph_""" + ABCDversion + WWP + """_withtopbtag_ZprimeM_combinehistos.root QCDandSC_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """_nominal QCDandSC_""" + ABCDversion + """_withtopbtag_CatB_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC
shapes QCD      CatA_ntb rootfiles/DATA_noSignalQCDMadgraph_""" + ABCDversion + WWP + """_notopbtag_ZprimeM_combinehistos.root QCDandSC_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """_nominal QCDandSC_""" + ABCDversion + """_notopbtag_CatB_Zprime_M_""" + ABCDversion + """_$SYSTEMATIC

------------------------------
bin             CatA_ntb   CatA_wtb
observation     -1         -1
------------------------------
bin                               CatA_ntb CatA_wtb CatA_ntb CatA_wtb CatA_ntb CatA_wtb 
process                           Sig      Sig      QCD      QCD      tt       tt           
process                           0        0        1        1        2        2
rate                              -1       -1       -1       -1       -1       -1

--------------------------------
#notopbtag_ZprimeM_syst	  shape    -        -       1.0       -        -        -       #ABCD uncertainty on QCDbackground
#withtopbtag_ZprimeM_syst  shape    -        -        -       1.0       -        -       #ABCD uncertainty on QCDbackground 

ABCD_rate	          shape    -        -       1.0       -        -        -       #ABCD uncertainty on QCDbackground
ABCD_shape                shape    -        -        -       1.0       -        -       #ABCD uncertainty on QCDbackground 

MCSF_CSVLF                shape   1.0      1.0      1.0      1.0      1.0      1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVHF                shape   1.0      1.0      1.0      1.0      1.0      1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVHFStats1          shape   1.0      1.0      1.0      1.0      1.0      1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVLFStats1          shape   1.0      1.0      1.0      1.0      1.0      1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVHFStats2          shape   1.0      1.0      1.0      1.0      1.0      1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVLFStats2          shape   1.0      1.0      1.0      1.0      1.0      1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVCErr1             shape   1.0      1.0      1.0      1.0      1.0      1.0      #MCSF uncertainty from ttbar and SC
MCSF_CSVCErr2             shape   1.0      1.0      1.0      1.0      1.0      1.0      #MCSF uncertainty from ttbar and SC
MCSF_toptag               shape   1.0      1.0      1.0      1.0      1.0      1.0      #MCSF uncertainty from ttbar and SC
MCSF_Wtag                 shape   1.0      1.0      1.0      1.0      1.0      1.0      #MCSF uncertainty from ttbar and SC
MCSF_PU                   shape   1.0      1.0      1.0      1.0      1.0      1.0      #MCSF uncertainty from ttbar and SC
MCSF_PDF                  shape    -        -       1.0      1.0      1.0      1.0      #MCSF uncertainty from ttbar
MCSF_Lumi                 shape   1.0      1.0      1.0      1.0      1.0      1.0      #MCSF uncertainty from ttbar and SC
MCSF_renfac_env           shape    -        -       1.0      1.0      1.0      1.0      #MCSF uncertainty from ttbar
nominal_JER               shape   1.0      1.0      1.0      1.0      1.0      1.0      #MCSF uncertainty from ttbar and SC
nominal_JES               shape   1.0      1.0      1.0      1.0      1.0      1.0      #MCSF uncertainty from ttbar and SC
ttbarXS                   shape   1.0      1.0      1.0      1.0      1.0      1.0      #MCSF uncertainty from ttbar and SC
"""
#nominal_JER               shape   1.0      1.0      1.0      1.0      1.0      1.0      #MCSF uncertainty from ttbar and SC
#nominal_JES               shape   1.0      1.0      1.0      1.0      1.0      1.0      #MCSF uncertainty from ttbar and SC

  for i in range(1,15):
        script=script+"""
nominal_bin""" + str(i) + """stat                  shape    -        -       1.0      1.0       -        -       #uncertainty from statistic in sideband"""




  
 
  
  
  
  
  f=open('plotutils_datacards/'+SignalNick+'_'+ABCDversion+WWP+'_'+'plotutils_datacard.txt','w')
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



#for root, dirs, filenames in os.walk(indir):
    #for f in filenames:
        #if f.find('.root')>0 and f.find('ABCD')>0:
            #ABCDversion='ABCDfail'
            #if 'ABCD1' in f:
                #ABCDversion='ABCD1'
            #if 'ABCD2' in f:
                #ABCDversion='ABCD2'
                #ABCDuncertainty_wtb=''
                #ABCDuncertainty_ntb=''
            #if 'ABCD3' in f:
                #ABCDversion='ABCD3'
            #if 'ABCD4' in f:
                #ABCDversion='ABCD4'
            #if 'ABCD5' in f:
                #ABCDversion='ABCD5'
            #if 'ABCD6' in f:
                #ABCDversion='ABCD6'
            #if 'ABCD7' in f:
                #ABCDversion='ABCD7'
                
            #createScript(f[:f.find('.root')],ABCDversion,Signal_nick)
for SignalNick in SignalNickList:
    #for ABCDversion in ['ABCD3','ABCD5']:
    for ABCDversion in ['ABCD5']:
        #for WWP in ['','_loose_new','_medium_new']:
        for WWP in ['_medium_new','_medium_Anna']:
            print SignalNick
            createScript(ABCDversion,WWP,SignalNick)
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
print 'Datacards created'
