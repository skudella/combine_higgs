#!/bin/bash 


cd /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src
eval `scram runtime -sh`
cd /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/plotutils_workspaces

for i in Sig*plotutils; do cd /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/plotutils_workspaces/$i;echo $i; combine -M Asymptotic --minosAlgo stepping --run blind --rMin -10 --rMax 10 -n _Asymptotic $i.root; cd ..; done
