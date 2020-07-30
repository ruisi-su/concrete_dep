import utils
import preprocess
from collections import Counter
import argparse, sys


predictions = open('./outputs/current_exp/test_4_noverb_noalign.txt', 'r')

head_dict = {}
for line in predictions:
    p, g, spans = line.strip().split('\t')
    g = g.replace('(', '').replace(')', '')
    g = g.split(' ')[2:]
    spans = list(eval(spans))
    # print(g)
    sent_l = len(g)
    # print(g)

    # init a counter for each word
    for w in g:
        if w not in head_dict.keys():
            count_dict = Counter({'immediate':0, 'intermediate':0, 'entire':0})
            head_dict[w] = count_dict
    # print(spans[0])
    for span in spans:
        (s, t, nt, h) = span
        span_l = t-s+1
        head_str = g[h]
        if span_l == 1:
            continue
        elif span_l <= 3:
            head_dict[head_str]['immediate'] += 1
        elif span_l > 3 and span_l < sent_l:
            head_dict[head_str]['intermediate'] += 1
        elif span_l == sent_l:
            head_dict[head_str]['entire'] += 1

head_dict_filter = {}
for head_c in head_dict.keys():
    total = sum(head_dict[head_c].values())
    if total != 0:
        head_dict_filter[head_c] = dict(head_dict[head_c])
        head_dict_filter[head_c]['total'] = total
head_dict_sorted = sorted(head_dict_filter.items(), key=lambda h: h[1]['total'], reverse=True)

for head in head_dict_sorted:
    word, hd = head
    print('{}\t{}\t{}\t{}\t{}'.format(word, hd['immediate'], hd['intermediate'], hd['entire'], hd['total']))