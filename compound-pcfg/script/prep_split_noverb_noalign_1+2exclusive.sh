#!/bin/bash
python preprocess.py --vocabsize 100000 --replace_num 1 --constraint_type 5 --align_type split_noverb --eqn_type dice --thresh 0.0 --no_align --dep --outputfile data/multimodal_dep_5_noalign/coco
