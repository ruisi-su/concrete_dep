#!/bin/bash
python train.py --t_states 25 --nt_states 20 --num_epochs 20 --train_file data/ptb/ptb-train.pkl --val_file data/ptb/ptb-val.pkl --test_file data/ptb_mscoco/cocotest.pkl --load_model dump_model/baseline_h512_nt20_t25_tembinit_b4_step2_alpha1_fasttext_ptb.pt --log_dir runs/baseline_h512_nt20_t25_tembinit_b4_step2_alpha1_fasttext_ptb --print_every 100 --pretrained_word_emb data/ptb/ptb300fasttext.pkl --state_dim 300 --max_length 20 --final_max_length 35 --h_dim 512 --seperate_nt_emb_for_emission --head_first --tie_word_emb --seed 1022 --t_emb_init fasttext-ptb-kmeans-25-centroids-300.txt --opt_level O2 --gpu 2 --delay_step 2 --lr 0.0005 --beta1 0.9 --mode test --data_type ptb --evaluate_dep
