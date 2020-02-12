import json
from typing import TextIO
import spacy
from spacy import displacy
import ast

nlp = spacy.load("en_core_web_sm")

# training annotations
train = json.load(open("train.json"))
imsitu = json.load(open("imsitu_space.json"))

NOUNS = imsitu["nouns"]
VERBS = imsitu["verbs"]

realized = 'simple_sentence_realization/realized_parts.tab'


#
# verbs["clinging"]

# {u'abstract': u'an AGENT clings to the CLUNGTO at a PLACE',
#  u'def': u'stick to',
#  u'framenet': u'Retaining',
#  u'order': [u'agent', u'clungto', u'place'],
#  u'roles': {
#   u'agent': {u'def': u'The entity doing the cling action',u'framenet': u'agent'},
#   u'clungto': {u'def': u'The entity the AGENT is clinging to',u'framenet': u'theme'},
#   u'place': {u'def': u'The location where the cling event is happening',u'framenet': u'place'}
#  }
# }

# NOUNS["n02129165"]

#{u'def': u'large gregarious predatory feline of Africa and India having a tawny coat with a shaggy mane in the male',
# u'gloss': [u'lion', u'king of beasts', u'Panthera leo']}

#{u'frames': [{u'agent': u'n01882714', u'clungto': u'n05563770', u'place': u''},
#  {u'agent': u'n01882714', u'clungto': u'n05563770', u'place': u''},
#  {u'agent': u'n01882714', u'clungto': u'n00007846', u'place': u''}],
# u'verb': u'clinging'}

h = train['glaring_215.jpg']['verb']
frames = train['glaring_215.jpg']['frames']


###############Realize Sentences##############

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
# subparts = {'verb': 'glowing', 'place': 'n04105893'}
# in_list = realized_dict(realized)

# print(get_realized(in_list, subparts))


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
            # result += hrt+'\t'
    # return result
# check2 = 'glaring_place_sidewalk	glaring_agent_man'

# # verb - frames
# def frames_h_r_ts(h: str, frames:[], write_file: TextIO):
#     result = []
#     for f in frames:
#         # result.append(pair_h_r_ts(h, f))
#         # pair_h_r_ts(h, f)
#
#         write_file.write(pair_h_r_ts(h, f) + '\t')
#     write_file.write('\n')
#     # return result
#
# # print(frames_h_r_ts(h, frames))

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

###############Dep Parse##############

# generate the dep text file
def gen_dep(in_file, out_file):
    with open(in_file, 'r') as f, open(out_file, 'w') as o:
        for l in f:
            gen_dep_line(l, o)
            # o.write('\n')

# doc = nlp("person adjusting fastening using hand at table.")
line = 'man_glaring_at_sidewalk'
dep_out_file = 'frame_dep.txt'
# displacy.serve(doc, style="dep")
# generate the dependency relations based on one line of the role relation entry
def gen_dep_line(input, file):
    words = input.split('_')
    doc = spacy.tokens.doc.Doc(nlp.vocab, words=words)
    # run the standard pipeline against it
    for name, proc in nlp.pipeline:
        doc = proc(doc)

    for token in doc:
        if token.dep_ == 'ROOT':
            continue
        else:
            result = token.head.text + '_' + token.dep_ + '_' + token.text
            # print(token.text, token.dep_, [child for child in token.children])
            file.write(result + '\t')
            print(result)

# gen_dep_line(line, dep_out_file)

gen_dep('image_realized.txt', 'image_dep.txt')
