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
def invalid_phrases(frame, phrase, invalids):
    predicate = frame[0].split('_')[0]
    phrase = phrase.split(' ')
    heads = phrase
    phrase_set = set(phrase)
    argument = set()
    # rule 1
    check_membership = True
    # rule 2
    check_head =  True
    print(frame)
    for f in frame:
        print(f)
        args = f.split('_')
        print(args)
        arg = args[2]
        argument.add(arg)

    intersect = phrase_set.intersection(argument)

    # check rule 1
    # check if predicate exists in phrase
    if predicate not in phrase_set:
        print('not in phrase')
        # if more than one argument exists in the phrase, its already invalid
        if len(intersect) > 1:
            check_membership = False
            for head in heads:
                if head not in invalids.keys():
                    invalids[head] = []
                phrase_str = ' '.join(phrase)
                invalids[head].append(phrase_str)

    else:
        print('in phrase')
        for head in heads:
            check_head = (head == predicate)
            if head not in invalids.keys():
                invalids[head] = []
            # TODO ASSUME predicate cannot exist by itself
            if len(intersect) == 0:
                invalids[head].append(predicate)
            elif head != predicate:
                phrase_str = ' '.join(phrase)

                invalids[head].append(phrase_str)

    return invalids

# print(invalid_phrases(sample_frame, 'dogs eat food'))

# generate all possible phrases from left to right, not including the entire sentence
def gen_phrases(sent, frame):
    sent = sent.split(' ')
    pointer = 0
    end = len(sent)
    invalids = {}
    while pointer < end:
        # loop for current pointer
        # if the first word, stop before the last word
        if pointer == 0:
            phrase_end = len(sent) - 1
        else:
            phrase_end = end
        for ind in range(pointer, phrase_end):
            print('pointer = ' + str(pointer) + ' word ' + str(sent[pointer]))
            phrase = sent[pointer:ind+1]
            phrase_str = ' '.join(phrase)
            print(phrase_str)
            invalids = invalid_phrases(frame, phrase_str, invalids)

        pointer += 1
    return invalids

# sample = 'dogs eat food at home'
# # sample11 = '(NT (T dogs) (NT (T eat) (NT (T food) (NT (T at) (T Home)))))'
# sample_frame = ['eat_agent_dogs', 'eat_food_food', 'eat_place_home']
# sample_phrases = ['eat food at home', 'food at home', 'food at', 'at home']
# sample_heads = ['eat', 'dogs', 'food', 'home']

# print(gen_phrases(sample, sample_frame))
