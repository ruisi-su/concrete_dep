import json
import spacy
import csv
from utils import update_dict
# for dependency parsing, using the generation templates for realizing situations
nlp = spacy.load("en_core_web_sm")

# mapping
imsitu = json.load(open("imsitu_space.json"))

# training annotations
train = json.load(open("train.json"))
# result dictionary
output_name = 'dep_data_perc.json'

# templates path
path = 'simple_sentence_realization/generation_templates.tab'

# write_dep(output_name, path)
def write_dep(output_name, temp_path):
    dep_dict = {}
    with open(path,'r') as f:
        # next(f) # skip headings
        reader=csv.reader(f,delimiter='\t')
        for verb, sent in reader:
            # print(sent)
            doc = nlp(sent.lower())
            # get dependencies
            for chunk in doc.noun_chunks:
                # print(chunk.text, chunk.root.text, chunk.root.dep_,
                        # chunk.root.head.text)
                dep_dict = update_dict(dep_dict, chunk.text, chunk.root.dep_)

    # Writing a JSON file
    with open(output_name, 'w') as f:
        json.dump(dep_dict, f)

# cleaned dependency data
input = "dep_data_clean.json"

def write_prob(output_name, input_name):
    dep_dict = json.load(open(input_name))
    # print(dep_dict)
    # convert probabilities by each key
    for k in dep_dict.keys():
    # print(dep_dict['destination'])
    # print(str(sum(dep_dict['destination'].values())))
        item = dep_dict[k]
        total = sum(item.values())
        for j in item.keys():
            item[j] /= total
    print(dep_dict)
    # Writing a JSON file
    with open(output_name, 'w') as f:
        json.dump(dep_dict, f)

write_prob('dep_data_prob.json', input)
