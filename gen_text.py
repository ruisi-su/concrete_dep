import json
from typing import TextIO
import spacy
from spacy import displacy
import ast
from os import listdir
from os.path import isfile, join
from mscoco_ann import get_id, get_anns
import stanfordnlp
import argparse
import utils

parser = argparse.ArgumentParser()
parser.add_argument('--parser', default='spacy', help='using spacy or stanfordnlp parser')
parser.add_argument('--type', default='imagename', help='generate the type of file')

args = parser.parse_args()

# training annotations
train = json.load(open("train.json"))
imsitu = json.load(open("imsitu_space.json"))

NOUNS = imsitu["nouns"]
VERBS = imsitu["verbs"]
realized = 'simple_sentence_realization/realized_parts.tab'

# h = train['glaring_215.jpg']['verb']
# frames = train['glaring_215.jpg']['frames']
#
# preds = json.load(open('examples_predictions/jumping_100.predictions'))

############### Realize Sentences ##############

# return a list object for future usage
def realized_dict(in_file, in_verb):
    sent_list = []
    with open(in_file, 'r') as rl:
        for l in rl:
            count, realized_parts, verb, sub = l.split('\t')
            if in_verb == verb:
                sent_dict = {}
                sent_dict['phrase'] = realized_parts
                sent_dict['verb'] = verb
                sent_dict['subparts'] = sub

                sent_list.append(sent_dict)
    return sent_list

def get_realized(in_list, subparts):
    for l in in_list:
        realized_parts = l['phrase']
        sub = l['subparts']
        sub = ast.literal_eval(sub)
        rp = realized_parts.split('_')
        if sub == subparts:
            return realized_parts

realized_clean = 'frame_realized.txt'
subparts = {'verb': 'glaring', 'agent': 'n10287213', 'place': 'n08613733'}

############### Generate Verb_Role_Noun txt ##############

# verb - frame
def pair_h_r_t(h: str, frame: dict, write_file: TextIO) -> []:
    # result = ''
    for f in frame.keys():
        if frame[f] != '':
            n_id = frame[f]
            ns = NOUNS[n_id]['gloss']
            # first of gloss
            n = ns[0]

            hrt = h + '_' + f + '_' + n
            write_file.write(hrt + '\t')

# using train.json frame data
def gen_frame_based(train):
    # name vars
    im_name = 'image'
    image_name = im_name + '.txt'
    relation_name = im_name + '_frame.txt'
    realized_name = im_name + '_realized.txt'

    # write image labels to text file
    with open(dep_name, 'w') as dp, open(image_name, 'w') as im, open(realized_name, 'w') as rl:
        # write image names
        for k in train.keys():
            # fr.write(k + '\n')
            # write frame data:
            # for example: h: throw r: agent t: kid
            # h_r_t
            h = train[k]['verb']
            frames = train[k]['frames']
            counter = 0
            realized_list = realized_dict(realized, h)

            for f in frames:
                # write roles
                pair_h_r_t(h, f, fr)
                # new line
                fr.write('\n')

                # write image labels
                im.write(k + '\t' + str(counter) + '\n')
                # counter
                counter += 1

                # write realized sent
                # remove empty entries
                sub = {k: v for k, v in f.items() if v != ''}
                sub['verb'] = h
                # find the phrase in realized parts
                rs = get_realized(realized_list, sub)
                print(rs)
                rl.write(rs + '\n')

