datapath = 'data/coco/mscoco/dep/'
# filenames = [datapath + 'train_gold.txt', datapath + 'val_gold.txt', datapath + 'test_gold.txt']
filenames = [datapath + 'train.conllx', datapath + 'val.conllx', datapath + 'test.conllx']

with open(datapath + 'train-val-test_dep.conllx', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)
