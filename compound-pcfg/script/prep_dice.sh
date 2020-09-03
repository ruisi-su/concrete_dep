#!/bin/bash
python preprocess.py --vocabsize 100000 --replace_num 1 --constraint_type 3 --align_type 3.0 --eqn_type dice --thresh 0.001 --dep --outputfile data/multimodal_dice_30/coco --data_type constraints
