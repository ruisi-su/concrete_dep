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
def invalid_phrases_type1(frame, predicate, phrase, start, end, invalids, sent, arguments, log_path=''):
    if log_path != '':
        log_file = open(log_path, "a")

    intersect = set(phrase).intersection(arguments)
    # rule 1 applies when predicate does not exist in the phrase
    if predicate == '':
        head_ind = start
        # if more than one argument exists in the phrase, its already invalid
        if len(intersect) > 1:
            for head in phrase:
                phrase_range = (start, end, head_ind)
                if head_ind <= end:
                    invalids.add(phrase_range)
                    log = 'R1 invalid is ('  + str(' '.join(sent[start:end+1])) + ') head is ' + str(head_ind) + '-' + str(sent[head_ind])

                    if log_path != '':
                        log_file.write(log + '\n')
                head_ind += 1
    if log_path != '':
        log_file.close()
    return invalids

# rule 2: an argument cannot be the head of a phrase that also contains its predicate
def invalid_phrases_type2(frame, predicate, phrase, start, end, invalids, sent, arguments, log_path=''):
    if log_path != '':
        log_file = open(log_path, "a")

    intersect = set(phrase).intersection(arguments)
    # predicate is present in this phrase
    if predicate != '':
        head_ind = start
        for head in phrase:
            phrase_range = (start, end, head_ind)
            assert(head_ind <= end)
            # if this head is an argument, it is invalid (because the span contains the predicate)
            if (head in intersect):
                log = 'R2 invalid is ('  + str(' '.join(sent[start:end+1])) + ') head is ' + str(head_ind) + '-' + str(sent[head_ind])
                invalids.add(phrase_range)
                if log_path != '':
                    log_file.write(log + '\n')
            head_ind += 1
    if log_path != '':
        log_file.close()
    return invalids

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
                invalids = invalid_phrases_type1(frame, pred_cap, phrase, pointer, ind-1, invalids, sent, arguments)
            elif constraint_type == 2:
                invalids = invalid_phrases_type2(frame, pred_cap, phrase, pointer, ind-1, invalids, sent, arguments)
            elif constraint_type == 3:
                invalids = invalid_phrases_type1(frame, pred_cap, phrase, pointer, ind-1, invalids, sent, arguments).union(invalid_phrases_type2(frame, pred_cap, phrase, pointer, ind-1, invalids, sent, arguments))
        pointer += 1
    # get the index of pred and arg
    print(pred_cap)
    if pred_cap in sent:
        pred_idx = sent.index(pred_cap)
    else:
        pred_idx = -1
    arg_idcs = []
    for argument in arguments:
        if argument in sent:
            arg_idcs.append(sent.index(argument))
    return list(invalids), pred_idx, arg_idcs


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
# gold tree : ((a (large post)) (with ((a clock) outside)))
aligns = 'a:place:0.890 clock:clock:0.702 with:item:0.236 large:displaying:0.070 outside:outside:0.052 post:tool:0.004'
frame = 'displaying_tool_tool\tdisplaying_item_clock\tdisplaying_place_outside\t'
sent = 'a large post with a clock outside'
invals = gen_phrases(sent, frame.strip().split('\t'), aligns.lower(), 1, 0.005)
invals_2 = gen_phrases(sent, frame.strip().split('\t'), aligns.lower(), 2, 0.005)
invals_3 = gen_phrases(sent, frame.strip().split('\t'), aligns.lower(), 3, 0.005)
print(invals)
print(invals_2)
print(invals_3)
