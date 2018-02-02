import sys
import os
import subprocess
import time
import datetime
import stat


print 'Creating workspace scripts'

cmsswpath='/nfs/dust/cms/user/skudella/CMSSW_7_4_7'
Signal_nick="Zprime15001200"


def createScript(datacardname,ABCDversion,Signal_nick):
  script="#!/bin/bash \n"
  if cmsswpath!='':
    script+="export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch \n"
    script+="source $VO_CMS_SW_DIR/cmsset_default.sh \n"
    script+="export SCRAM_ARCH="+os.environ['SCRAM_ARCH']+"\n"
    script+='cd '+cmsswpath+'/src\neval `scram runtime -sh`\n'
    script+='cd - \n'
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
  script+="""
text2workspace.py """ + datacardname + """.txt text2workspace.py -o """ + datacardname + """_workspace.root -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose  --PO \'map=.*/(Zprime_*|SC_Zprime*):r[1,-10,10]\'

"""
  
 
  
  
  
  
  f=open(datacardname+'_data2workspace.sh','w')
  f.write(script)
  f.close()
  st = os.stat(datacardname+'_data2workspace.sh')
  os.chmod(datacardname+'_data2workspace.sh', st.st_mode | stat.S_IEXEC)

indir = '/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic'
outdir= '/nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic'
#scriptdir= '/nfs/dust/cms/user/skudella/processed_MC/flat_trees_new/birdscripts/scripts/'
#scalefunctionsdir='/nfs/dust/cms/user/skudella/addBranch/TreeAnalyzer/'
#scalefunctions='Zprime_SBSSSFs_Graphs.root'

#os.chdir(scriptdir)



for root, dirs, filenames in os.walk(indir):
    for f in filenames:
        if f.find('.txt')>0 and f.find('ABCD')>0:
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
                
            createScript(f[:f.find('.txt')],ABCDversion,Signal_nick)


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
