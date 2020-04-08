
datapath = 'data/coco/mscoco/unfiltered/'
cap_file = 'val_cap.txt'
frame_file = 'val_frame.txt'
out_file = 'val_cap_clean.txt'
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
