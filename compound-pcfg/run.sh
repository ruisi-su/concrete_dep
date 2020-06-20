#!/bin/bash
python train.py  --t_states 20 --nt_states 10 --num_epochs 20 --load_model dump_model/baseline_vico_h512.pt --pretrained_word_emb data/multimodal/vico_500.pkl --state_dim 500 --seperate_nt_emb_for_emission --head_first --tie_word_emb --test_file data/multimodal_dep_2/cocotest.pkl --out_file outputs/test_h512_type3_span.txt --multimodal 1 --evaluate_dep  --mode test --gpu 0
