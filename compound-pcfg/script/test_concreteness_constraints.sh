#!/bin/bash
python train.py --t_states 25 --nt_states 20 --num_epochs 20 --train_file data/mscoco_concrete/cocotrain.pkl --val_file data/mscoco_concrete/cocoval.pkl --test_file data/multimodal_dep_3_split_noverb_dice_noalign/cocotest.pkl --load_model dump_model/concreteness_scale_2.pt --print_every 100 --pretrained_word_emb data/fasttext300.pkl --state_dim 300 --max_length 20 --final_max_length 35 --h_dim 512 --seperate_nt_emb_for_emission --head_first --tie_word_emb --seed 1022 --t_emb_init fasttext-ptb-kmeans-25-centroids-300.txt --opt_level O2 --gpu 2 --delay_step 2 --lr 0.0005 --beta1 0.9 --data_type constraints --con_mult 0.0 --evaluate_dep --mode test --out_file outputs/test_scale_2_constraints.txt
