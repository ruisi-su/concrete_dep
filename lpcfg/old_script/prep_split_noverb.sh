#!/bin/bash
python preprocess.py --vocabsize 100000 --replace_num 1 --constraint_type 3 --align_type split_noverb --eqn_type dice --vocabfile data/ptb/ptb.dict --dep --outputfile data/mscoco_ptb_dict/coco
