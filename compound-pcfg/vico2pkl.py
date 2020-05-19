import pickle
import sys
import numpy as np
import tqdm

import h5py
import json
import numpy as np

# dict_path = 'data/preprocessed/ptb.dict'

glove_dim=300
vico_path = './glove_300_vico_linear_100/'
#vico_path = './glove_300_vico_select_200/'
f = h5py.File(vico_path + 'visual_word_vecs.h5py','r')
word_to_idx = json.load(open(vico_path + 'visual_word_vecs_idx.json','r'))
visual_words = json.load(open(vico_path + 'visual_words.json','r'))

# To just slice the row in the matrix without loading the full matrix in RAM do the following:
# embed_mat = f[embeddings]
# To load the entire matrix in memory (recommended if you are going to query words frequently) use the following instead:
embed_mat = f['embeddings'][()]

# write to pickle
w2v = dict()

with open(sys.argv[1], 'r') as dict:
    for l in tqdm.tqdm(dict):
        word, count = l.strip().split(' ')
        if word in word_to_idx:
            word_embed = embed_mat[word_to_idx[word]]
            word_embed_glove = word_embed[:glove_dim] # GloVe component
            word_embed_vico = word_embed[glove_dim:]  # ViCo component
        else:
            print('Word not in vocabulary ' + word)

        if word in visual_words:
            print('Word has ViCo component ' + word)
            # print(word_embed.shape)
        else:
            print('Word is not in the visual word vocabulary. word_embed_vico is set to average ViCo embedding computed across visual words' + word)
            word_embed = np.average(embed_mat, 0)
            word_embed_glove = word_embed[:glove_dim] # GloVe component
            word_embed_vico = word_embed[glove_dim:]  # ViCo component
        w2v[word] = word_embed_vico
pickle.dump(w2v, open(sys.argv[2], "wb"))
