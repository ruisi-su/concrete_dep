#!/bin/bash
python preprocess.py --vocabsize 100000 --replace_num 1 --constraint_type 3 --align_type temp --eqn_type dice --dep --thresh 0.5 --outputfile data/multimodal_dep_3_temp/coco
