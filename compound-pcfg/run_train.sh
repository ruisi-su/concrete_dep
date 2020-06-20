#!/bin/bash
python train.py --t_states 20 --nt_states 10 --num_epochs 20 --save_path dump_model/baseline_vico100_h512.pt --log_dir runs/baseline_vico100_h512 --pretrained_word_emb data/vico_100.pkl --state_dim 100 --seperate_nt_emb_for_emission --head_first --tie_word_emb --gpu 1
