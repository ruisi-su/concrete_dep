import utils
import preprocess
from collections import Counter
import argparse, sys

# deptrees = utils.read_conll(open(conllfile, 'r'))
# words, heads = next(deptrees)
#
#
# print(heads)
# gold_tree = '(NP (NP (NP (DT A) (NN man)) (PP (IN with) (NP (DT a) (JJ red) (NN helmet)))) (PP (IN on) (NP (NP (DT a) (JJ small) (NN moped)) (PP (IN on) (NP (DT a) (NN dirt) (NN road))))) (. .))'
# from VGNSL ground truth
# ground_truth = '( ( ( A man ) ( with ( a red helmet ) ) ) ( on ( ( a small moped ) ( on ( a dirt road ) ) ) ) . )'


# how many times is a word a head for a span of two words?
# how many times is a word a hea for the entire sentence?
# how many times is a word a head for intermediate spans (not the immediate head nor the root of the sentence)
def get_span_heads(gold_tree, heads, head_dict, pos_dict):

    action = preprocess.get_actions(gold_tree)
    tags, sent, sent_lower = preprocess.get_tags_tokens_lowercase(gold_tree)
    span, binary_actions, nonbinary_actions = utils.get_nonbinary_spans(action)
    tree_w_heads = utils.get_span2head(span, heads, gold_actions=action, gold_tags=tags)
    sent_l = len(sent)

    for (l, r) in tree_w_heads.keys():
        # print((l, r))
        span = sent_lower[l:r+1]
        head, pos = tree_w_heads[(l, r)]
        head_str = sent_lower[head]
        span_l = len(span)

        if head_str not in head_dict.keys():
            # print('adding %s' % head_str)
            # print(head_dict)
            count_dict = Counter({'immediate':0, 'intermediate':0, 'entire':0})
            head_dict[head_str] = count_dict
            pos_dict[head_str] = pos

        if span_l <= 3 and span_l > 1:
            # print('add to immediate' + str(span))
            head_dict[head_str]['immediate'] += 1
        elif span_l < sent_l and span_l > 3:
            head_dict[head_str]['intermediate'] += 1
        elif span_l == sent_l:
            head_dict[head_str]['entire'] += 1
        # print('%s \t %s' % (' '.join(span), head_str))
    return head_dict, pos_dict


def parse_heads(tree_file, conllx_file, head_dict, pos_dict):
    deptrees = utils.read_conll(open(conllx_file, 'r'))
    count = 0
    with open(tree_file, 'r') as trees:
        for gold_tree in trees:
            count += 1
            word, heads = next(deptrees)
            head_dict, pos_dict = get_span_heads(gold_tree, heads, head_dict, pos_dict)
    # print(len(head_dict))
    head_dict_filter = {}
    for head_c in head_dict.keys():
        total = sum(head_dict[head_c].values())
        if total != 0:
            head_dict_filter[head_c] = dict(head_dict[head_c])
            head_dict_filter[head_c]['total'] = total

    # print(head_dict_filter)
    return count, head_dict_filter, pos_dict

# tree_file = '../data/coco/VGNSL_split/test_trees.txt'
# conllx_file ='data/dep/test.conllx'

def main():
    # split type: all, test, train, dev
    parser = argparse.ArgumentParser()
    parser.add_argument('--make_count', action='store_true')
    parser.add_argument('--split_type', type=str)
    parser.add_argument('--count_file', type=str)
    args = parser.parse_args()

    if args.make_count:
        head_dict = {}
        pos_dict = {}
        tree_file = '../data/coco/VGNSL_split/{}_trees.txt'.format(args.split_type)
        conllx_file = 'data/dep/{}.conllx'.format(args.split_type)

        count, head_dict, pos_dict = parse_heads(tree_file, conllx_file, head_dict, pos_dict)

        head_dict_sorted = sorted(head_dict.items(), key=lambda h: h[1]['total'], reverse=True)
        for head in head_dict_sorted:
            word, hd = head
            print('{}\t{}\t{}\t{}\t{}\t{}'.format(word, hd['immediate'], hd['intermediate'], hd['entire'], hd['total'], pos_dict[word]))
        # print(count)
    else:
        with open(args.count_file, 'r') as count:
            for line in count:
                print(line)

if __name__ == "__main__":
    main()
