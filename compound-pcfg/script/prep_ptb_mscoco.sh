#!/bin/bash
python preprocess.py --vocabsize 100000 --replace_num 1 --dep --vocabfile data/ptb/ptb-.dict --outputfile data/ptb_mscoco_concrete/coco --data_type concreteness
