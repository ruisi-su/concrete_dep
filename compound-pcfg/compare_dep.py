import tqdm
import sys

same = 0
diff = 0
with open(sys.argv[1], 'r') as t1, open(sys.argv[2], 'r') as t2, open(sys.argv[3], 'r') as t3, open(sys.argv[4], 'w') as out:
    for l1, l2, l3 in zip(t1,t2, t3):

        pred_1, _ = l1.rstrip().split('\t')
        pred_2, _ = l2.rstrip().split('\t')
        pred_3, _ = l3.rstrip().split('\t')
        pred_1 = pred_1.split(' ')[2:]
        pred_2 = pred_2.split(' ')[2:]
        pred_3 = pred_3.split(' ')[2:]

        if (pred_1 == pred_2) and (pred_2 == pred_3) and (pred_3 == pred_1):
            same += 1
            continue
        else:
            diff += 1
            out.write('--------------'+'\n')
            out.write('file 1 : ' +' '.join(pred_1) + '\n' + 'file 2 : ' + ' '.join(pred_2) + '\n' + 'file 3 : ' + ' '.join(pred_3) + '\n')
    out.write(str(same) + ' identical outputs ' + str(diff) + ' different outputs' )
