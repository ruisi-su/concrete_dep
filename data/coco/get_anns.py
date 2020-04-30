#!/usr/bin/env python
# coding: utf-8

#from pycocotools.coco import COCO
import numpy as np
# from nltk.tokenize import ToktokTokenizer
# toktok = ToktokTokenizer()

import json
import spacy
# nlp = spacy.load("en_core_web_sm")
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
nlp = English()
# Create a blank Tokenizer with just the English vocab
tokenizer = Tokenizer(nlp.vocab)
import random
import re
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--start', type = int,default=0,help='start idx')
parser.add_argument('--end', type = int, default=413915,help='end idx')
args = parser.parse_args()

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
    captions = []
    im_file = splitType + '_ids_' + str(start_idx) + '.txt'
    log_file = splitType + '_log_' + str(start_idx) + '.txt'
    # get the caps from text
    with open(splitFolder + splitType + '_caps.txt', 'r') as cap_file:
        for i, c in enumerate(cap_file):
            if i < start_idx or i >= end_idx:
                continue
#             c = c.replace("**LL** ", '(').replace(" **RR**",')').lower()
#             c = c.strip('\n').replace('.', '').replace(',',' ').replace('-', ' ').replace('/', ' ').replace(":", "").lower()
#             c = c.replace("``", "").replace(";", "")
#             # manual replacement
            c = c.replace(" 's", "s").replace(" 're", "re").replace(" n't", "nt").replace(" 'd", "d")
            c = c.replace('can not', 'cannot')
#             c = c.replace("# ", '#')
#             c = c.replace("$ ", "$")
            c = c.replace('1950s', '1950 s')
            c = c.replace(" 'd", "'d")
            # manual train
            c = re.sub('[^A-Za-z0-9]+', ' ', c.lower())
            captions.append(c)

    if splitType == 'dev':
        splitType = 'val'

    coco_set = []
    for im in IMAGES:
        if im['split'] == splitType:
            sents = im['sentences']
            tokens = [sent['tokens'] for sent in sents]
            raws = [sent['raw'] for sent in sents]
            coco_set.append((im['cocoid'], tokens))
            # coco_set.append((im['cocoid'], raws))
    count = 0
    count_miss = 0
    #im_ids = []
    for idx, c in enumerate(captions):
        c_tok = tokenizer(c)
        c_tok = [token.text for token in c_tok]
        # print(len(c_tok))
        # c_tok = c.split()
        found = False
        for (cocoid, items) in coco_set:
            for item in items:
                # item = re.sub('[^A-Za-z0-9]+', ' ', item.lower())
                # item = item.split()
                diff_1 = list(set(item).difference(set(c_tok)))
                diff_2 = list(set(c_tok).difference(set(item)))
                diff = max(len(diff_1), len(diff_2))
                if diff == 0:
                    #im_ids.append(cocoid)
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
                logfile.write(str(idx) + '\t' + str(c_tok) + '\t' + c + '\n')
                print('could not found : ' + str(idx) + str(c_tok) + ' ' + c)

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
#             caps = anns[0]['caption']
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
    # get_image_id('train', args.start, args.end)
    get_image_id('test')
