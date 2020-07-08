import json
import ast
import argparse
import tqdm

parser = argparse.ArgumentParser(description="Parse arguments")
parser.add_argument("--type", default='template', help="Whether to output frame / template")
parser.add_argument("--split", help="Which split of data")
args = parser.parse_args()


split_type = args.split
path_cap = './cc_allcocositu_coco'
# path_cap = './cc_imsitu_coco' <-- old
cap_path = './VGNSL_split'
id_path = './VGNSL_ids'
file_name_id = '{}/{}_ids.filter.txt'.format(id_path, split_type)

def get_argpred(data_path, split_type):
    if split_type == 'dev':
        split_type = 'val'
    file_name_arg = '{}/{}_label20.json'.format(data_path, split_type)
    with open(file_name_arg) as f:
        arguments = json.load(f)
    # print(arguments[0])

    file_name_pred = '{}/{}_caption20.txt'.format(data_path, split_type)
    data = open(file_name_pred).readlines()
    data = [x.strip() for x in data if x.strip()]

    predicates = {}
    for item in data:
        imgid, line = item.split('\t')
        predicate = line.split()[3]
        predicates[imgid] = predicate

    return arguments, predicates

def get_tempcap(data_path, split_type):
    if split_type == 'dev':
        split_type = 'val'
    file_name_arg = '{}/{}_decode_coco20.json'.format(data_path, split_type)
    with open(file_name_arg) as f:
        template_captions = json.load(f)
    return template_captions

def pair_h_r_t(h, frame):
    result = ''
    for f in frame.keys():
        if type(frame[f]) is list and len(frame)>0:
            if len(frame[f]) > 0:
                word = frame[f][0]
                words = frame[f]
                if 'null' in words:
                    words.remove('null')
                if word != 'null':
                    words = '-'.join(words)
                    # word = word.replace(' ','-')
                    hrt = h + '_' + f.lower() + '_' + words
                    result += hrt + '\t'
    return result

def find_by_id(im_id, data_dict, key_id):
    # print(data_dict)
    for arg in data_dict:
        # print(arg)
        arg_id = arg['image_id']
        assert(type(im_id) == type(arg_id))
        if im_id == arg_id:
            # print('found' + str(arg))
            # print(len(arg))
            return arg
    print('could not find id ' + im_id)
    return {}


if args.type == 'frame':
    file_name_frame = '{}/{}_frames.txt'.format(cap_path, split_type)
    key_id = 'imgid'
    args, preds = get_argpred(path_cap, split_type)
    with open(file_name_id, 'r') as im_file, open(file_name_frame, 'w') as fr_file:
        for id in im_file:
            id = id.strip()
            pred = preds[id]
            arg_dict = find_by_id(id, args, key_id)
            line = pair_h_r_t(pred, arg_dict)
            for i in range(5):
                fr_file.write(line+'\n')

elif args.type == 'template':
    file_name_template = '{}/{}_templates.txt'.format(cap_path, split_type)
    key_id = 'image_id'
    temp_captions = get_tempcap(path_cap, split_type)
    with open(file_name_id, 'r') as im_file, open(file_name_template, 'w') as fr_file:
        for id in im_file:
            id = id.strip()
            arg_dict = find_by_id(int(id), temp_captions, key_id)
            if len(arg_dict) == 0:
                line = ''
            else:
                line = arg_dict['caption'].strip().split(' . ')[1]
            for i in range(5):
                fr_file.write(line+'\n')

else:
  raise ValueError(f'Illegal equation {args.type}')
