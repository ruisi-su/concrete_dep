import sys
from cfg2dep import get_sentence, find_matching_parenthese

fann = open(sys.argv[1], "w")
ftxt = open(sys.argv[2], "w")

def parse_line(line, offset=0):
    assert line[0] == "(" and line[-1] == ")", line
    label = line.split(' ')[0][1:]
    content = ' '.join(line.split(' ')[1:])[:-1]
    is_leaf = int(label.split('-')[0]) >= 10
    if is_leaf:
        return {'token': content, 'label':label}, 1
    else:
        break_pos = find_matching_parenthese(content, 0)
        left_subtree, left_count = parse_line(content[:break_pos], offset=offset)
        right_subtree, right_count = parse_line(content[break_pos+1:], offset=offset+left_count)
        return {'left':left_subtree, 'right':right_subtree, 'break_token_pos':offset+left_count, 'label':label}, left_count + right_count

def get_tags(tree):
    if 'left' in tree:
        return get_tags(tree['left']) + get_tags(tree['right'])
    else: 
        return [tree['label'].split('-')[0]]

nodeid = 0
def add_node(tag, start, word):
    global nodeid
    nodeid += 1
    label = "T%d"%(nodeid)
    fann.write("%s\t%s %d %d\t%s\n"%(label, tag, start, start + len(word), word))
    return label

def get_head(tree):
    head = int(tree['label'].split('-')[1])
    if not 'left' in tree:
        return head, []
    left_head, left_heads = get_head(tree['left'])
    right_head, right_heads = get_head(tree['right'])
    if left_head == head:
        ret_heads = [(right_head, head)]
    else:
        ret_heads = [(left_head, head)]
    ret_heads += left_heads
    ret_heads += right_heads
    return head, ret_heads

relationid = 0
position = 0
for line in sys.stdin:
    tree, _ = parse_line(line.strip())
    sentence = get_sentence(tree)
    tags = get_tags(tree)
    sentence_str = ' '.join(sentence)
    ftxt.write(sentence_str + "\n")
    pos = [position]
    for i in sentence:
        pos.append(pos[-1] + len(i) + 1)
    position = pos[-1]
    labels = []
    for i in range(len(sentence)):
        labels.append(add_node(tags[i], pos[i], sentence[i]))
    _, heads = get_head(tree)
    for u, v in heads:
        relationid += 1
        fann.write("R%d\t_ Arg1:%s Arg2:%s\n"%(relationid, labels[u], labels[v]))