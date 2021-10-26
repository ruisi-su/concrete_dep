#!/bin/bash
outputdir=$1
concre=$2

mkdir -p $outputdir

python preprocess.py --vocabsize 100000 --replace_num 1 --dep --outputfile $outputdir/coco --concrete_file $concre --gpu 0
