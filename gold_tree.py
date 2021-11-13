# import spacy
# from benepar.spacy_plugin import BeneparComponent
import argparse
from nltk import Tree
import benepar
import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
parser = argparse.ArgumentParser()
parser.add_argument('--splitType', default='train')
args = parser.parse_args()

tree_parser = benepar.Parser("benepar_en3_large")


def gen_gold_tree(in_sent):
    tree = tree_parser.parse(in_sent)
    parse_string = ' '.join(str(tree).split())
    return parse_string


def gen_trees(input_file, output_file):
    with open(input_file, 'r') as in_file, open(output_file, 'w') as out_file:
        for line in in_file:
            line = line.strip('\n')
            line = line.replace(' .', '')  # remove the legal periods
            line = line.replace('.', ' ')  # remove the illegal periods of the data
            tree = gen_gold_tree(line)
            out_file.write(tree + '\n')


def main(args):
    data_path = 'data/proc_data'
    input = 'caps'
    output = 'trees'
    input_file = '{}/{}_{}.txt'.format(data_path, args.splitType, input)
    output_file = '{}/{}_{}.txt'.format(data_path, args.splitType, output)
    gen_trees(input_file, output_file)


if __name__ == '__main__':
    main(args)