# gen_frame_based(train)
def mscoco_frame(path, type):
    # name vars
    im_name = 'mscoco'
    image_name = im_name + '.txt'
    relation_name = im_name + '_frame.txt'
    realized_name = im_name + '_realized1.txt'

    preds = [f for f in listdir(path) if isfile(join(path, f))]
    #
    # if type == 'all':
    #     with open(relation_name, 'w') as fr, open(image_name, 'w') as im, open(realized_name, 'w') as rl:
    for p in preds:
        file_name, ext = p.split('.')
        predFile = '{}/{}'.format(path,p)
        print(predFile)
        p_data = json.load(open(predFile))
        p_data = p_data[0]
        frames = p_data['frames']
        h = p_data['verb']
        if type == 'all':
            with open(relation_name, 'a') as fr, open(image_name, 'a') as im, open(realized_name, 'a') as rl:
                # counter = 0
                for f in frames:
                    # write roles
                    pair_h_r_t(h, f, fr)
                    # new line
                    fr.write('\n')

                    # write image labels
                    im.write(p + '\n')

                    # write captions
                    img_name = file_name + '.jpg'
                    print(img_name)
                    ann = get_anns(get_id(img_name))
                    rl.write(ann + '\n')
        elif type == 'frame':
            with open(relation_name, 'a') as fr:
                for f in frames:
                    # write roles
                    pair_h_r_t(h, f, fr)
                    # new line
                    fr.write('\n')
        elif type == 'realized':
            with open(realized_name, 'a') as rl:
                for f in frames:
                    # write captions
                    img_name = file_name + '.jpg'
                    print(img_name)
                    ann = get_anns(get_id(img_name))
                    rl.write(ann + '\n')
        elif type == 'imagename':
            with open(image_name, 'a') as im:
                for f in frames:
                    # write image labels
                    im.write(p + '\n')
        else:
            raise NotImplementedError

# mscoco_frame(preds)
# mscoco_frame(path)
############### Dep Parse ##############

# generate the dep text file
def gen_dep(in_file, out_file, type):
    # set parser
    if args.parser == 'spacy':
        nlp = spacy.load("en_core_web_sm")
    elif args.parser == 'stanfordnlp':
        stanfordnlp.download('en', force=True)
        nlp = stanfordnlp.Pipeline()

    with open(in_file, 'r') as f, open(out_file, 'w') as o:
        for l in f:
            l = l.rstrip()
            sents = l.split('\t')
            for s in sents:
                print(s)
                if type == 'spacy':
                    gen_dep_line(s, o, nlp)
                else:
                    gen_dep_sementic(s, o, nlp)
            o.write('\n')

# generate the dependency relations based on one line of the role relation entry
def gen_dep_line(input, file, nlp):
    # words = input.split('_')
    # doc = spacy.tokens.doc.Doc(nlp.vocab, words=words)
    # # run the standard pipeline against it
    # for name, proc in nlp.pipeline:
    #     doc = proc(doc)

    doc = nlp(input)
    whitelist = {'pobj', 'dobj', 'nsubj'}
    results = []
    # for token in doc:
    for token in doc.noun_chunks:
        # if token.dep_ == 'ROOT':
        # if token.root.dep_ == 'ROOT':
        #     continue
        if token.root.dep_ in whitelist:
            result = token.root.head.text + '_' + token.root.dep_ + '_' + token.root.text
            # result = token.head.text + '_' + token.dep_ + '_' + token.text
            # print(token.text, token.dep_, [child for child in token.children])
            results.append(result)
            # print(result)
        else:
            continue
    old = len(results)
    results = utils.unique(results)
    new = len(results)
    print('old len: ' + str(old) + ' new len: ' + str(new))
    for result in results:
        file.write(result + '\t')

def gen_dep_sementic(sent, file, nlp):
    doc = nlp(sent)
    deps = doc.sentences[0].dependencies
    # ignore = {'punct', 'det', 'root'}
    whitelist = {'obl', 'obj', 'nsubj', 'subj', 'iobj'}
    results = []
    for d in deps:
        w1, r, w2 = d
        h = w1.text
        t = w2.text
        if r in whitelist:
            result = h + '_' + r + '_' + t
            results.append(result)
        else:
            continue
    results = utils.unique(results)
    for result in results:
        file.write(result + '\t')
        print(result)

    # return results
# print(gen_dep_sementic(line, dep_out_file))
# gen_dep('mscoco_realized.txt', 'mscoco_dep.txt')


def main(args):
    data_path = 'data/mscoco/'
    mscoco_path = 'coco_val'

    # set type to generate
    if args.type == 'imagename':
        mscoco_frame(mscoco_path, 'imagename')
    elif args.type == 'realized':
        mscoco_frame(mscoco_path, 'realized')
    elif args.type == 'frame':
        mscoco_frame(mscoco_path, 'frame')
    elif args.type == 'all':
        mscoco_frame(mscoco_path, 'all')
    elif args.type == 'dep':
        gen_dep(data_path+'mscoco_realized.txt', data_path+'mscoco_dep_sem_short.txt', args.parser)
    else:
        raise NotImplementedError
    # else:
    #     raise NotImplementedError
    # mscoco_frame(path)

if __name__ == '__main__':
    main(args)
