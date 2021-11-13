import argparse
import spacy
from spacy.util import compile_infix_regex
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
all_stopwords = nlp.Defaults.stop_words


def get_concreteness():
    con = {}
    with open(args.concrete_file, 'r') as c:
        for line in c:
            line = line.strip().split('\t')
            word = '-'.join(line[0].split(' '))
            score = line[2]
            con[word] = score
    return con


def make_input(captions_file, frames_file, frame_preproc):
    infixes = ("…", r"(?<=[0-9])[*-+^](?=[0-9-])")
    infix_regex = compile_infix_regex(infixes)
    nlp.tokenizer.infix_finditer = infix_regex.finditer

    captions = open(captions_file).readlines()
    frames = open(frames_file).readlines()
    assert len(frames) == len(captions)

    tokenized_captions = [c.strip() for c in captions]

    with open(frames_file.replace('_frames.txt', '') +
              '.cap-frame.{}'.format(frame_preproc), 'w') as out:
        for caption, frame in zip(tokenized_captions, frames):
            if not frame.strip():
                out.write('\n')
                continue
            frame_words = []
            for word in frame.strip().split('\t'):
                if frame_preproc == 'none':
                    frame_words.append(word)
                elif frame_preproc == 'split_verb':
                    spl = word.split('_')
                    assert len(spl) == 3
                    if spl[0] not in frame_words:
                        frame_words.append(spl[0])
                    if '{}_{}'.format(spl[1],spl[2]) not in frame_words:
                        frame_words.append('{}_{}'.format(spl[1], spl[2]))
                elif frame_preproc == 'split_noverb':
                    spl = word.split('_')
                    assert len(spl) == 3
                    if spl[0] not in frame_words:
                        frame_words.append(spl[0])
                    if spl[2] not in frame_words:
                        frame_words.append(spl[2])
                elif frame_preproc == 'split_all':
                    spl = word.split('_')
                    assert len(spl) == 3
                    if spl[0] not in frame_words:
                        frame_words.append(spl[0])
                    if spl[1] not in frame_words:
                        frame_words.append(spl[1])
                    if spl[2] not in frame_words:
                        frame_words.append(spl[2])
                else:
                    print('No valid splitting provided.')

            # remove stop words & lemmatize
            cap_nonstop = []
            cap_doc = nlp(caption)
            for token in cap_doc:
                if token.is_punct:
                    continue
                elif (token.lemma_ in all_stopwords):
                    cap_nonstop.append('_')
                    continue
                cap_nonstop.append(token.lemma_)

            cap_str = ' '.join(cap_nonstop)
            if not cap_str:
                out.write('\n')
                continue
            out.write('{} ||| {}\n'.format(cap_str, ' '.join(frame_words)))


def align_words(align_output, align_input):
    intersect_alignment = open(align_output).readlines()
    pairs = open(align_input).readlines()

    assert len(intersect_alignment) == len(pairs)

    with open(align_output.replace('.intersect', '.output'), 'w') as f:
        for a, p in zip(intersect_alignment, pairs):
            if not a.strip():
                f.write('\n')
                continue
            pair_spl = p.strip().split(' ||| ')
            src_spl = pair_spl[0].strip().split()
            tgt_spl = pair_spl[1].strip().split()
            aligns = a.strip().split()

            for al in aligns:
                a_spl = al.split('-')
                f.write("{}:{} ".format(src_spl[int(a_spl[0])],
                                        tgt_spl[int(a_spl[1])]))
            f.write('\n')


parser = argparse.ArgumentParser()
parser.add_argument('--frames')
parser.add_argument('--captions')
parser.add_argument('--make_input', action='store_true')
parser.add_argument('--frame_preproc')
parser.add_argument('--align_output')
parser.add_argument('--align_input')
parser.add_argument('--filter', action='store_true')
parser.add_argument('--concrete_file', help='The file for concreteness scores', type=str, default='../../compound-pcfg/Concreteness_ratings_Brysbaert_et_al_BRM_modified.txt')
parser.add_argument('--gpu', type=int, default=0, help='GPU number for spacy')
args = parser.parse_args()

spacy.prefer_gpu(args.gpu)

if args.make_input:
    make_input(args.captions, args.frames, args.frame_preproc)

elif args.align_output:
    align_words(args.align_output, args.align_input)
