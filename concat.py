datapath = 'data/coco/mscoco/unfiltered/'
# filenames = [datapath + 'train_gold.txt', datapath + 'val_gold.txt', datapath + 'test_gold.txt']
filenames = [datapath + 'val_cap_clean.txt', datapath + 'test_cap_clean.txt']

with open(datapath + 'val-test_cap.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)
