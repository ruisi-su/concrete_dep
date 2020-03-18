import pickle
from nltk import ParentedTree
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
sample = 'dogs eat food at home'
# sample11 = '(NT (T dogs) (NT (T eat) (NT (T food) (NT (T at) (T Home)))))'
sample_frame = ['eat_agent_dogs', 'eat_food_food', 'eat_place_home']
sample_phrases = ['eat food at home', 'food at home', 'food at', 'at home']
sample_heads = ['eat', 'dogs', 'food', 'home']

# frame only has one verb
def phrase_validity(sent, frame, phrase, head):
    predicate = frame[0].split('_')[0]
    phrase = phrase.split(' ')
    phrase = set(phrase)
    argument = set()

    # rule 1
    check_membership = False
    # rule 2
    check_head = False

    for f in frame:
        arg = f.split('_')[2]
        argument.add(arg)

    intersect = phrase.intersection(argument)
    # print(head)
    # print(argument)
    # print(phrase)

    # check rule 1
    # check if predicate exists in phrase
    if predicate not in phrase:
        # the head must exist in the phrase
        check_head = (head in phrase)
        # if more than one argument exists in the phrase
        if len(intersect) > 1:
            check_membership = False
        # only one argument exists in this phrase
        else:
            check_membership = True
    else:
        check_head = (head == predicate)
        # TODO ASSUME predicate cannot exist by itself
        if len(intersect) > 0:
            check_membership = True
        else:
            check_membership = False
    # print(check_membership)
    # print(check_head)
    return check_membership and check_head

assert(phrase_validity(sample, sample_frame, sample_phrases[0], sample_heads[0]) == True)
assert(phrase_validity(sample, sample_frame, sample_phrases[0], sample_heads[1]) == False)
assert(phrase_validity(sample, sample_frame, sample_phrases[0], sample_heads[2]) == False)
assert(phrase_validity(sample, sample_frame, sample_phrases[0], sample_heads[3]) == False)
assert(phrase_validity(sample, sample_frame, sample_phrases[1], sample_heads[2]) == False)
assert(phrase_validity(sample, sample_frame, sample_phrases[1], sample_heads[3]) == False)
assert(phrase_validity(sample, sample_frame, sample_phrases[1], sample_heads[1]) == False)
assert(phrase_validity(sample, sample_frame, sample_phrases[2], sample_heads[2]) == True)
assert(phrase_validity(sample, sample_frame, sample_phrases[2], sample_heads[3]) == False)
assert(phrase_validity(sample, sample_frame, sample_phrases[3], sample_heads[3]) == True)
