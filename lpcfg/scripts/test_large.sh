#!/bin/bash
model=$1
datadir=$2
dtype=$3
output=$4
reward=$5
gpu=$6
python -u train.py --t_states 25 --nt_states 20 --num_epochs 20 --train_file data/$datadir/cocotrain.pkl --val_file data/$datadir/cocodev.pkl --test_file data/$datadir/cocotest.pkl --load_model dump_model/$model --print_every 100 --pretrained_word_emb data/coco300fasttext.pkl --state_dim 300 --max_length 15 --final_max_length 20 --seperate_nt_emb_for_emission --head_first --tie_word_emb --seed 1022 --t_emb_init fasttext-coco-kmeans-25-centroids-300.txt --opt_level O2 --gpu $gpu --delay_step 2 --lr 0.0005 --data_type $dtype --evaluate_dep --reward $reward --mode test --out_file $output --non_root

