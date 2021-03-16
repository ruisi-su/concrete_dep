import tqdm
import sys
from preprocess import *
import argparse

# generate comparison results

parser = argparse.ArgumentParser(description="Parse arguments")
parser.add_argument('o1') #baseline
parser.add_argument('o2') #concrete
parser.add_argument('o3') # constraints
parser.add_argument('o4') # constraints
parser.add_argument("--align1", help="Specific alignment file to include")
parser.add_argument("--align2", help="Specific alignment file to include")
args = parser.parse_args()

# parse alignments and frames
def gen_dict(data_path, align_path, align_file):
    test_dict = {}

    with open(data_path+'_caps.txt', 'r') as cap, open(data_path+'_frames.txt', 'r') as frame, open(align_path+align_file, 'r') as align:
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
            if diff == diff.intersection(filter_words):
                a = ' '.join(dict[i]['alignment'])
                f = ' '.join(dict[i]['frame'])
                return (a, f)

    raise ValueError('Tree is not found in caption dictionary')


same = 0
diff = 0

out_dir = 'outputs/'

# gen dict
data_path = '../data/coco/VGNSL_split/test'
align_path = '../data/coco/VGNSL_split/alignments/'
compare_rule = True


# if args.align:
dict_t0 = gen_dict(data_path, align_path, args.align1)
dict_t1 = gen_dict(data_path, align_path, args.align2)

with open(args.o1, 'r') as t0, open(args.o2, 'r') as t1, open(args.o3, 'r') as t2, open(args.o4, 'r') as t3:

    for l0, l1, l2, l3 in zip(t0, t1, t2, t3):
    # for l0, l1, l2 in zip(t0, t1, t2):
    # for l0, l3 in zip(t0, t3):

        pred_0, gold, _ = l0.rstrip().split('\t')
        pred_1, _, _ = l1.rstrip().split('\t')
        pred_2, _, _ = l2.rstrip().split('\t')
        pred_3, _, _ = l3.rstrip().split('\t')
        pred_0 = pred_0.split(' ')[2:]
        pred_1 = pred_1.split(' ')[2:]
        pred_2 = pred_2.split(' ')[2:]
        pred_3 = pred_3.split(' ')[2:]
        gold = gold.split(' ')[2:]

        # dict_t1 = gen_dict(data_path, align_path, align_t1, eqn_type)

        align_0, frame = get_af(' '.join(gold), dict_t0)
        align_1, _ = get_af(' '.join(gold), dict_t1)
        # align_2, frame = get_af(' '.join(gold), verb_dict)
        # align_3, frame = get_af(' '.join(gold), noverb_dict)

        if (pred_0 == pred_1 == pred_2 == pred_3):
            same += 1
            print('-----SAME-----')
        else:
            diff += 1
            print('-----DIFF-----')

        print('baseline : ' + ' '.join(pred_0))

        print('output 1 : ' + ' '.join(pred_1))

        print('output 2 : ' + ' '.join(pred_2))
        print('align : ' + align_0)

        print('output 3 : ' + ' '.join(pred_3))
        print('align : ' + align_1)

        print('gold tree : ' + ' '.join(gold))
        print('frame : ' + frame)
        # if args.align_file != '':
        #     output_line_frame =  'frame : ' + frame + '\n'
        #     output_line_align = 'align : ' + align_0 + '\n'
        #     # out.write(output_line_0 + output_line_1 + output_line_gold + output_line_frame)
        #     print(output_line_3 + output_line_0 + output_line_1 +output_line_2 + output_line_gold + output_line_frame + output_line_align)
        # else:
        #     print(output_line_3 + output_line_0 + output_line_1 +output_line_2 + output_line_gold)

    print('--------------')
    print(str(same) + ' identical outputs ' + str(diff) + ' different outputs' )
