#!/bin/bash
python preprocess.py --vocabsize 100000 --replace_num 1 --batchsize 16 --constraint_type 3 --align_type split_all --eqn_type dice --thresh 0.1  --dep --outputfile data/multimodal_dep_3_batch_16_split_all_dice/coco
