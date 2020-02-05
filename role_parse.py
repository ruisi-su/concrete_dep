import json
from collections import Counter
from utils import update_dict, update_dict_prob
from dep_parse import write_prob

# mapping
imsitu = json.load(open("imsitu_space.json"))

# training annotations
train = json.load(open("train.json"))

output_name = 'role_data.json'

# for each line of training
# for each frame
# save the noun key to its role
# new dic should look like: {'noun_id1': ['agent': x many times, 'place': y many times, etc]}

# image file | frames | 3 examples | list of roles with specific nouns

def write_role(train):
    role_dict = {}
    for train_entry in train:
        item = train[train_entry]['frames']
        for frame in item:
            for role in frame.keys():
                noun_id = frame[role]
                if noun_id == '':
                    continue
                role_dict = update_dict(role_dict, noun_id, role)
    # Writing a JSON file
    with open(output_name, 'w') as f:
        json.dump(role_dict, f)

# write_role(train)
role_data = json.load(open('role_data_prob.json'))
dep_data = json.load(open('dep_data_prob.json'))
# print(role_data['n09265620'])
# noun1_key = 'n13270038'
# noun2_key = 'n15021085'
# noun1 = nouns[noun1_key]

# out_dict = output dictionary
# n_id = the noun id
# dep_data = dependency data
# role_data = situation role data
def update_noun(out_dict, n_id, dep_data, role_data):
    if n_id not in role_data.keys():
        return out_dict
    roles = role_data[n_id]
    noun = nouns[n_id]
    # item, place, etc
    for r in roles:
        if r not in dep_data.keys():
            continue
        role_prob = roles[r]
        # nsubj, dobj, etc.
        for d in dep_data[r].keys():
            combined_prob = role_prob * dep_data[r][d]
            update_dict_prob(out_dict, noun['gloss'], d, combined_prob)
    return out_dict

## PROBABLITIES ARE WRONG
def update_nouns(nouns, out_file, dep_data, role_data):
    out_dict = {}
    for n in nouns:
        out_dict = update_noun(out_dict, n, dep_data, role_data)
    print('finishing...write to file')
    with open(out_file, 'w') as f:
        json.dump(out_dict, f)

update_nouns(nouns, 'combine_prob.json', dep_data, role_data)

# for key, value in role1.items():
#     if key not in ['gloss']:
#         probs = dep_data[key]
#         print(probs)
# print(role_dep)

# combine the probabilities by:
# sum _(i=pos) (p(dep=pos | role = r)p(role = r))
# def combine_prob(role_dict, dep_dict):
#     for n in nouns:
#         print(n)
#
# combine_prob(role_data, dep_data)
