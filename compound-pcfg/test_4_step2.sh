#!/bin/bash
python train.py --t_states 25 --nt_states 20 --num_epochs 20 --train_file data/multimodal_dep_3_split_noverb_dice_v2_nothresh/cocotrain.pkl --val_file data/multimodal_dep_3_split_noverb_dice_v2_nothresh/cocoval.pkl --test_file data/multimodal_dep_3_split_noverb_dice_v2_nothresh/cocotest.pkl --load_model dump_model/baseline_h512_nt20_t25_tembinit_b4_step2.pt --pretrained_word_emb data/vico_500.pkl --max_length 20 --final_max_length 35 --state_dim 500 --h_dim 512 --seperate_nt_emb_for_emission --head_first --tie_word_emb --seed 1022 --t_emb_init glovevico-kmeans-25-centroids-500.txt --multimodal 0 --mode test --gpu 1
