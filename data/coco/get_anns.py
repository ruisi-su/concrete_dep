#!/usr/bin/env python
# coding: utf-8

#from pycocotools.coco import COCO
import numpy as np
import json
import spacy
from spacy.lang.en import English
from spacy.tokenizer import Tokenizer
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import compile_infix_regex

import random
import re
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--start', type = int,default=0,help='start idx')
parser.add_argument('--end', type = int, default=413915,help='end idx')
args = parser.parse_args()
nlp = spacy.load("en_core_web_sm")

dataType=['train2014','val2014']
# annFile='{}/annotations/instances_{}.json'.format(dataDir,dataType)
annFile_train='annotations/instances_{}.json'.format(dataType[0])
annFile_val='annotations/instances_{}.json'.format(dataType[1])
splitFolder = './VGNSL_split/'
splitFile = 'dataset_coco.json'
dataDir = '.'

with open(splitFile) as datafile:
        data = json.load(datafile)
        IMAGES = data['images']

def get_image_id(splitType, start_idx=0, end_idx=5000):
    im_file = splitType + '_ids_' + str(start_idx) + '.txt'
    log_file = splitType + '_log_' + str(start_idx) + '.txt'
    # im_file = splitType + '_ids'  + '.txt'
    # log_file = splitType + '_log' + '.txt'
    json_file = 'data_' + splitType + '.json'
    # get the caps from text
    vgnsl_caps = []

    with open(splitFolder + splitType + '_caps.txt', 'r') as cap_file:
        for i, c in enumerate(cap_file):
            if i < start_idx or i >= end_idx:
                continue
            c = c.strip().lower()
            # manually replacing ``, periods, and apostrophes
            c = c.replace("``", "\"").replace('.','').replace(" '","'").replace("**rr**",")").replace("**ll**", "(")
            vgnsl_tok = [token.text for token in nlp(c)]
            if ' ' in vgnsl_tok:
                vgnsl_tok.remove(' ')
            vgnsl_caps.append((c, vgnsl_tok))

    if splitType == 'dev':
        splitType = 'val'

    coco_set = []
    for im in IMAGES:
        if im['split'] == splitType:
            sents = im['sentences']
            tokens = [sent['tokens'] for sent in sents]
            raws = [sent['raw'].replace('.','').strip().lower() for sent in sents]
            # coco_set.append((im['cocoid'], tokens))
            raws_tokens = []
            for raw in raws:
                coco_token = [token.text for token in nlp(raw)]
                if ' ' in coco_token:
                    coco_token.remove(' ')
                raws_tokens.append(coco_token)
            assert(len(raws_tokens) == len(raws))
            coco_set.append((im['cocoid'], raws, tokens, raws_tokens))

    with open(json_file, "w") as write_file:
        json.dump(coco_set, write_file)

    count = 0
    count_miss = 0

    for idx, vgnsl in enumerate(vgnsl_caps):
        (c, vgnsl_tok) = vgnsl
        vgnsl_list = c.split()
        if ' ' in vgnsl_list:
            vgnsl_list.remove(' ')
        found = False
        for (cocoid, raws, tokens, raws_tokens) in coco_set:
            for raw, token, raw_token in zip(raws, tokens, raws_tokens):
                raw_split = raw.split()
                if ' ' in raw_split:
                    raw_split.remove(' ')
                # string comparison and VGNSL splits vs. tokens
                if (raw == c) or (vgnsl_list == token) or (vgnsl_list == raw_split):
                    count += 1
                    found = True
                    break
                # regex(vgnsl) vs. regex(coco)
                # coco_regex = re.sub("[^a-z-A-Z-0-9' ]+", '', item)
                # if (vgnsl_regex == coco_regex) or (vgnsl_regex.split() == coco_regex.split()):
                #     count += 1
                #     found = True
                #     break
                # VGNSL split vs. tokenize(coco)
                # coco_list = [token.text for token in nlp(raw)]
                if (raw_token == vgnsl_list):
                    count += 1
                    found = True
                    break
                # tokenize(VGNSL) vs. tokenize(coco)
                if (raw_token == vgnsl_tok) or (token == vgnsl_tok):
                    count += 1
                    found = True
                    break
            if found:
                with open(im_file, 'a') as imfile:
                    imfile.write(str(cocoid) + '\n')
                break
        if not found:
            count_miss += 1
            with open(log_file, 'a') as logfile:
                logfile.write(str(idx) + '\t' + str(vgnsl_list) + '\t' + c + '\n')
                print('could not found : ' + str(idx) + str(vgnsl_list) + ' ' + c)

def write_data(splitType, coco_im, coco_cap, dataIds):
    capfile = dataDir + '/' + splitType + '_cap.txt'
    imfile = dataDir + '/' + splitType + '_name.txt'
    count = 0
    with open(capfile, 'w') as cap, open(imfile, 'w') as name:
        for dataId in dataIds[splitType]:
            img = coco_im.loadImgs(dataId)[0]
            annIds = coco_cap.getAnnIds(imgIds=img['id']);
            anns = coco_cap.loadAnns(annIds)
            caps = anns[random.randint(0,len(anns)-1)]['caption']
            caps = caps.strip().lower().replace('.', '').replace('\n','')
#             caps = get_anns(anns) FILTER
            if caps is None or len(caps) < 1:
                continue
            else:
                filename = img['file_name']
                cap.write(caps + '\n')
                name.write(filename + '\n')
                count += 1
    print(count)

def get_anns(anns):
    for ann in anns:
        cap = ann['caption']
        cap = cap.replace('.', '')
        action = has_action(cap)
        if action:
            return cap
    return None

def has_action(ann):
    doc = nlp(ann)
    for token in doc:
        if token.dep_ == 'ROOT' and token.head.pos_ == 'VERB':
            return True
        elif token.dep_ == 'ROOT':
            return 'VERB' in [child.pos_ for child in token.children]
    return False

if __name__ == '__main__':
    get_image_id('train', args.start, args.end)
    # get_image_id('test')

    # coco = "A man is riding an elephant with and \"I love NY\" sign."
    # vgnsl = "**LL** A man is riding an elephant with and `` I love NY `` sign ."
    # coco = re.sub("[^a-z-A-Z' ]+", '', coco.lower())
    # vgnsl = re.sub("[^a-z-A-Z' ]+", '', vgnsl.lower())
    #
    # # ss = re.sub("[a-zA-Z0-9\-]+", '',ss)
    # c_tok = [token.text for token in nlp(vgnsl.strip())]
    # print(c_tok)
    # print(coco.split() == vgnsl.split())
