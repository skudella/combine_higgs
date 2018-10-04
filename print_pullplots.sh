#!/bin/bash

for i in Sig*/; do cd $i; for j in mlfit*.root ; do python /nfs/dust/cms/user/skudella/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/data/ZprimeToTprimeAllHadronic/diffNuisances.py -g ${j}_pullplot $j; done;  cd .. ;  done
