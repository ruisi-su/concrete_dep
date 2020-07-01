#!/bin/bash
python preprocess.py --vocabsize 100000 --replace_num 1 --constraint_type 2 --align_type split_noverb --eqn_type dice --thresh 0.5 --dep --outputfile data/multimodal_dep_2_split_noverb_dice_v2/coco
