import io
import numpy as np
import tqdm
import sys
import pickle
import fasttext
import fasttext.util


ft = fasttext.load_model('../../Downloads/cc.en.300.bin')

# write to pickle
w2v = dict()

with open(sys.argv[1], 'r') as dict:
    for l in tqdm.tqdm(dict):
        word, count = l.strip().split(' ')

        w2v[word] = ft.get_word_vector(word)
        # w2v[word] = word_embed
pickle.dump(w2v, open(sys.argv[2], "wb"))
# def load_vectors(fname):
#     fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
#     n, d = map(int, fin.readline().split())
#     data = {}
#     for line in fin:
#         tokens = line.rstrip().split(' ')
#         map_float = map(float, tokens[1:])
#         data[tokens[0]] = np.fromiter(map_float, dtype=float)
#         assert(len(data[tokens[0]]) == 300)
#     return data
#
# load_vectors('../../Downloads/cc.en.300.vec')
