import tqdm
import sys
from preprocess import *
# parse alignments and frames
def gen_dict(data_path, align_path, align_type):
    test_dict = {}

    with open(data_path+'_caps.txt', 'r') as cap, open(data_path+'_frames.txt', 'r') as frame, open(align_path+align_type+'.align', 'r') as align:
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
align_path = '../data/coco/VGNSL_split/alignments/test.'
none_dict = gen_dict(data_path, align_path, 'none')
all_dict = gen_dict(data_path, align_path, 'split_all')
verb_dict = gen_dict(data_path, align_path, 'split_verb')
noverb_dict = gen_dict(data_path, align_path, 'split_noverb')


same = 0
diff = 0


# generate comparison results
dim = sys.argv[1]
out_file = sys.argv[2]
out_dir = 'outputs/'
with open(out_dir+'test_h{}_3_none.txt'.format(dim), 'r') as t0, open(out_dir+'test_h{}_3_split_all.txt'.format(dim), 'r') as t1, open(out_dir+'test_h{}_3_split_verb.txt'.format(dim), 'r') as t2, open(out_dir+'test_h{}_3_split_noverb.txt'.format(dim), 'r') as t3,  open(out_dir+out_file, 'w') as out:
    for l0, l1, l2, l3 in zip(t0, t1, t2, t3):

        pred_0, gold, span_0 = l0.rstrip().split('\t')
        pred_1, _, span_1 = l1.rstrip().split('\t')
        pred_2, _, span_2 = l2.rstrip().split('\t')
        pred_3, _, span_3 = l3.rstrip().split('\t')
        pred_0 = pred_1.split(' ')[2:]
        pred_1 = pred_1.split(' ')[2:]
        pred_2 = pred_2.split(' ')[2:]
        pred_3 = pred_3.split(' ')[2:]
        gold = gold.split(' ')[2:]

        align_0, frame = get_af(' '.join(gold), none_dict)
        align_1, frame = get_af(' '.join(gold), all_dict)
        align_2, frame = get_af(' '.join(gold), verb_dict)
        align_3, frame = get_af(' '.join(gold), noverb_dict)

        if (pred_0 == pred_1) and (pred_1 == pred_2) and (pred_2 == pred_3) and (pred_3 == pred_0):
            same += 1
            out.write('-----SAME-----'+'\n')
        else:
            diff += 1
            out.write('-----DIFF-----'+'\n')

        output_line_0 = 'none : ' + ' '.join(pred_0) + '\n' + str(span_0) + '\n' + 'alignment : ' + align_0 + '\n'
        output_line_1 = 'split all : ' +' '.join(pred_1) + '\n' + str(span_1) + '\n' + 'alignment : ' + align_1 + '\n'
        output_line_2 = 'split verb : ' + ' '.join(pred_2) + '\n' + str(span_2) + '\n' + 'alignment : ' + align_2 + '\n'
        output_line_3 = 'split no verb : ' + ' '.join(pred_3) + '\n' + str(span_0) + '\n' + 'alignment : ' + align_3 + '\n'
        output_line_gold = 'gold tree : ' + ' '.join(gold) + '\n'
        output_line_frame =  'frame : ' + frame + '\n'

        out.write(output_line_0 + output_line_1 +output_line_2 + output_line_3 + output_line_gold + output_line_frame)
    out.write('--------------'+'\n')
    out.write(str(same) + ' identical outputs ' + str(diff) + ' different outputs' )
