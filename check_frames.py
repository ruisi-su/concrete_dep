from collections import defaultdict
import math
import sys

cnt_frame_dep = defaultdict(lambda: 0)
cnt_frame = defaultdict(lambda: 0)
cnt_dep = defaultdict(lambda: 0)

sents = 0.0

frame_file = sys.argv[1]
dep_file = sys.argv[2]

data_path = 'data/mscoco/'
with open(data_path+frame_file, 'r') as frame, open(data_path+dep_file, 'r') as dep:
    read = []
    for fstr, dstr in zip(frame,dep):
        sents += 1.0
        fs = fstr.strip().split('\t')
        ds = dstr.strip().split('\t')
        for d in ds:
            cnt_dep[d] += 1.0
        for f in fs:
            cnt_frame[f] += 1.0
            for d in ds:
                cnt_frame_dep[f, d] += 1.0

scored_pairs = []
print(len(cnt_frame_dep))
for tup, c in cnt_frame_dep.items():
    if c > 1:
        f, d = tup
        scored_pairs.append((f, d, math.log(cnt_frame_dep[f,d]/cnt_dep[d]) - math.log(cnt_frame[f]/sents)))

scored_pairs.sort(key=lambda x: x[2], reverse=True)
with open(data_path+'mutual_inf.txt', 'w') as mi:
    for v in scored_pairs[:100]:
        print(v)
        mi.write(str(v))
        mi.write('\n')

# kframe = sorted(denomframe.keys(), key=lambda x: denomframe[x], reverse=True)
# for k in kframe[:10]:
#     print(k, denomframe[k])