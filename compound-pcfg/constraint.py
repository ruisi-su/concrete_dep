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
# constraint type: 1 = rule 1, 2 = rule 2
def invalid_phrases_type1(frame, predicate, phrase, start, end, invalids, valids, sent, arguments, log_path=''):
    if log_path != '':
        log_file = open(log_path, "a")
    print(arguments)
    intersect = set(phrase).intersection(arguments)
    # rule 1 applies when predicate does not exist in the phrase
    if predicate == '':
        # if more than one argument exists in the phrase, its already invalid
        if len(intersect) > 1:
            head_ind_invalid = start
            for head in phrase:
                phrase_range = (start, end, head_ind_invalid)
                if head_ind_invalid <= end:
                    invalids.add(phrase_range)
                    log = 'R1 invalid is ('  + str(' '.join(sent[start:end+1])) + ') head is ' + str(head_ind_invalid) + '-' + str(sent[head_ind_invalid])

                    if log_path != '':
                        log_file.write(log + '\n')
                head_ind_invalid += 1
        elif len(intersect) == 1:
            arg = intersect.pop()
            arg_ind = sent.index(arg)
            if arg_ind <= end and arg_ind >= start:
                valids.add((start, end, arg_ind))
    if log_path != '':
        log_file.close()
    return invalids, valids

# rule 2: an argument cannot be the head of a phrase that also contains its predicate
def invalid_phrases_type2(frame, predicate, phrase, start, end, invalids, valids, sent, arguments, log_path=''):
    if log_path != '':
        log_file = open(log_path, "a")

    intersect = set(phrase).intersection(arguments)
    # predicate is present in this phrase
    if predicate != '':
        head_ind_invalid = start
        # add valid span that has pred as head
        pred_ind = sent.index(predicate)
        for head in phrase:
            assert(head_ind_invalid <= end and head_ind_invalid >= start)
                # if this head is an argument, it is invalid (because the span contains the predicate)
            if (head in intersect):
                assert(head_ind_invalid != pred_ind)
                phrase_range = (start, end, head_ind_invalid)
                # log = 'R2 invalid is ('  + str(' '.join(sent[start:end+1])) + ') head is ' + str(head_ind_invalid) + '-' + str(sent[head_ind_invalid])
                invalids.add(phrase_range)
                # if log_path != '':
                    # log_file.write(log + '\n')
            head_ind_invalid += 1
        if pred_ind <= end and pred_ind >= start:
            valids.add((start, end, sent.index(predicate)))
    if log_path != '':
        log_file.close()
    return invalids, valids

