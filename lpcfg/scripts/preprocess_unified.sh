#!/bin/bash
outputdir=$1
align_in=$2
align_out=$3
concre=$4

mkdir -p $outputdir

python preprocess.py --vocabsize 100000 --replace_num 1 --dep --outputfile $outputdir/coco --align_input $align_in --align_output $align_out --concrete_file $concre --gpu 0
