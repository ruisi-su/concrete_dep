#!/bin/bash
python preprocess.py --vocabsize 100000 --replace_num 1 --dep --outputfile data/mscoco_concrete_modifed/coco --data_type concreteness --concrete_file Concreteness_ratings_Brysbaert_et_al_BRM_modified.txt
