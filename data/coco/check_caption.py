from collections import Counter
import numpy as np
from functools import reduce
import statistics
from statistics import mode

unique_ids = []
# with open('test_ids.txt', 'r') as data, open('VGNSL_ids/test_ids.filter.txt', 'w') as data_filt:
#     for i, line in enumerate(data):
#         if i % 5 == 0:
#             id_per_5 = []
#         id_list_1 = line.strip().replace('[','').replace(']','').replace(' ','').split(',')
#         id_per_5.append(id_list_1)
#         if i % 5 == 4:
#             assert(len(id_per_5) == 5)
#             if [''] in id_per_5:
#                 id_per_5.remove([''])
#             res = reduce(np.intersect1d, np.array(id_per_5))
#             print(id_per_5)
#
#             if len(res) > 0:
#                 most_common = res[0]
#             else:
#                 # find by majority vote
#                 flatten_list = [item for sublist in id_per_5 for item in sublist]
#                 most_common = mode(flatten_list)
#             # print('most common is ' + str(most_common) + 'for id ' + str(i))
#             if most_common in unique_ids:
#                 print('dup for ' + str(most_common) +' id with ' + str(i))
#             unique_ids.append(most_common)
#             data_filt.write(str(most_common) + '\n')

with open('VGNSL_ids/check.filter.txt', 'r') as train:
    for i, line in enumerate(train):
        unique_ids.append(line.strip())
assert(len(set(unique_ids)) == len(unique_ids))
