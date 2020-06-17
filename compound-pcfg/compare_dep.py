import tqdm
import sys
from preprocess import *
# parse alignments and frames
def gen_dict(data_path):
    test_dict = {}

    with open(data_path+'_caps.txt', 'r') as cap, open(data_path+'_frames.txt', 'r') as frame, open(data_path+'.align', 'r') as align:
        for i, (c, f, a) in enumerate(zip(cap, frame, align)):
            if i not in test_dict.keys():
                test_dict[i] = {}
            test_dict[i]['caption'] = c.strip().lower()
            test_dict[i]['frame'] = f.strip().split('\t')
            test_dict[i]['alignment'] = a.strip().lower().split(' ')

    return test_dict


# get alignment and frame of a tree
def get_af(tree, dict):
    tree = tree.replace('(', '').replace(')','').lower()
    tree_toks = set(tree.split(' '))
    # print(tree)
    has_unk = False
    filter_words = {'<unk>', 'n:n', 'n', 'en', 'nth', 'mpn'}
    if len(tree_toks.intersection(filter_words)) > 0:
        has_unk = True
    for i in dict.keys():
        if dict[i]['caption'] == tree:
            a = ' '.join(dict[i]['alignment'])
            f = ' '.join(dict[i]['frame'])
            return (a, f)
        elif has_unk:
            cap_toks = set(dict[i]['caption'].split(' '))

            diff = tree_toks.difference(cap_toks)
            # print(diff)
            if (len(diff) < 3) and (diff.pop() in filter_words):
                a = ' '.join(dict[i]['alignment'])
                f = ' '.join(dict[i]['frame'])
                return (a, f)

    raise ValueError('Tree is not found in caption dictionary')

# gen dict
data_path = '../data/coco/VGNSL_split/test'
test_dict = gen_dict(data_path)

same = 0
diff = 0


# generate comparison results
dim = sys.argv[1]
out_file = sys.argv[2]

with open('test_h{}_base_dep.txt'.format(dim), 'r') as base, open('test_h{}_type1_dep.txt'.format(dim), 'r') as t1, open('test_h{}_type2_dep.txt'.format(dim), 'r') as t2, open('test_h{}_type3_dep.txt'.format(dim), 'r') as t3,  open(out_file, 'w') as out:
    for l0, l1, l2, l3 in zip(base, t1, t2, t3):

        pred_0, gold = l0.rstrip().split('\t')
        pred_1, _ = l1.rstrip().split('\t')
        pred_2, _ = l2.rstrip().split('\t')
        pred_3, _ = l3.rstrip().split('\t')
        pred_0 = pred_1.split(' ')[2:]
        pred_1 = pred_1.split(' ')[2:]
        pred_2 = pred_2.split(' ')[2:]
        pred_3 = pred_3.split(' ')[2:]
        gold = gold.split(' ')[2:]

        align, frame = get_af(' '.join(gold), test_dict)

        if (pred_0 == pred_1) and (pred_1 == pred_2) and (pred_2 == pred_3) and (pred_3 == pred_0):
            same += 1
            out.write('-----SAME-----'+'\n')
            output_line = 'baseline : ' + ' '.join(pred_0) + '\n' + 'type 1 : ' +' '.join(pred_1) + '\n' + 'type 2 : ' + ' '.join(pred_2) + '\n' + 'type 3 : ' + ' '.join(pred_3) + '\n' + 'gold tree : ' + ' '.join(gold) + '\n' + 'alignment : ' + align + '\n' + 'frame : ' + frame + '\n'
        else:
            diff += 1
            out.write('-----DIFF-----'+'\n')
            output_line = 'baseline : ' + ' '.join(pred_0) + '\n' + 'type 1 : ' +' '.join(pred_1) + '\n' + 'type 2 : ' + ' '.join(pred_2) + '\n' + 'type 3 : ' + ' '.join(pred_3) + '\n' + 'gold tree : ' + ' '.join(gold) + '\n' + 'alignment : ' + align + '\n' + 'frame : ' + frame + '\n'
            # print(output_line)
        out.write(output_line)
    out.write('--------------'+'\n')
    out.write(str(same) + ' identical outputs ' + str(diff) + ' different outputs' )
