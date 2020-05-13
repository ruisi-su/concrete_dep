
model_outs = []

with open('mmodal_out.txt', 'r') as output:
    for o in output:
        o = o.split('\t')
        pred = o[0].strip().replace('Pred Tree: ', '')
        gold = o[1].strip().replace('Gold Tree: ', '')
        gold = gold.replace('(', '').replace(')', '').split()
        gold = ' '.join(gold).lower()
        model_outs.append((pred, gold))

print(len(model_outs))

with open('test_ground-truth.txt', 'r') as ground, open('mmodal_out.align.txt', 'w') as align:
    miss = 0
    for g in ground:
        g_filt = g.strip().replace('.', '').replace('(', '').replace(')', '').split()
        g_str = ' '.join(g_filt).lower()
        # print(g_str)
        match_pred = ''
        for pred, gold in model_outs:
            pred_str = pred.replace('(', '').replace(')', '')
            if gold == g_str:
                # print(g_str)
                # print(pred_str)
                match_pred = pred
                break

        if match_pred != '':
            align.write('Pred: ' + match_pred + '\t' + 'Gold: ' + g + '\n')
        else:
            miss += 1
    print(miss)

    # print(ground_order)
#
#
# for ground in ground_order:
#     # print(ground)
#     for pred in model_outs:
#         pred_str = pred.replace('(', '').replace(')', '')
#         if pred_str == ground:
#             print(pred_str)

    # match = [pred for pred in model_outs if pred.replace('(', '').replace(')', '') == ground]

    # print(match)
