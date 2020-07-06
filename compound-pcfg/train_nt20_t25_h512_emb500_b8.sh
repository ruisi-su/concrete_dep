#!/bin/bash
python train.py --t_states 25 --nt_states 20 --num_epochs 20 --train_file data/multimodal_dep_3_batch_8_split_all_dice/cocotrain.pkl --val_file data/multimodal_dep_3_batch_8_split_all_dice/cocoval.pkl --test_file data/multimodal_dep_3_batch_8_split_all_dice/cocotest.pkl --save_path dump_model/baseline_vico500_h512_nt20_t25_tembinit_b8.pt --log_dir runs/baseline_vico500_h512_nt20_t25_tembinit_b8 --print_every 100 --pretrained_word_emb data/vico_500.pkl --max_length 20 --final_max_length 35 --state_dim 500 --h_dim 512 --seperate_nt_emb_for_emission --head_first --tie_word_emb --seed 1022 --t_emb_init glovevico-kmeans-25-centroids-500.txt --opt_level O2 --gpu 0
