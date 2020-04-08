datapath = 'data/coco/mscoco/unfiltered/'
# filenames = [datapath + 'train_gold_clean.txt', datapath + 'val_gold_clean.txt', datapath + 'test_gold_clean.txt']
filenames = [datapath + 'val_gold.txt', datapath + 'test_gold.txt']

with open(datapath + 'val-test_gold.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)
