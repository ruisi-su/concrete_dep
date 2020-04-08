import spacy
from benepar.spacy_plugin import BeneparComponent
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--splitType', default='train')
args = parser.parse_args()

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe(BeneparComponent('benepar_en2'))

def gen_gold_tree(in_sent):
    doc = nlp(in_sent)
    sent = list(doc.sents)[0]
    return sent._.parse_string

def gen_trees(input_file, output_file):
    with open(input_file, 'r') as in_file, open(output_file, 'w') as out_file:
        for line in in_file:
            line = line.strip('\n')
            tree = gen_gold_tree(line)
            out_file.write(tree + '\n')

def main(args):
    data_path = 'data/coco/mscoco_unfiltered'
    input_file = '{}/{}_cap_clean.txt'.format(data_path, args.splitType)
    output_file = '{}/{}_gold.txt'.format(data_path, args.splitType)
    gen_trees(input_file, output_file)

if __name__ == '__main__':
    main(args)
