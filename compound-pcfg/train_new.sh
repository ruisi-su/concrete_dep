#!/bin/bash
python train.py --t_states 20 --nt_states 10 --num_epochs 20 --save_path dump_model/baseline_vico500_h256_nt10_t20_tembinit.pt --log_dir runs/baseline_vico500_h256_nt10_t20_tembinit --print_every 100 --pretrained_word_emb data/vico_500.pkl --max_length 20 --final_max_length 35 --state_dim 500 --h_dim 256 --opt_level O2 --seperate_nt_emb_for_emission --head_first --tie_word_emb --seed 1022 --t_emb_init glovevico-kmeans-20-centroids.txt --gpu 0
