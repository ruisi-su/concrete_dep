import spacy
nlp = spacy.load('en_core_web_sm')

con = {}

def check_hyphen(str):

    if '-' in str:
        return str
    else:
        str = nlp(str)
        return str[0].lemma_

with open('./Concreteness_ratings_Brysbaert_et_al_BRM_modified.txt', 'r') as c:
    for line in c:
        line = line.strip().split('\t')
        word = '-'.join(line[0].split(' '))
        score = line[2]
        con[word] = score

with open('./traindevtest.cos', 'r') as cos, open('./traindevtest.cos.lemma', 'w') as out:
    for line in cos:
        if not line.strip():
            out.write('\n')
            continue
        pairs = line.strip().lower().split('\t')
        c_seen = []
        for pair in pairs:
            c, f = pair.split(':')
            if c in c_seen:
                continue
            c_seen.append(c)
            c = check_hyphen(c)
            f = check_hyphen(f)

        if c == f:
            out.write('%s:%s\t' %(c, f))
        out.write('\n')

        # if c in con.keys() and f in con.keys():
