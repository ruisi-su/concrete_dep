#!/bin/bash
python train.py --t_states 25 --nt_states 20 --num_epochs 20 --train_file data/multimodal_dep_2_split_noverb_dice_v2/cocotrain.pkl --val_file data/multimodal_dep_2_split_noverb_dice_v2/cocoval.pkl --test_file data/multimodal_dep_2_split_noverb_dice_v2/cocotest.pkl --save_path dump_model/baseline_h512_nt20_t25_tembinit_b4_step2.pt --log_dir runs/baseline_h512_nt20_t25 --print_every 100 --pretrained_word_emb data/vico_500.pkl --state_dim 500 --max_length 20 --final_max_length 35 --h_dim 512 --seperate_nt_emb_for_emission --head_first --tie_word_emb --seed 1022 --t_emb_init glovevico-kmeans-25-centroids-500.txt --opt_level O2 --gpu 0 --delay_step 2 --lr 0.0005
