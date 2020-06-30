#!/bin/bash
python preprocess.py --vocabsize 100000 --replace_num 1 --constraint_type 3 --align_type none --eqn_type dice --thresh 0.5 --dep --outputfile data/multimodal_dep_3_none_dice/coco