# generate all possible phrases from left to right, not including the entire sentence
def gen_phrases(sent, frame, alignment, constraint_type, threshold):
    alignment = alignment
    # parse alignment
    alignment = get_align(alignment.lower(), threshold)
    sent = sent.split(' ')
    predicate = frame[0].split('_')[0]
    # print(alignment)
    # add alignments
    arguments = set()
    for f in frame:
        args = f.split('_')
        arg = args[2]
        # if arg is not part of the alignment
        if arg not in alignment.keys():
            arguments.add(arg)
        else:
        # else add the aligned word instead
            align = alignment[arg]
            arguments.add(align)
    # print(arguments)
    pointer = 0
    # end = len(sent)
    invalids = set()
    valids = set()
    while pointer < len(sent):
        # loop for current pointer
        if pointer == 0:
            end = len(sent)
        else:
            end = len(sent) + 1
        for ind in range(pointer+2, end):
            phrase = sent[pointer:ind]
            # print(str(phrase) + ' from ' + str(pointer) + ' to ' + str(ind-1))
            # generate set
            phrase_set = set(phrase)
            # predicate in caption
            pred_cap = ''
            # find predicate in caption phrase, if any, or if it is aligned to any word of the caption phrase
            if (predicate in phrase):
                pred_cap = predicate
            elif (predicate in alignment.keys()) and (alignment[predicate] in phrase):
                pred_cap = alignment[predicate]
            # generate list of heads
            if constraint_type == 1:
                invalids, valids = invalid_phrases_type1(frame, pred_cap, phrase, pointer, ind-1, invalids, valids, sent, arguments)
            elif constraint_type == 2:
                invalids, valids = invalid_phrases_type2(frame, pred_cap, phrase, pointer, ind-1, invalids, valids, sent, arguments)
            elif constraint_type == 3:
                invalids_1, valids_1 = invalid_phrases_type1(frame, pred_cap, phrase, pointer, ind-1, invalids, valids, sent, arguments)
                invalids_2, valids_2 = invalid_phrases_type2(frame, pred_cap, phrase, pointer, ind-1, invalids, valids, sent, arguments)
                invalids = invalids_1.union(invalids_2)
                valids = valids_1.union(valids_2)
                # invalids = invalid_phrases_type1(frame, pred_cap, phrase, pointer, ind-1, invalids, sent, arguments).union(invalid_phrases_type2(frame, pred_cap, phrase, pointer, ind-1, invalids, sent, arguments))
        pointer += 1
    # get the index of pred and arg

    # find predicate in caption phrase, if any, or if it is aligned to any word of the caption phrase
    # print(alignment)
    if (predicate in sent):
        pred_idx = sent.index(predicate)
    elif (predicate in alignment.keys()) and (alignment[predicate] in sent):
        pred_idx = sent.index(alignment[predicate])
    else:
        pred_idx = -1
    arg_idcs = []
    for argument in arguments:
        if argument in sent:
            arg_idcs.append(sent.index(argument))
    # return list(invalids), pred_idx, arg_idcs
    # return list(invalids), list(valids)
    assert(len(invalids.intersection(valids)) == 0)
    return list(invalids), list(valids)

    # return invalids, valids

# threshold is a relative percentage to the current set of alignments
# if threshold = 0.1 -> alignment with a score lower than 0.1 * max of current set is ignored
def get_align(alignment, threshold):
    # key is frame, value is cap
    aligns = {}
    alignment = alignment.strip().split(' ')
    if len(alignment) == 0 or alignment[0] == '':
        return aligns
    # the alignment with the max score is the first
    max_score = alignment[0].split(':')[-1]
    thresh = float(max_score) * threshold
    # alignment is from cap : frame
    for al in alignment:
        als = al.split(':')
        if len(als) > 3:
            cap = als[0] + ':' + als[1]
            frame = als[2]
            score = als[3]
            print('colon is detected, cap is ' + cap + ' frame is ' + frame)
        else:
            cap, frame, score = als
        # if below threshold, continue
        if float(score) < thresh:
            continue
        frame = frame.split('_')
        # remove indicators from the alignment by type
        # single word alignment
        if len(frame) == 1:
            frame = frame[0]
        elif len(frame) == 2:
            frame = frame[1]
        elif len(frame) == 3:
            frame = frame[2]
        else:
            raise ValueError('length of frame is invalid for ' + '_'.join(frame))
        if frame not in aligns.keys():
            aligns[frame] = cap
    return aligns

# ((two horses) (grazing (together (in (a field)))))

# {'taxiing': 'runway', 'airport': 'airport'}
# gold tree : (S (NP (DT A) (NN restaurant)) (VP (VBZ has) (NP (JJ modern) (JJ wooden) (NNS tables) (CC and) (NNS chairs))) (. .))
# aligns = 'runway:taxxiing:0.498 airport:airport:0.130'
# frame = 'taxiing_place_airport\ttaxiing_agent_airplane\ttaxiing_ground_runway'
# sent = 'the view of runway from behind the windows of airport .'
# invals, vals = gen_phrases(sent, frame.strip().split('\t'), aligns.lower(), 1, 0.0)
# invals_2, vals_2 = gen_phrases(sent, frame.strip().split('\t'), aligns.lower(), 2, 0.0)
# invals_3, vals_3 = gen_phrases(sent, frame.strip().split('\t'), aligns.lower(), 3, 0.0)
# print(invals)
# print(vals)
# print(invals_2)
# print(vals_2)
# print(invals_3)
# print(vals_3)
# print(len(invals.union(invals_2)))
# print(len(invals_3))
# print(invals_3.intersection(vals_3))
# assert(len(invals.union(invals_2))== len(invals_3))
