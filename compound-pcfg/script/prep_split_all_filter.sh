#!/bin/bash
python preprocess.py --vocabsize 100000 --replace_num 1 --constraint_type 3 --align_type split_all --eqn_type dice --thresh 0.0 --test_only --dep --outputfile data/multimodal_dep_3_split_all_dice_filter_test/coco
