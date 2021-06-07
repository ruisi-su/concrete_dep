#!/bin/bash
model=$1
datadir=$2
reward=$3
gpu=$4

python -u train.py --t_states 25 --nt_states 20 --num_epochs 10 --train_file data/$datadir/cocotrain.pkl --val_file data/$datadir/cocodev.pkl --test_file data/$datadir/cocotest.pkl --save_path dump_model/$model --print_every 1000 --pretrained_word_emb data/coco300fasttext.pkl --state_dim 300 --max_length 15 --final_max_length 20 --seperate_nt_emb_for_emission --head_first --tie_word_emb --seed 1022 --t_emb_init fasttext-ptb-kmeans-25-centroids-300.txt  --opt_level O2 --gpu $gpu --delay_step 2 --data_type concreteness --evaluate_dep --reward $reward --lr 0.0005 --beta1 0.9 --non_root
