#!/bin/bash
python preprocess.py --vocabsize 100000 --replace_num 1 --constraint_type 3 --align_type split_noverb --eqn_type dice --thresh 0.0 --dep --outputfile data/multimodal_dep_3_split_noverb_dice_v2_nothresh/coco
