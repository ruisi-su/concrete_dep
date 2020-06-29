data_dir = 'data/coco/VGNSL_split/'
align_dir = 'alignments/'
with open(data_dir + 'traindevtest.cap', 'r') as cap, open(data_dir + 'traindevtest.frame', 'r') as frame, open(data_dir + align_dir + 'traindevtest.cap-frame.split_all.v2', 'w') as out:
    for c, f in zip(cap, frame):
        c = c.strip()
        flist = f.strip().split('\t')
        # fline is what to print on the input line after caption
        fline = []
        if len(flist) > 1:
            pred = flist[0].split('_')[0]
            fline.append(pred)
            for fitem in flist:
                fitems = fitem.split('_')
                fline += fitems[1:]
                # print(' '.join(fline))

            flstr = ' '.join(fline)
            output = c + ' ||| ' + flstr + '\n'
            out.write(output)
        else:
            out.write('\n')
