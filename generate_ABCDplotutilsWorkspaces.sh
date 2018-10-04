#!/bin/bash 

cd /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src
eval `scram runtime -sh`

cd /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/plotutils_datacards

for i in Sig*plotutils_datacard.txt; do cd ../plotutils_workspaces ; mkdir ${i%_datacard.txt}; done
cd /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/plotutils_datacards

for i in Sig*plotutils_datacard.txt; do echo ${i%_datacard.txt}; cd /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic  ; text2workspace.py plotutils_datacards/$i -o plotutils_workspaces/${i%_datacard.txt}/${i%_datacard.txt}.root; done
