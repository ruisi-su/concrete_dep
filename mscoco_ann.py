# from pycocotools.coco import COCO
# import numpy as np
# import skimage.io as io
# import matplotlib.pyplot as plt
# import pylab
import json
import random

dataDir='annotations_2014'
dataType='val2014'

annFile = '{}/captions_{}.json'.format(dataDir,dataType)

coco  = json.load(open(annFile))
imgs = coco['images']
anns = coco['annotations']

# print(imgs[0])
# print(coco_caps.anns)
im_id = 'COCO_val2014_000000352755.jpg'

def get_id(file_name):
    for im in imgs:
        if im['file_name'] == file_name:
            return im['id']


def get_anns(im_id):
    result_anns = []
    result = ''
    for ann in anns:
        if ann['image_id'] == im_id:
            cap = ann['caption']
            cap = cap.strip('\n').strip('\t')
            # result_anns.append(cap)
            result += cap + '\t'

    # # randomly pick one
    # # print(result_anns)
    # ind = random.randint(0, len(result_anns)-1)
    # # print(ind)
    #
    # result = result_anns[ind].strip('\n').strip('.')
    # # print(result)
    # # result = result.replace(' ', '_')
    # print(result)
    return result

# get_anns(get_id(im_id))
