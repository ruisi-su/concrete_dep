datapath = 'data/coco/mscoco/unfiltered/'
filenames = [datapath + 'train_gold_clean.txt', datapath + 'val_gold_clean.txt', datapath + 'test_gold_clean.txt']
with open(datapath + 'train-val-test_gold.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)
