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
# constraint type: 1 = rule 1, 2 = rule 2, 3 = rule 1 & 2
def invalid_phrases(frame, phrase, invalids, sent, alignment, type, is_pred, log_invalids=False):
    if log_invalids:
        log_file = open("log_invalids.txt", "a")
    else:
        log_file = ''

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
    # store copies for different rule type
    invalids_2 = invalids
    invalids_3 = invalids
    # get range
    start_idx = sent.index(phrase[0])
    end_idx = len(phrase) - 1
    phrase_str = ' '.join(phrase)


    # check rule 1
    # check if predicate exists in phrase, or it doesn't exist at all in the sent
    if (predicate not in phrase_set) or not is_pred:
        # if more than one argument exists in the phrase, its already invalid
        if len(intersect) > 1:
            for head in heads:
                head_ind = sent.index(head)
                phrase_range = (start_idx, end_idx, head_ind)
                if head_ind <= end_idx:
                    log = 'R1 invalid is ('  + str(' '.join(sent[start_idx:end_idx])) + ') head is ' + str(head_ind) + '-' + str(sent[head_ind])
                    invalids.add(phrase_range)
                    invalids_3.add(phrase_range)
                    if log_file != '':
                        log_file.write(log + '\n')

    else:
        pred_ind = sent.index(predicate)
        for head in heads:
            head_ind = sent.index(head)
            phrase_range = (start_idx, end_idx, head_ind)
            if (head != predicate) or (head_ind <= end_idx):
            #if (head != predicate) or (head_ind <= end_idx) or (head not in argument):
                log = 'R2 invalid is ('  + str(' '.join(sent[start_idx:end_idx])) + ') head is ' + str(head_ind) + '-' + str(sent[head_ind])
                invalids_2.add(phrase_range)
                invalids_3.add(phrase_range)
                if log_file != '':
                    log_file.write(log + '\n')
    if log_file != '':
        log_file.close()
    if type == 1:
        return invalids
    elif type == 2:
        return invalids_2
    else:
        return invalids_3

# generate all possible phrases from left to right, not including the entire sentence
def gen_phrases(sent, frame, alignment, type, pred_present):
    alignment = get_align(alignment.lower())
    sent = sent.split(' ')
    # default: assume pred is in the sent
    is_pred = True
    # check if predicate exists in the sentence, or it is aligned
    predicate = frame[0].split('_')[0]
    if (predicate in alignment.keys()) or (predicate in sent):
        # print('pred is in sent')
        pred_present += 1
        is_pred = False
    pointer = 0
    end = len(sent)
    invalids = set()
    while pointer < end:
        # loop for current pointer
        # if the first word, stop before the last word
        if pointer == 0:
            phrase_end = end - 1
        else:
            phrase_end = end
        for ind in range(pointer, phrase_end):
            phrase = sent[pointer:ind+1]
            invalids = invalid_phrases(frame, phrase, invalids, sent, alignment, type, is_pred)
        pointer += 1
    return list(invalids), pred_present

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
        # remove indicators from the alignment: place_dining -> dining
        frame = frame.split('_')
        if len(frame) > 1:
            frame = frame[1]
        else:
            frame = frame[0]
        # print(cap)
        # only store the first occurance of the aligned word
        if frame not in aligns.keys():
            aligns[frame] = cap
    return aligns

# gold is ( ( a road ) ( filled ( with cars ) ( in ( a desert ) ) ) )
# aligns = 'road:obstacle_car in:source_land '
# frame = 'filled_destination_land	filled_agent_man	filled_source_land	filled_obstacle_car	filled_place_road'
# sent = 'a road filled with cars in a desert'
# invals = gen_phrases(sent, frame.strip().split('\t'), aligns, 1, 0)
# print(invals)
