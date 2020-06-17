import json
import ast

def get_argpred(data_path_arg, data_path_cap, split_type):
    if split_type == 'dev':
        split_type = 'val'
    file_name_arg = '{}/{}_label20.json'.format(data_path_arg, split_type)
    with open(file_name_arg) as f:
        arguments = json.load(f)
    # print(arguments[0])

    file_name_pred = '{}/{}_caption20.txt'.format(data_path_cap, split_type)
    data = open(file_name_pred).readlines()
    data = [x.strip() for x in data if x.strip()]

    predicates = {}
    for item in data:
        imgid, line = item.split('\t')
        predicate = line.split()[3]
        predicates[imgid] = predicate

    return arguments, predicates

def pair_h_r_t(h, frame):
    result = ''
    for f in frame.keys():
        if type(frame[f]) is list and len(frame)>0:
            if len(frame[f]) > 0:
                word = frame[f][0]
                words = frame[f]
                if word != 'null':
                    words = '-'.join(words)
                    # word = word.replace(' ','-')
                    hrt = h + '_' + f.lower() + '_' + words
                    result += hrt + '\t'
    return result

def find_by_id(im_id, arguments):
    for arg in arguments:
        arg_id = arg['imgid']
        if im_id == arg_id:
            return arg
    print('could not find id ' + im_id)
    return {}

split_type = 'train'
path_cap = './cc_cocositu_coco'
# path_cap = './cc_imsitu_coco' <-- old

cap_path = './VGNSL_split'
id_path = './VGNSL_ids'
file_name_id = '{}/{}_ids.filter.txt'.format(id_path, split_type)
file_name_frame = '{}/{}_frames.txt'.format(cap_path, split_type)
# train set uses the same path
args, preds = get_argpred(path_cap, path_cap, split_type)
with open(file_name_id, 'r') as im_file, open(file_name_frame, 'w') as fr_file:
    for id in im_file:
        id = id.strip()
        pred = preds[id]
        arg_dict = find_by_id(id, args)
        line = pair_h_r_t(pred, arg_dict)
        for i in range(5):
            fr_file.write(line+'\n')
