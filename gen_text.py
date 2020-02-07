import json
from typing import TextIO
import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")

# training annotations
train = json.load(open("train.json"))
imsitu = json.load(open("imsitu_space.json"))

NOUNS = imsitu["nouns"]
VERBS = imsitu["verbs"]
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

h = train['clinging_250.jpg']['verb']
frames = train['clinging_250.jpg']['frames']

###############Generate Verb_Role_Noun txt##############
def gen_h_r_t(h: str, r: str, ts: [], write_file: TextIO) -> []:
    # result = []
    for t in ts:
        h_r_t = h + '_' + r + '_' + t
        write_file.write(h_r_t + '\n')
        # print('writing')
        # result.append(h_r_t)
    # return result

check1 = ['h_agent_koala', 'h_agent_koala bear', 'h_agent_kangaroo bear', 'h_agent_native bear', 'h_agent_Phascolarctos cinereus']
ts = ['koala', 'koala bear', 'kangaroo bear', 'native bear', 'Phascolarctos cinereus']
# assert(gen_h_r_t('h', 'agent', ts) == check1)


def pair_h_r_ts(h: str, frame: dict,  write_file: TextIO) -> []:
    # result = []
    for f in frame.keys():
        if frame[f] != '':
            n_id = frame[f]
            ns = NOUNS[n_id]['gloss']
            # print('role ' + f + '\n' + 'ns ' + str(ns))
            r_ts = gen_h_r_t(h, f, ns, write_file)
            # result.extend(r_ts)
    # return result
check2 = ['clinging_clungto_arm', 'clinging_agent_koala', 'clinging_agent_koala bear', 'clinging_agent_kangaroo bear', 'clinging_agent_native bear', 'clinging_agent_Phascolarctos cinereus']
# assert(pair_h_r_ts(h, frames[0]) == check2)

def frames_h_r_ts(h: str, frames:[], write_file: TextIO):
    # result = []
    for f in frames:
        # result.extend(pair_h_r_ts(h, f))
        pair_h_r_ts(h, f, write_file)
    # return result

# print(frames_h_r_ts(h, frames))

# using train.json frame data
def gen_frame_based(train, image_name, frame_name):
    # write image labels to text file
    with open(image_name, 'w') as im, open(frame_name, 'w') as fr:
        # write image names
        for k in train.keys():
            im.write(k + '\n')
            # fr.write(k + '\n')
            # write frame data:
            # for example: h: throw r: agent t: kid
            # h_r_t
            h = train[k]['verb']
            frames = train[k]['frames']
            frames_h_r_ts(h, frames, fr)

image_name = 'image.txt'
frame_name = 'image_frame.txt'
# gen_frame_based(train, image_name, frame_name)

###############Realize Sentences##############
# remove frequency counts and subparts, filter out entries containing only the verbs
def clean_realized(in_file, out_file):

    with open(in_file, 'r') as rl, open(out_file, 'w') as rc:
        for l in rl:
            count, realized_parts, verb, sub = l.split('\t')
            rp = realized_parts.split('_')
            if len(rp) > 1:
                line = realized_parts + '\t' + verb
                rc.write(line + '\n')
            # print(realized_parts)
realized = 'simple_sentence_realization/realized_parts.tab'
realized_clean = 'realized_clean.txt'
# clean_realized(realized, realized_clean)

###############Dep Parse##############

# generate the dep text file
# h_dep_t: throw_nsubj_kid
def gen_dep(in_file, out_file):
    with open(in_file, 'r') as f, open(out_file, 'w') as o:
        for l in f:
            realize, verb = l.split('\t')
            # print(realize)
            gen_dep_line(realize, o)

# gen_dep(realized_clean)


# doc = nlp("person adjusting fastening using hand at table.")
line = 'person_adjusting_fastening_using_hand_at_table'
dep_out_file = 'image_dep.txt'
# displacy.serve(doc, style="dep")
# generate the dependency relations based on one line of the role relation entry
def gen_dep_line(input, file):
    words = input.split('_')
    doc = spacy.tokens.doc.Doc(nlp.vocab, words=words)
    for name, proc in nlp.pipeline:
        doc = proc(doc)

    for token in doc:
        result = token.head.text + '_' + token.dep_ + '_' + token.text
        # print(token.text, token.dep_, [child for child in token.children])
        # print(printing)
        file.write(result + '\n')

gen_dep(realized_clean, dep_out_file)
