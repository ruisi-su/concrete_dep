import math
from collections import Counter

# check and update dictionary with counters
# dict: dictionary to search in
# id: key in the dictionary to search for
# c_id: id of the element in the counter to look for
def update_dict(dict, id, c_id):
    # update dict
    if id not in dict.keys():
        dict[id] = Counter()
    # update counter
    if c_id in dict[id].keys():
        dict[id][c_id] += 1
    else:
        dict[id][c_id] = 1
    # print(dict)
    return dict

# update probability values instead of count
def update_dict_prob(dict, ids, c_id, prob):
    for id in ids:
        # update dict
        if id not in dict.keys():
            dict[id] = {}
        # update counter
        if c_id in dict[id].keys():
            dict[id][c_id] += prob
        else:
            dict[id][c_id] = prob
        # print(dict)
    return dict

def initLinear(linear, val = None):
  if val is None:
    fan = linear.in_features +  linear.out_features
    spread = math.sqrt(2.0) * math.sqrt( 2.0 / fan )
  else:
    spread = val
  linear.weight.data.uniform_(-spread,spread)
  linear.bias.data.uniform_(-spread,spread)
