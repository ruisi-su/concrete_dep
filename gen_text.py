import json
from typing import TextIO
import spacy
from spacy import displacy
import ast
from os import listdir
from os.path import isfile, join
from mscoco_ann import get_id, get_anns
import stanfordnlp

# USING SPACY PARSER
# nlp = spacy.load("en_core_web_sm")


# USING STANFORD NLP PARSER
stanfordnlp.download('en', force=True)
nlp = stanfordnlp.Pipeline()

# training annotations
train = json.load(open("train.json"))
imsitu = json.load(open("imsitu_space.json"))

NOUNS = imsitu["nouns"]
VERBS = imsitu["verbs"]

realized = 'simple_sentence_realization/realized_parts.tab'

h = train['glaring_215.jpg']['verb']
frames = train['glaring_215.jpg']['frames']

preds = json.load(open('examples_predictions/jumping_100.predictions'))

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
def mscoco_frame(path):
    # name vars
    im_name = 'mscoco'
    image_name = im_name + '.txt'
    relation_name = im_name + '_frame.txt'
    realized_name = im_name + '_realized.txt'

    preds = [f for f in listdir(path) if isfile(join(path, f))]

    with open(relation_name, 'w') as fr, open(image_name, 'w') as im, open(realized_name, 'w') as rl:
        for p in preds:
            file_name, ext = p.split('.')
            predFile = '{}/{}'.format(path,p)
            print(predFile)
            p_data = json.load(open(predFile))
            p_data = p_data[0]

            # write frame data
            h = p_data['verb']
            frames = p_data['frames']
            # counter = 0

            for f in frames:
                # write roles
                pair_h_r_t(h, f, fr)
                # new line
                fr.write('\n')

                # write image labels
                im.write(p + '\n')
                # counter
                # counter += 1

                # write captions
                img_name = file_name + '.jpg'
                print(img_name)
                ann = get_anns(get_id(img_name))
                rl.write(ann + '\n')

# mscoco_frame(preds)
path = 'coco_val'
# mscoco_frame(path)
############### Dep Parse ##############

# generate the dep text file
def gen_dep(in_file, out_file):
    with open(in_file, 'r') as f, open(out_file, 'w') as o:
        for l in f:
            l = l.rstrip()
            gen_dep_sementic(l, o)
            o.write('\n')

# doc = nlp("person adjusting fastening using hand at table.")
line = 'Player returning ball during volley at tennis match'
dep_out_file = 'mscoco_dep.txt'

# generate the dependency relations based on one line of the role relation entry
def gen_dep_line(input, file):
    # words = input.split('_')
    # doc = spacy.tokens.doc.Doc(nlp.vocab, words=words)
    # # run the standard pipeline against it
    # for name, proc in nlp.pipeline:
    #     doc = proc(doc)

    doc = nlp(input)

    for token in doc:
        if token.dep_ == 'ROOT':
            continue
        else:
            result = token.head.text + '_' + token.dep_ + '_' + token.text
            # print(token.text, token.dep_, [child for child in token.children])
            # file.write(result + '\t')
            print(result)

def gen_dep_sementic(sent, file):
    doc = nlp(sent)
    deps = doc.sentences[0].dependencies
    # results = []
    for d in deps:
        w1, r, w2 = d
        h = w1.text
        t = w2.text
        result = h + '_' + r + '_' + t
        # results.append(result)
        file.write(result + '\t')
        print(result)
    # return results
# print(gen_dep_sementic(line, dep_out_file))
gen_dep('mscoco_realized.txt', 'mscoco_dep.txt')
