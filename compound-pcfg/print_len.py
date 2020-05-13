import utils
import preprocess

conllfile = '/Users/sisi/MultimodalGI/data/coco/mscoco/dep/train.conllx'
textfile = '/Users/sisi/MultimodalGI/data/coco/mscoco/unfiltered/train-val-test_gold.filter.txt'
deptrees = utils.read_conll(open(conllfile, 'r'))
dep_list = list(deptrees)
print(len(dep_list))
count = 0
ind = 0
for i, tree in enumerate(open(textfile, 'r')):
        print(ind)
        words, heads = dep_list[ind]
        tree = tree.strip()
        # print(tree)
        tags, sent, sent_lower = preprocess.get_tags_tokens_lowercase(tree)
        if words != sent:
            # words, heads = next(deptrees)
            print("Data mismatch, got {} in {}, but {} in {}.".format(sent, textfile, words, conllfile))
        else:
            ind += 1
