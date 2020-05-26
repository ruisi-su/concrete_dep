#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create data files
"""

import os
import sys
import argparse
import numpy as np
import pickle
import itertools
from collections import defaultdict
import utils
import re
from constraint import gen_phrases
from itertools import islice


class Indexer:
    def __init__(self, symbols = ["<pad>","<unk>","<s>","</s>"]):
        self.vocab = defaultdict(int)
        self.PAD = symbols[0]
        self.UNK = symbols[1]
        self.BOS = symbols[2]
        self.EOS = symbols[3]
        self.d = {self.PAD: 0, self.UNK: 1, self.BOS: 2, self.EOS: 3}
        self.idx2word = {}

    def add_w(self, ws):
        for w in ws:
            if w not in self.d:
                self.d[w] = len(self.d)

    def convert(self, w):
        return self.d[w] if w in self.d else self.d[self.UNK]

    def convert_sequence(self, ls):
        return [self.convert(l) for l in ls]

    def write(self, outfile):
        out = open(outfile, "w")
        items = [(v, k) for k, v in self.d.items()]
        items.sort()
        for v, k in items:
            out.write(" ".join([k, str(v)]) + "\n")
        out.close()

    def prune_vocab(self, k, cnt = False):
        vocab_list = [(word, count) for word, count in self.vocab.items()]
        if cnt:
            self.pruned_vocab = {pair[0]:pair[1] for pair in vocab_list if pair[1] > k}
        else:
            vocab_list.sort(key = lambda x: x[1], reverse=True)
            k = min(k, len(vocab_list))
            self.pruned_vocab = {pair[0]:pair[1] for pair in vocab_list[:k]}
        for word in self.pruned_vocab:
            if word not in self.d:
                self.d[word] = len(self.d)
        for word, idx in self.d.items():
            self.idx2word[idx] = word

    def load_vocab(self, vocab_file):
        self.d = {}
        for line in open(vocab_file, 'r'):
            v, k = line.strip().split()
            self.d[v] = int(k)
        for word, idx in self.d.items():
            self.idx2word[idx] = word

def is_next_open_bracket(line, start_idx):
    for char in line[(start_idx + 1):]:
        if char == '(':
            return True
        elif char == ')':
            return False
    raise IndexError('Bracket possibly not balanced, open bracket not followed by closed bracket')

def get_between_brackets(line, start_idx):
    output = []
    for char in line[(start_idx + 1):]:
        if char == ')':
            break
        assert not(char == '(')
        output.append(char)
    return ''.join(output)

def get_tags_tokens_lowercase(line):
    output = []
    line_strip = line.rstrip()
    for i in range(len(line_strip)):
        if i == 0:
            assert line_strip[i] == '('
        if line_strip[i] == '(' and not(is_next_open_bracket(line_strip, i)): # fulfilling this condition means this is a terminal symbol
            output.append(get_between_brackets(line_strip, i))
    #print 'output:',output
    output_tags = []
    output_tokens = []
    output_lowercase = []
    for terminal in output:
        terminal_split = terminal.split()
        # print(terminal, terminal_split)
        assert len(terminal_split) == 2 # each terminal contains a POS tag and word
        output_tags.append(terminal_split[0])
        output_tokens.append(terminal_split[1])
        output_lowercase.append(terminal_split[1].lower())
    return [output_tags, output_tokens, output_lowercase]

# for the VGNSL ground truth spans comparison
def extract_spans(tree):
    answer = list()
    stack = list()
    items = tree.split()
    curr_index = 0
    for item in items:
        if item == ')':
            pos = -1
            right_margin = stack[pos][1]
            left_margin = None
            while stack[pos] != '(':
                left_margin = stack[pos][0]
                pos -= 1
            assert left_margin is not None
            assert right_margin is not None
            stack = stack[:pos] + [(left_margin, right_margin)]
            answer.append((left_margin, right_margin))
        elif item == '(':
            stack.append(item)
        else:
            stack.append((curr_index, curr_index))
            curr_index += 1
    return answer

def get_nonterminal(line, start_idx):
    assert line[start_idx] == '(' # make sure it's an open bracket
    output = []
    for char in line[(start_idx + 1):]:
        if char == ' ':
            break
        assert not(char == '(') and not(char == ')')
        output.append(char)
    return ''.join(output)


def get_actions(line):
    output_actions = []
    line_strip = line.rstrip()
    i = 0
    max_idx = (len(line_strip) - 1)
    while i <= max_idx:
        assert line_strip[i] == '(' or line_strip[i] == ')'
        if line_strip[i] == '(':
            if is_next_open_bracket(line_strip, i): # open non-terminal
                curr_NT = get_nonterminal(line_strip, i)
                output_actions.append('NT(' + curr_NT + ')')
                i += 1
                while line_strip[i] != '(': # get the next open bracket, which may be a terminal or another non-terminal
                    i += 1
            else: # it's a terminal symbol
                output_actions.append('SHIFT')
                while line_strip[i] != ')':
                    i += 1
                i += 1
                while line_strip[i] != ')' and line_strip[i] != '(':
                    i += 1
        else:
             output_actions.append('REDUCE')
             if i == max_idx:
                 break
             i += 1
             while line_strip[i] != ')' and line_strip[i] != '(':
                 i += 1
    assert i == max_idx
    return output_actions

def pad(ls, length, symbol):
    if len(ls) >= length:
        return ls[:length]
    return ls + [symbol] * (length -len(ls))

def clean_number(w):
    new_w = re.sub('[0-9]{1,}([,.]?[0-9]*)*', 'N', w)
    return new_w

def get_data(args):
    indexer = Indexer(["<pad>","<unk>","<s>","</s>"])
    def make_vocab(textfile, seqlength, minseqlength, lowercase, replace_num,
                   train=1, apply_length_filter=1):
        num_sents = 0
        max_seqlength = 0
        for tree in open(textfile, 'r'):
            tree.strip()
            tags, sent, sent_lower = get_tags_tokens_lowercase(tree)
            assert(len(tags) == len(sent))

            if lowercase == 1:
                sent = sent_lower
            if replace_num == 1:
                sent = [clean_number(w) for w in sent]
            if (len(sent) > seqlength and apply_length_filter == 1) or len(sent) < minseqlength:
                continue
            num_sents += 1
            max_seqlength = max(max_seqlength, len(sent))
            if train == 1:
                for word in sent:
                    indexer.vocab[word] += 1
        return num_sents, max_seqlength

    def convert(textfile, lowercase, replace_num,
                batchsize, seqlength, minseqlength, outfile, num_sents, max_sent_l=0,
                shuffle=0, include_boundary=1, apply_length_filter=1, framefile='', alignfile='', constraint_type=3, conllfile="", test=False):
        newseqlength = seqlength
        if include_boundary == 1:
            newseqlength += 2 #add 2 for EOS and BOS
        sents = np.zeros((num_sents, newseqlength), dtype=int)
        sent_lengths = np.zeros((num_sents,), dtype=int)
        dropped = 0
        sent_id = 0
        other_data = []

        dep_idx = 0
        if (conllfile != ''):
            deptrees = utils.read_conll(open(conllfile, 'r'))
            dep_list = list(deptrees)

        if test:
            with open(textfile, 'r') as txt, open(framefile, 'r') as fr, open(alignfile, 'r') as align, open('../data/coco/VGNSL_split/test_ground-truth.txt', 'r') as truth:
                for (tree, frame, alignment, ground_truth) in zip(txt, fr, align, truth):
                    frame = frame.strip().split('\t')
                    tree = tree.strip()
                    ground_truth = ground_truth.strip()
                    action = get_actions(tree)
                    tags, sent, sent_lower = get_tags_tokens_lowercase(tree)
                    assert(len(tags) == len(sent))

                    if (conllfile != ''):
                        try:
                            words, heads = dep_list[dep_idx]
                        except IndexError:
                            continue
                        if words != sent:
                            print("Data mismatch, got {} in {}, but {} in {}.".format(sent, textfile, words, conllfile))
                            continue
                        else:
                            dep_idx += 1
                        assert(len(words) == len(heads))
                        assert(len(heads) == len(sent))

                    if lowercase == 1:
                        sent = sent_lower
                    sent_str = " ".join(sent)
                    if replace_num == 1:
                        sent = [clean_number(w) for w in sent]
                    if (len(sent) > seqlength and apply_length_filter == 1) or len(sent) < minseqlength:
                        dropped += 1
                        continue
                    if include_boundary == 1:
                        sent = [indexer.BOS] + sent + [indexer.EOS]
                    max_sent_l = max(len(sent), max_sent_l)
                    sent_pad = pad(sent, newseqlength, indexer.PAD)
                    sents[sent_id] = np.array(indexer.convert_sequence(sent_pad), dtype=int)
                    sent_lengths[sent_id] = (sents[sent_id] != 0).sum()
                    if frame[0] == '':
                        invalids = []
                    else:
                        invalids = gen_phrases(sent_str, frame, alignment, constraint_type)

                    span, binary_actions, nonbinary_actions = utils.get_nonbinary_spans(action)

                    span = extract_spans(ground_truth)
                    other_data_item = [sent_str, invalids, tags, action,
                        binary_actions, nonbinary_actions, span, tree]

                    if (conllfile != ''):
                        other_data_item.append(heads)

                    other_data.append(other_data_item)
                    assert(2*(len(sent)- 2) - 1 == len(binary_actions))
                    assert(sum(binary_actions) + 1 == len(sent) - 2)
                    sent_id += 1
                    if sent_id % 100000 == 0:
                        print("{}/{} sentences processed".format(sent_id, num_sents))
        else:
            with open(textfile, 'r') as txt, open(framefile, 'r') as fr, open(alignfile, 'r') as align:
                for (tree, frame, alignment) in zip(txt, fr, align):
                    frame = frame.strip().split('\t')
                    tree = tree.strip()

                    action = get_actions(tree)
                    tags, sent, sent_lower = get_tags_tokens_lowercase(tree)
                    assert(len(tags) == len(sent))
                    if (conllfile != ''):
                        try:
                            words, heads = dep_list[dep_idx]
                        except IndexError:
                            continue
                        if words != sent:
                            print("Data mismatch, got {} in {}, but {} in {}.".format(sent, textfile, words, conllfile))
                            continue
                        else:
                            dep_idx += 1
                        assert(len(words) == len(heads))
                        assert(len(heads) == len(sent))

                    if lowercase == 1:
                        sent = sent_lower
                    sent_str = " ".join(sent)
                    if replace_num == 1:
                        sent = [clean_number(w) for w in sent]
                    if (len(sent) > seqlength and apply_length_filter == 1) or len(sent) < minseqlength:
                        dropped += 1
                        continue
                    if include_boundary == 1:
                        sent = [indexer.BOS] + sent + [indexer.EOS]
                    max_sent_l = max(len(sent), max_sent_l)
                    sent_pad = pad(sent, newseqlength, indexer.PAD)
                    sents[sent_id] = np.array(indexer.convert_sequence(sent_pad), dtype=int)
                    sent_lengths[sent_id] = (sents[sent_id] != 0).sum()
                    if frame[0] == '':
                        invalids = []
                    else:
                        invalids = gen_phrases(sent_str, frame, alignment, constraint_type)

                    span, binary_actions, nonbinary_actions = utils.get_nonbinary_spans(action)

                    other_data_item = [sent_str, invalids, tags, action,
                        binary_actions, nonbinary_actions, span, tree]

                    if (conllfile != ''):
                        other_data_item.append(heads)

                    other_data.append(other_data_item)
                    assert(2*(len(sent)- 2) - 1 == len(binary_actions))
                    assert(sum(binary_actions) + 1 == len(sent) - 2)
                    sent_id += 1
                    if sent_id % 100000 == 0:
                        print("{}/{} sentences processed".format(sent_id, num_sents))


        print(sent_id, num_sents)
        if shuffle == 1:
            rand_idx = np.random.permutation(sent_id)
            sents = sents[rand_idx]
            sent_lengths = sent_lengths[rand_idx]
            other_data = [other_data[idx] for idx in rand_idx]

        assert sent_id == len(other_data)
        #break up batches based on source lengths
        sent_lengths = sent_lengths[:sent_id]
        sent_sort = np.argsort(sent_lengths)
        sents = sents[sent_sort]
        other_data = [other_data[idx] for idx in sent_sort]
        sent_l = sent_lengths[sent_sort]
        curr_l = 1
        l_location = [] #idx where sent length changes

        for j,i in enumerate(sent_sort):
            if sent_lengths[i] > curr_l:
                curr_l = sent_lengths[i]
                l_location.append(j)
        l_location.append(len(sents))
        #get batch sizes
        curr_idx = 0
        batch_idx = [0]
        nonzeros = []
        batch_l = []
        batch_w = []
        for i in range(len(l_location)-1):
            while curr_idx < l_location[i+1]:
                curr_idx = min(curr_idx + batchsize, l_location[i+1])
                batch_idx.append(curr_idx)
        for i in range(len(batch_idx)-1):
            batch_l.append(batch_idx[i+1] - batch_idx[i])
            batch_w.append(sent_l[batch_idx[i]])
        # Write output
        f = {}
        f["source"] = sents
        f["other_data"] = other_data
        f["batch_l"] = np.array(batch_l, dtype=int)
        f["source_l"] = np.array(batch_w, dtype=int)
        f["sents_l"]  = np.array(sent_l, dtype = int)
        f["batch_idx"] = np.array(batch_idx[:-1], dtype=int)
        f["vocab_size"] = np.array([len(indexer.d)])
        f["idx2word"] = indexer.idx2word
        f["word2idx"] = {word : idx for idx, word in indexer.idx2word.items()}

        print("Saved {} sentences (dropped {} due to length/unk filter)".format(
            len(f["source"]), dropped))
        pickle.dump(f, open(outfile, 'wb'))
        return max_sent_l

    print("First pass through data to get vocab...")
    num_sents_train, train_seqlength = make_vocab(args.trainfile, args.seqlength, args.minseqlength,args.lowercase, args.replace_num, 1, 1)
    print("Number of sentences in training: {}".format(num_sents_train))
    num_sents_valid, valid_seqlength = make_vocab(args.valfile, args.seqlength, args.minseqlength,args.lowercase, args.replace_num, 0, 0)
    print("Number of sentences in valid: {}".format(num_sents_valid))
    num_sents_test, test_seqlength = make_vocab(args.testfile, args.seqlength, args.minseqlength,args.lowercase, args.replace_num, 0, 0)
    print("Number of sentences in test: {}".format(num_sents_test))

    if args.vocabminfreq >= 0:
        indexer.prune_vocab(args.vocabminfreq, True)
    else:
        indexer.prune_vocab(args.vocabsize, False)
    if args.vocabfile != '':
        print('Loading pre-specified source vocab from ' + args.vocabfile)
        indexer.load_vocab(args.vocabfile)
    indexer.write(args.outputfile + ".dict")
    print("Vocab size: Original = {}, Pruned = {}".format(len(indexer.vocab),
                                                          len(indexer.d)))
    print(train_seqlength, valid_seqlength, test_seqlength)
    max_sent_l = 0
    max_sent_l = convert(args.testfile, args.lowercase, args.replace_num,
                         args.batchsize, test_seqlength, args.minseqlength,
                         args.outputfile + "test.pkl", num_sents_test,
                         max_sent_l, args.shuffle, args.include_boundary, 0,
                         args.testframe, args.testalign, args.constraint_type,
                         conllfile="data/dep/test.conllx" if args.dep else "", test=True)
    max_sent_l = convert(args.valfile, args.lowercase, args.replace_num,
                         args.batchsize, valid_seqlength, args.minseqlength,
                         args.outputfile + "val.pkl", num_sents_valid,
                         max_sent_l, args.shuffle, args.include_boundary, 0,
                         args.valframe, args.valalign, args.constraint_type,
                         conllfile="data/dep/dev.conllx" if args.dep else "")
    max_sent_l = convert(args.trainfile, args.lowercase, args.replace_num,
                         args.batchsize, args.seqlength,  args.minseqlength,
                         args.outputfile + "train.pkl", num_sents_train,
                         max_sent_l, args.shuffle, args.include_boundary, 1,
                         args.trainframe, args.trainalign, args.constraint_type,
                         conllfile="" if args.dep else "")
    print("Max sent length (before dropping): {}".format(max_sent_l))

def main(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--vocabsize', help="Size of source vocabulary, constructed "
                                                "by taking the top X most frequent words. "
                                                " Rest are replaced with special UNK tokens.",
                                                type=int, default=10000)
    parser.add_argument('--vocabminfreq', help="Minimum frequency for vocab. Use this instead of "
                                                "vocabsize if > 0",
                                                type=int, default=-1)
    parser.add_argument('--include_boundary', help="Add BOS/EOS tokens", type=int, default=1)
    parser.add_argument('--lowercase', help="Lower case", type=int, default=1)
    parser.add_argument('--replace_num', help="Replace numbers with N", type=int, default=1)
    parser.add_argument('--trainfile', help="Path to training data.", required=True)
    parser.add_argument('--valfile', help="Path to validation data.", required=True)
    parser.add_argument('--testfile', help="Path to test validation data.", required=True)
    # parser.add_argument('--trainstart', help="index of the start of training data.", required=True)
    # parser.add_argument('--valstart', help="index of the start of validation data.", required=True)
    # parser.add_argument('--teststart', help="index of the start of test validation data.", required=True)
    # parser.add_argument('--textfile', help='fix file manually change indices to split', required=True)
    # parser.add_argument('--alignfile', help='File for alignment between frame and sent', type = str, default='')

    parser.add_argument('--batchsize', help="Size of each minibatch.", type=int, default=4)
    parser.add_argument('--seqlength', help="Maximum sequence length. Sequences longer "
                                               "than this are dropped.", type=int, default=150)
    parser.add_argument('--minseqlength', help="Minimum sequence length. Sequences shorter "
                                               "than this are dropped.", type=int, default=0)
    parser.add_argument('--outputfile', help="Prefix of the output file names. ", type=str,
                        required=True)
    parser.add_argument('--vocabfile', help="If working with a preset vocab, "
                                          "then including this will ignore srcvocabsize and use the"
                                          "vocab provided here.",
                                          type = str, default='')
    parser.add_argument('--shuffle', help="If = 1, shuffle sentences before sorting (based on  "
                                           "source length).",
                                          type = int, default = 0)
    parser.add_argument('--dep', action="store_true", help="Including dependency parse files. Their "
                                                           "names should be same as data file, but extensions "
                                                           "are .conllx.")
    # parser.add_argument('--multimodal', help='Using multimodal', type = int, default = 0)
    parser.add_argument('--trainframe', help='File for train frame results', type = str, default='')
    parser.add_argument('--valframe', help='File for val frame results', type = str, default='')
    parser.add_argument('--testframe', help='File for test frame results', type = str, default='')
    parser.add_argument('--trainalign', help='File for train align results', type = str, default='')
    parser.add_argument('--valalign', help='File for val align results', type = str, default='')
    parser.add_argument('--testalign', help='File for test align results', type = str, default='')
    parser.add_argument('--constraint_type', help='Type for constraint setup, rule 1 or rule 2 or both', type = int, default=3)
    args = parser.parse_args(arguments)
    np.random.seed(3435)
    get_data(args)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
