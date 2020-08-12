#!/bin/bash
python train.py --t_states 25 --nt_states 20 --num_epochs 20 --train_file data/mscoco_concrete/cocotrain.pkl --val_file data/mscoco_concrete/cocoval.pkl --test_file data/mscoco_concrete/cocotest.pkl --load_model dump_model/concreteness_all.pt --print_every 100 --pretrained_word_emb data/fasttext300.pkl --state_dim 300 --max_length 20 --final_max_length 35 --h_dim 512 --seperate_nt_emb_for_emission --head_first --tie_word_emb --seed 1022 --t_emb_init fasttext-kmeans-25-centroids-300.txt --opt_level O2 --gpu 2 --delay_step 2 --lr 0.0005 --beta1 0.9 --data_type concreteness --mode test --evaluate_dep --concrete_scr 3.0 --concrete_type all --out_file outputs/concrete_all_00_30.txt
