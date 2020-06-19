import utils
import preprocess
from collections import Counter
from operator import itemgetter
# tree = '(NP (NP (NN Doorway) (NN view)) (PP (IN of) (NP (NP (DT a) (NN kitchen)) (PP (IN with) (NP (DT a) (NN sink) (, ,) (NN stove) (, ,) (NN refrigerator) (CC and) (NN pantry))))) (. .))'

def head_count(tree, heads, split, count_head, count_occur):

    action = preprocess.get_actions(tree)
    tags, sent, sent_lower = preprocess.get_tags_tokens_lowercase(tree)

    # parse occurrence
    for word in sent_lower:
        count_occur[word] += 1
    span, _, _ = utils.get_nonbinary_spans(action)
    gold_sig = utils.get_span2head(span, heads, action, tags)

    for span, (head, label) in gold_sig.items():
     if(span[0] == span[1]):
       gold_sig[span] = (head, utils.PT2ID[label])
     else:
       f = lambda x : x[:x.find('-')] if x.find('-') != -1 else x
       g = lambda y : y[:y.find('=')] if y.find('=') != -1 else y
       gold_sig[span] = (head, utils.NT2ID[f(g(label))])
       count_head[sent_lower[head]] += 1

    return count_head, count_occur


def find_root(words, heads):
    for i, h in enumerate(heads):
        if h == 0:
            return words[i].lower()

def parse_split(split, count_head, count_root, count_occur):
    with open('../data/coco/VGNSL_split/{}_trees.txt'.format(split), 'r') as trees:
        conllfile="data/dep/{}.conllx".format(split)
        deptrees = utils.read_conll(open(conllfile, 'r'))
        # dep_list = list(deptrees)
        for line in trees:
            tree = line.strip()
            words, heads = next(deptrees)
            root = find_root(words, heads)
            count_head, count_occur = head_count(tree, heads, split, count_head, count_occur)
            count_root[root] += 1
    return count_head, count_root, count_occur

def get_concreteness():
    con = {}
    with open('concreteness.txt', 'r') as c:
        for line in c:
            line = line.strip().split(' ')
            if len(line) < 2:
                continue
            # print(line)
            word = line[0]
            score = line[1]
            con[word] = score
    return con

def concreteness_occurrance(type):
    concrete_dict = get_concreteness()

    count_head = Counter()
    count_root = Counter()
    count_occur = Counter()

    count_head, count_root, count_occur = parse_split('dev', count_head, count_root, count_occur)
    count_head, count_root, count_occur = parse_split('test', count_head, count_root, count_occur)
    # check there is one root for every entry
    assert(sum(count_root.values()) == 10000)
    if type == 'head':
        count = count_head
    elif type == 'root':
        count = count_root

    result = {}
    # normalize head occurrence
    for key in count:
        # total number of times this word appears in the text
        occurrence = count_occur[key]
        # normalize the head count by the total time it occurs
        result[key] = count[key] / occurrence
    with open('concrete_count_{}.txt'.format(type), 'w') as cc:
        cc.write('word\tpercent\tconcreteness\tcount_{}\tcount_occur\n'.format(type))
        for (word, freq) in sorted(result.items(), key=itemgetter(1), reverse=True):
            if word in concrete_dict.keys():
                # total number of times this word appears in the text
                # normalize the head count by the total time it occurs
                assert(freq == count[word] / count_occur[word])
                cc.write(word + '\t' + str(round(freq, 3)) + '\t' + concrete_dict[word] + '\t' + str(count[word]) + '\t' + str(count_occur[word]) + '\n')

concreteness_occurrance('root')
concreteness_occurrance('head')

# print(c.most_common(10))
