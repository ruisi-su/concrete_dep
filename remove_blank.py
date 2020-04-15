datapath = 'data/coco/mscoco/unfiltered/original/'
cap_file = 'test_name.txt'
frame_file = 'test_frame.txt'
out_file = 'test_name_clean.txt'
with open(datapath + cap_file, 'r') as cap, open(datapath + frame_file, 'r') as fr, open(datapath + out_file, 'w') as out:
    for tree, frame in zip(cap, fr):
        frame = frame.strip().split('\t')
        if frame[0] == '':
            continue
        else:
            out.write(tree)


# with open(datapath + frame_file, 'r') as fr, open(datapath + out_file, 'w') as out:
#     for frame in fr:
#         frame_r = frame.strip()
#         if frame_r == '':
#             continue
#         else:
#             out.write(frame)
