# import spacy
# from benepar.spacy_plugin import BeneparComponent
import argparse
from nltk import Tree
import benepar
import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'
parser = argparse.ArgumentParser()
parser.add_argument('--splitType', default='train')
# parser.add_argument('--imsitu', action='store_true')
args = parser.parse_args()

# nlp = spacy.load('en_core_web_sm')
# nlp.add_pipe(BeneparComponent('benepar_en2'))
tree_parser = benepar.Parser("benepar_en3_large")

def gen_gold_tree(in_sent):
    tree = tree_parser.parse(in_sent)
    parse_string = ' '.join(str(tree).split())
    # tokens = parser.parse(in_sent.split())
    # parse_tokens = ' '.join(str(tokens).split())
    # assert(parse_string == parse_tokens)
    # doc = nlp(in_sent.strip())
    # sent = list(doc.sents)[0]
    # print(sent._.parse_string)
    # print(parse_string)
    # print(parse_tokens)
    # assert(str(parse_string) == str(sent._.parse_string))
    return parse_string

def gen_trees(input_file, output_file):
    with open(input_file, 'r') as in_file, open(output_file, 'w') as out_file:
        for line in in_file:
            line = line.strip('\n')
            line = line.replace(' .', '') # remove the legal periods
            line = line.replace('.', ' ') # remove the illegal periods of the data
            tree = gen_gold_tree(line)
            out_file.write(tree + '\n')

def main(args):
    data_path = 'data/coco/VGNSL_split'
    input = 'caps'
    output = 'trees'
    # if args.imsitu:
    #     input = 'templates'
    #     output = 'temp_trees'
    input_file = '{}/{}_{}.txt'.format(data_path, args.splitType, input)
    output_file = '{}/{}_{}.txt'.format(data_path, args.splitType, output)
    gen_trees(input_file, output_file)

if __name__ == '__main__':
    main(args)
