from numpy.linalg import norm
import operator
import fasttext

ft = fasttext.load_model('../Downloads/cc.en.300.bin')


with open('./data/coco/VGNSL_split/traindevtest.cap', 'r') as cap, open('./data/coco/VGNSL_split/traindevtest.frame', 'r') as frame, open('./traindevtest.cos', 'w') as out:
    for c, f in zip(cap, frame):
        if not f.strip():
            out.write('\n')
            continue
        c = c.strip()
        f = f.strip().split('\t')
        kwl = []
        # get frame labels
        for i, fr in enumerate(f):
            fr = fr.split('_')
            if i == 0:
                kwl.append(fr[0])
            kwl.append(fr[2])
        for kw in kwl:
            kwd = {}
            kwv = ft.get_word_vector(kw)
            # search captions
            for w in c.split(' '):
                wv = ft.get_word_vector(w)
                dis = (wv @ kwv.T) / (norm(wv) * norm(kwv))
                kwd[w] = dis
            argmax = max(kwd.items(), key=operator.itemgetter(1))[0]
            # print('for keyword %s, argmax is %s' % (kw, argmax))
            # cap : frame
            out.write('%s:%s\t' %(argmax, kw))
        out.write('\n')
