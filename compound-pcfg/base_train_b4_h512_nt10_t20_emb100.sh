#!/bin/bash
python train.py --t_states 20 --nt_states 10 --num_epochs 20 --save_path dump_model/baseline_vico100_h512_nt10_t20.pt --log_dir runs/baseline_vico100_h512_nt10_t20 --print_every 100 --pretrained_word_emb data/vico_100.pkl --max_length 20 --final_max_length 35 --state_dim 100 --seperate_nt_emb_for_emission --head_first --tie_word_emb --gpu 0
