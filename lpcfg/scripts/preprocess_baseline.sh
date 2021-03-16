#!/bin/bash
outputdir=$1

mkdir -p $outputdir
python preprocess.py --vocabsize 100000 --replace_num 1 --dep --outputfile $outputdir/coco