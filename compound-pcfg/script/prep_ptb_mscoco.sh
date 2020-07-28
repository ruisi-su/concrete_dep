#!/bin/bash
python preprocess.py --vocabsize 100000 --replace_num 1 --dep --vocabfile data/ptb/ptb-.dict --outputfile data/ptb_mscoco/coco --no_align --test_only
