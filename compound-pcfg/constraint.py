import re
'''
1. two arguments belonging to the same predicate should not exist in a phrase unless the predicate also exists in that phrase
2. an argument cannot be the head of a phrase that also contains its predicate
Example: dogs eat food at home
here the predicate/argument pairs are:
eat->dogs
eat->food
eat->home

with rule 1, "food at home" could not be a phrase, but "eat food at home", "food at", and "at home" could all be phrases.

with rule 2, if we had a phrase "dogs eat", the head could not be "dogs", and "dogs eat food at home" the heads could not be "dogs", "food", or "home"
'''

# frame only has one verb
# gets the invalid phrases that violent either rules
# sent gives the original position of each word
def invalid_phrases(frame, phrase, invalids, sent, alignment):
    predicate = frame[0].split('_')[0]
    # phrase = phrase.split(' ')
    heads = phrase
    phrase_set = set(phrase)
    argument = set()
    for f in frame:
        args = f.split('_')
        arg = args[2]
        # if arg is not part of the alignment
        if arg not in alignment.keys():
            argument.add(arg)
        else:
        # else add the aligned word instead
            align = alignment[arg]
            argument.add(align)

    intersect = phrase_set.intersection(argument)

    # get range
    start_idx = sent.index(phrase[0])
    end_idx = sent.index(phrase[-1])
    phrase_str = ' '.join(phrase)
    # check rule 1
    # check if predicate exists in phrase
    if predicate not in phrase_set:
        # if more than one argument exists in the phrase, its already invalid
        if len(intersect) > 1:
            for head in heads:
                head_ind = sent.index(head)
                phrase_range = (start_idx, end_idx, head_ind)
                invalids.add(phrase_range)
    else:
        pred_ind = sent.index(predicate)

        for head in heads:
            head_ind = sent.index(head)
            phrase_range = (start_idx, end_idx, head_ind)
            # ASSUME predicate cannot exist by itself
            #if len(intersect) == 0  and pred_ind <= end_idx:
            #    print('indx equal')
            #    invalids.add((start_idx, end_idx, pred_ind))
            if (head != predicate) or (head_ind <= end_idx) or (head not in argument):
                invalids.add(phrase_range)
    return invalids

# generate all possible phrases from left to right, not including the entire sentence
def gen_phrases(sent, frame, alignment):
    alignment = get_align(alignment)
    sent = sent.split(' ')
    pointer = 0
    end = len(sent)
    invalids = set()
    while pointer < end:
        # loop for current pointer
        # if the first word, stop before the last word
        if pointer == 0:
            phrase_end = len(sent) - 1
        else:
            phrase_end = end
        for ind in range(pointer, phrase_end):
            phrase = sent[pointer:ind+1]
            # phrase_str = ' '.join(phrase)
            invalids = invalid_phrases(frame, phrase, invalids, sent, alignment)

        pointer += 1
    return list(invalids)

def get_align(alignment):
    # key is frame, value is cap
    aligns = {}
    alignment = alignment.strip().split(' ')
    if len(alignment) == 0 or alignment[0] == '':
        return aligns
    # alignment is from cap : frame
    for al in alignment:
        # print(al)
        als = al.split(':')
        if len(als) > 2:
            cap = als[0] + ':' + als[1]
            frame = als[2]
        else:
            cap, frame = als
        # print(cap)
        # only store the first occurance of the aligned word
        if frame not in aligns.keys():
            aligns[frame] = cap
    return aligns
