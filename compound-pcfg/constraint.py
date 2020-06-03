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
def invalid_phrases_type1(frame, predicate, phrase_set, start, end, invalids, sent, arguments, is_pred, heads, log_path=''):
    if log_path != '':
        log_file = open(log_path, "a")

    # predicate = frame[0].split('_')[0]
    # heads = phrase
    # phrase_set = set(phrase)
    intersect = phrase_set.intersection(arguments)
    # phrase_str = ' '.join(phrase)
    # rule 1 applies when predicate does not exist in the phrase
    if (predicate not in phrase_set) or not is_pred:
        # if more than one argument exists in the phrase, its already invalid
        if len(intersect) > 1:
            if heads != None:
                for head in heads:
                    head_ind = sent.index(head)
                    phrase_range = (start, end, head_ind)
                    if head_ind <= end:
                        invalids.add(phrase_range)
                        log = 'R1 invalid is ('  + str(' '.join(sent[start:end])) + ') head is ' + str(head_ind) + '-' + str(sent[head_ind])
                        if log_path != '':
                            log_file.write(log + '\n')
            else:
                phrase_range = (start, end)
                invalids.add(phrase_range)
                log = 'R1 invalid is ('  + str(' '.join(sent[start:end])) + ')'
                if log_path != '':
                    log_file.write(log + '\n')
    if log_path != '':
        log_file.close()
    return invalids

def invalid_phrases_type2(frame, predicate, phrase_set, start, end, invalids, sent, arguments, alignment, is_pred, heads, log_path=''):
    if log_path != '':
        log_file = open(log_path, "a")

    # predicate = frame[0].split('_')[0]
    # heads = phrase
    # phrase_set = set(phrase)

    intersect = phrase_set.intersection(arguments)
    # phrase_str = ' '.join(phrase)
    # rule 2 applies when the predicate exists in the phrase (must exist in the sent)
    if (predicate in phrase_set) or is_pred:
        if predicate in alignment.keys():
            predicate = alignment[predicate]
        else:
            pred_ind = sent.index(predicate)
        if heads != None:
            for head in heads:
                head_ind = sent.index(head)
                phrase_range = (start, end, head_ind)
                if (head != predicate) or (head_ind <= end):
                #if (head != predicate) or (head_ind <= end_idx) or (head not in argument):
                    log = 'R2 invalid is ('  + str(' '.join(sent[start:end])) + ') head is ' + str(head_ind) + '-' + str(sent[head_ind])
                    invalids.add(phrase_range)
                    if log_path != '':
                        log_file.write(log + '\n')
    if log_path != '':
        log_file.close()
    return invalids

# generate all possible phrases from left to right, not including the entire sentence
def gen_phrases(sent, frame, alignment, type, head):
    alignment = alignment
    # parse alignment
    alignment = get_align(alignment.lower())
    # default: assume pred is not in the sent
    is_pred = False

    sent = sent.split(' ')
    # check if predicate exists in the sentence, or it is aligned
    predicate = frame[0].split('_')[0]
    if (predicate in sent) or (predicate in alignment.keys()):
        is_pred = True
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

    pointer = 0
    end = len(sent)
    invalids = set()

    while pointer < end:
        # loop for current pointer
        for ind in range(pointer, end):
            # set end index
            if pointer == 0:
                phrase = sent[pointer:ind]
            else:
                phrase = sent[pointer:ind+1]
            # generate set
            phrase_set = set(phrase)
            # generate list of heads
            if head:
                heads = phrase
            else:
                heads = None

            if type == 1:
                invalids = invalid_phrases_type1(frame, predicate, phrase_set, pointer, ind, invalids, sent, arguments, is_pred, heads)
            elif type == 2:
                invalids = invalid_phrases_type2(frame, predicate, phrase_set, pointer, ind, invalids, sent, arguments, alignment, is_pred, heads)
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
        # only store the first occurance of the aligned word
        if frame not in aligns.keys():
            aligns[frame] = cap
    return aligns

# gold is ( ( ( ( A man) ) ( doing ( a  hand ) ) ) ( stand ( next ( to (a Frisbee ) ) ) ) (. .))
# aligns = 'man:agent_man hand:tool_hand Frisbee:caughtitem_Frisbee '
# frame = 'catching_tool_hand	catching_agent_man	catching_caughtitem_Frisbee	catching_place_park'
# sent = 'a man doing a hand stand next to a frisbee'
# invals = gen_phrases(sent, frame.lower().strip().split('\t'), aligns.lower(), 1, False)
# invals_2 = gen_phrases(sent, frame.strip().split('\t'), aligns.lower(), 2, True)
# print(invals)
# print(invals_2)
# print(invals == invals_2)
