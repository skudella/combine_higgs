#!/bin/bash 
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch 
source $VO_CMS_SW_DIR/cmsset_default.sh 
export SCRAM_ARCH=slc6_amd64_gcc530
cd /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src
eval `scram runtime -sh`
cd - 

for i in *datacard.txt; do text2workspace.py $i text2workspace.py -o ${i%_datacard.txt}.root -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose  --PO 'map=.*/(Zprime_*|SC_Zprime*):r[1,-10,10]'; echo ${i%_datacard.txt}.root;
done

