#!/bin/bash
python preprocess.py --vocabsize 100000 --replace_num 1 --constraint_type 3 --align_type temp --eqn_type dice --test_only --dep --thresh 0.0 --outputfile data/multimodal_dep_3_temp_filter_test/coco
