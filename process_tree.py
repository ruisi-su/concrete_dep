import os
import re
import sys
import argparse
import nltk
from nltk.corpus import ptb
from nltk.tree import Tree
import os
from pathlib import Path
from lpcfg.preprocess import get_tags_tokens_lowercase


def get_data_ptb(orig_path, args):
  # tag filter is from https://github.com/yikangshen/PRPN/blob/master/data_ptb.py
  word_tags = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 
               'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 
               'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ',
               'WDT', 'WP', 'WP$', 'WRB']
  # currency_tags_words = ['#', '$', 'C$', 'A$']
  # ellipsis = ['*', '*?*', '0', '*T*', '*ICH*', '*U*', '*RNR*', '*EXP*', '*PPA*', '*NOT*']
  # punctuation_tags = ['.', ',', ':', '-LRB-', '-RRB-', '\'\'', '``']
  # punctuation_words = ['.', ',', ':', '-LRB-', '-RRB-', '\'\'', '``', '--', ';', 
  #                      '-', '?', '!', '...', '-LCB-', '-RCB-']
  # train_file_ids = []
  # val_file_ids = []
  # test_file_ids = []
  # train_section = ['02', '03', '04', '05', '06', '07', '08', '09', '10',
  #                  '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21']
  # val_section = ['22']
  # test_section = ['23']

  # for dir_name, _, file_list in os.walk(root, topdown=False):
  #   if dir_name.split("/")[-1] in train_section:
  #     file_ids = train_file_ids
  #   elif dir_name.split("/")[-1] in val_section:
  #     file_ids = val_file_ids
  #   elif dir_name.split("/")[-1] in test_section:
  #     file_ids = test_file_ids
  #   else:
  #     continue
  #   for fname in file_list:
  #     file_ids.append(os.path.join(dir_name, fname))
  #     assert(file_ids[-1].split(".")[-1] == "mrg")
  # print(len(train_file_ids), len(val_file_ids), len(test_file_ids))

  def del_tags(tree, word_tags):    
    for sub in tree.subtrees():
      for n, child in enumerate(sub):
        if isinstance(child, str):
          continue
        if all(leaf_tag not in word_tags for leaf, leaf_tag in child.pos()):
          del sub[n]

  def save_file(in_file_name, orig_path, args):
    # sens = []
    # trees = []
    # tags = []
    in_file = os.path.join(orig_path, in_file_name)
    out_file_name = 'clean.'+in_file_name
    out_file = os.path.join(orig_path, out_file_name)

    if args.cap:
      cap_file = os.path.join(orig_path, out_file_name.replace('_trees', '_caps'))
      cap_out = open(cap_file, 'w')

    with open(in_file, 'r') as orig_tree, open(out_file, 'w') as f_out:
      for l in orig_tree:
        l = l.strip()
        sen_tree = Tree.fromstring(l)
        orig = sen_tree.pformat(margin=sys.maxsize).strip()
        c = 0
        while not all([tag in word_tags for _, tag in sen_tree.pos()]):
          del_tags(sen_tree, word_tags)
          c += 1
          if c > 10:
            assert False
        out = sen_tree.pformat(margin=sys.maxsize).strip()          
        while re.search('\(([A-Z0-9]{1,})((-|=)[A-Z0-9]*)*\s{1,}\)', out) is not None:
          out = re.sub('\(([A-Z0-9]{1,})((-|=)[A-Z0-9]*)*\s{1,}\)', '', out)
        out = out.replace(' )', ')')
        out = re.sub('\s{2,}', ' ', out)
        f_out.write(out + '\n')

        if args.cap:
          _, caps, _ = get_tags_tokens_lowercase(out) 
          cap_out.write(' '.join(caps)+'\n')
    cap_out.close()

  save_file("train_trees.txt", orig_path, args)
  save_file("dev_trees.txt", orig_path, args)
  save_file("test_trees.txt", orig_path, args)

def main(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--orig_path', help='Path to the original parsed trees', type=str, 
                        default='./data/VGNSL_split/')
    parser.add_argument('--cap', help='Save cleaned captions', action='store_true')
    args = parser.parse_args(arguments)
    get_data_ptb(args.orig_path, args)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


