#!/bin/bash
model=$1
reward=$2
gpu=$3

python -u train.py --t_states 20 --nt_states 15 --num_epochs 10 --train_file data/unified_fix_no_pred/cocotrain.pkl --val_file data/unified_fix_no_pred/cocodev.pkl --test_file data/unified_fix_no_pred/cocotest.pkl --save_path dump_model/$model --print_every 1000 --pretrained_word_emb data/coco300fasttext.pkl --state_dim 300 --max_length 15 --final_max_length 20 --h_dim 128 --seperate_nt_emb_for_emission --head_first --tie_word_emb --seed 1022 --t_emb_init fasttext-coco-kmeans-20-centroids-300.txt  --opt_level O2 --gpu $gpu --delay_step 2 --lr 0.0005 --data_type both --evaluate_dep --reward $2 --non_root

