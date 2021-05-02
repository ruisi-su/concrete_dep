#!/bin/bash
outputdir=$1

mkdir -p $outputdir
python preprocess.py --replace_num 1 --dep --outputfile $outputdir/ptb --inputdir ../data/ptb/ --vocabfile ../data/ptb/ptb.dict --concrete_file ../data/concreteness_modified.txt