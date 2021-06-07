#!/bin/bash
python -u train.py --t_states 20 --nt_states 15 --num_epochs 20 --train_file data/coupling/cocotrain.pkl --val_file data/coupling/cocodev.pkl --test_file data/coupling/cocotest.pkl --save_path dump_model/coupling_h512_reward_1.pt --print_every 100 --pretrained_word_emb data/coco300fasttext.pkl --state_dim 300 --max_length 15 --final_max_length 20 --seperate_nt_emb_for_emission --head_first --tie_word_emb --seed 1022 --t_emb_init fasttext-coco-kmeans-20-centroids-300.txt --opt_level O2 --gpu 0 --delay_step 2 --lr 0.0005 --data_type coupling --evaluate_dep --reward 1.0 --non_root

