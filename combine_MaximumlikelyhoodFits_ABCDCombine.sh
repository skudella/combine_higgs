#!/bin/bash 


cd /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src
eval `scram runtime -sh`
cd /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic

for i in Sig*Combine; do cd $i;echo $i combine; -M MaxLikelihoodFit --minimizerStrategy 0 --minimizerTolerance 0.1 --rMin -10 --rMax 10 -t -1 --expectSignal 1 --saveNormalizations --saveShapes --plots -n _MaxLikelihood_wAsimov_wSig $i.root; combine -M MaxLikelihoodFit --minimizerStrategy 0 --minimizerTolerance 0.1 --rMin -10 --rMax 10 -t -1 --expectSignal 0 --saveNormalizations --saveShapes --plots -n _MaxLikelihood_wAsimov_nSig $i.root; combine -M MaxLikelihoodFit --minimizerStrategy 0 --minimizerTolerance 0.1 --rMin -10 --rMax 10 --saveNormalizations --saveShapes --plots -n _MaxLikelihood_nAsimov $i.root; cd ..; done
