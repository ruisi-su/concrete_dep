import tqdm
import sys
from preprocess import *
# parse alignments and frames
def gen_dict(data_path, align_path, align_type, eqn_type):
    test_dict = {}

    with open(data_path+'_caps.txt', 'r') as cap, open(data_path+'_frames.txt', 'r') as frame, open(align_path+align_type+'.'+eqn_type+'.align', 'r') as align:
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


same = 0
diff = 0


# generate comparison results
dim = sys.argv[1]
cons_type = sys.argv[2]
align_t0 = sys.argv[3]
# align_t1 = sys.argv[4]

eqn_type = sys.argv[4]
out_file = sys.argv[5]

# align_t0 = 'split_all'
# align_t1 = 'split_noverb'

out_dir = 'outputs/'

# gen dict
data_path = '../data/coco/VGNSL_split/test'
align_path = '../data/coco/VGNSL_split/alignments/test.'
# none_dict = gen_dict(data_path, align_path, 'none', eqn_type)
# all_dict = gen_dict(data_path, align_path, 'split_all', eqn_type)
# verb_dict = gen_dict(data_path, align_path, 'split_verb', eqn_type)
# noverb_dict = gen_dict(data_path, align_path, 'split_noverb', eqn_type)
compare_rule = True

with open(out_dir+'test_h{}_{}_{}_{}.txt'.format(dim, 1, align_t0, eqn_type), 'r') as t0, open(out_dir+'test_h{}_{}_{}_{}.txt'.format(dim, 2, align_t0, eqn_type), 'r') as t1, open(out_dir+'test_h{}_{}_{}_{}.txt'.format(dim, 3, align_t0, eqn_type), 'r') as t2, open(out_dir+'test_h{}_base_span.txt'.format(dim), 'r') as t3, open(out_dir+out_file, 'w') as out:

    for l0, l1, l2, l3 in zip(t0, t1, t2, t3):
    # for l0, l1, l2 in zip(t0, t1, t2):
    # for l0, l1 in zip(t0, t1):

        pred_0, gold, span_0 = l0.rstrip().split('\t')
        pred_1, _, span_1 = l1.rstrip().split('\t')
        pred_2, _, span_2 = l2.rstrip().split('\t')
        pred_3, _, span_3 = l3.rstrip().split('\t')
        pred_0 = pred_0.split(' ')[2:]
        pred_1 = pred_1.split(' ')[2:]
        pred_2 = pred_2.split(' ')[2:]
        pred_3 = pred_3.split(' ')[2:]
        gold = gold.split(' ')[2:]

        dict_t0 = gen_dict(data_path, align_path, align_t0, eqn_type)
        # dict_t1 = gen_dict(data_path, align_path, align_t1, eqn_type)

        align_0, frame = get_af(' '.join(gold), dict_t0)
        # align_1, frame = get_af(' '.join(gold), dict_t1)
        # align_2, frame = get_af(' '.join(gold), verb_dict)
        # align_3, frame = get_af(' '.join(gold), noverb_dict)

        if (pred_0 == pred_1 == pred_2 == pred_3):
            # print(pred_0)
            # print(pred_1)
             # and (pred_1 == pred_2) and (pred_2 == pred_3) and (pred_3 == pred_0):
            same += 1
            out.write('-----SAME-----'+'\n')
        else:
            diff += 1
            out.write('-----DIFF-----'+'\n')

        # output_line_0 = align_t0 + ' : ' + ' '.join(pred_0) + '\n' + str(span_0) + '\n' + 'alignment : ' + align_0 + '\n'
        # output_line_1 = align_t1 + ' : ' +' '.join(pred_1) + '\n' + str(span_1) + '\n' + 'alignment : ' + align_1 + '\n'
        # output_line_2 = 'split verb : ' + ' '.join(pred_2) + '\n' + str(span_2) + '\n' + 'alignment : ' + align_2 + '\n'
        # output_line_3 = 'split no verb : ' + ' '.join(pred_3) + '\n' + str(span_0) + '\n' + 'alignment : ' + align_3 + '\n'
        output_line_0 = 'rule 1 : ' + ' '.join(pred_0) + '\n' + str(span_0) + '\n'
        output_line_1 = 'rule 2 : ' + ' '.join(pred_1) + '\n' + str(span_1) + '\n'
        output_line_2 = 'rule 3 : ' + ' '.join(pred_2) + '\n' + str(span_2) + '\n'
        output_line_3 = 'base : ' + ' '.join(pred_3) + '\n' + str(span_3) + '\n'
        # output_line_2 = 'rule 3 : ' + ' '.join(pred_2) + '\n' + str(span_2) + '\n'

        output_line_gold = 'gold tree : ' + ' '.join(gold) + '\n'
        output_line_frame =  'frame : ' + frame + '\n'
        output_line_align = 'align : ' + align_0 + '\n'

        # out.write(output_line_0 + output_line_1 + output_line_gold + output_line_frame)
        out.write(output_line_3 + output_line_0 + output_line_1 +output_line_2 + output_line_gold + output_line_frame + output_line_align)
        # out.write(output_line_0 + output_line_1 +output_line_2 + output_line_gold + output_line_frame)

    out.write('--------------'+'\n')
    out.write(str(same) + ' identical outputs ' + str(diff) + ' different outputs' )
