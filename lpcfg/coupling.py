import numpy as np
'''
The coupling heuristics does not follow a set of rules. Rather, it uses labels to couple
arguments around their predicates.
For example:
caption: 0-A 1-girl 2-is 3-eating 4-a 5-slice 6-of 7-cheesecake 8-.
frame labels: eat (predicate), woman (argument), cake (argument)
align captions with labels: 1-girl:woman, 3-eat(lemmatized):eat, 7-cheesecake:cake

predicate is at index 3, arguments are at index 1 and index 7, respectively.

Then we return spans that couple each argument with the predicate, and mark the predicate as
head of the span:
(start, end, head) as [s, t)
(1, 4, 3) -> (eating-girl is eating)
(3, 8, 3) -> (eating-eating a slice of cheesecake)

align_in: _ restaurant _ modern wooden table _ chair _ ||| dine restaurant people
align_out: 	

'''



def couple(align_in, align_out, ctvb, ctnvb):
	lcap, lfra = align_in.split(' ||| ')
	lali = align_out.lower().strip().split()
	print(lali)
	lali = [a for a in lali if float(a.split(':')[-1]) >= 0.0] # remove alignments with negative scores
	wcap = lcap.lower().strip().split()
	wfra = lfra.lower().strip().split()
	# get indices in caption 
	ifra = [0]*len(wfra)
	for i, w in enumerate(wfra):
		w_c_i = None 
		for ali in lali:
			alis = ali.split(':')
			if len(alis) > 3:
				c = ':'.join(alis[:2])
				f = alis[2]
				score = alis[3]
			else:
				c, f, score = ali.split(':')
			if w == f:
				w_c_i = wcap.index(c) 
				ifra[i] = w_c_i
				# exit alignment lookup
				break
		if not w_c_i:
			ifra[i] = -1

	# frame labels are in the order: [pred, arg1, arg2, ..., argn]
	# if predicate is never found in the captions
	# couple each pair of argument in order (index of the caption)
	# allow both arguments be heads
	spans = []
	if ifra[0] == -1:
		ctnvb += 1
		ifra = [x for x in ifra if x != -1]
		ifra.sort() # sort by order of occurance in caption
		for i in range(1, len(ifra)):
			spans.append((ifra[i-1], ifra[i]+1, ifra[i-1]))
			spans.append((ifra[i-1], ifra[i]+1, ifra[i]))
	else:
		ctvb += 1

		ifra = [x for x in ifra if x != -1]
		d_pred = [x-ifra[0] for x in ifra]
		arg_sort = np.argsort([abs(dd) for dd in d_pred]) # sort by abs dist
		for i in range(1, len(arg_sort)):
			d = d_pred[arg_sort[i]]
			if d < 0:
				spans.append((ifra[arg_sort[i]], ifra[0]+1, ifra[0]))
			else:
				spans.append((ifra[0], ifra[arg_sort[i]]+1, ifra[0]))
	return spans, ctvb, ctnvb 


# s, _, _ = couple('_ restaurant _ modern wooden table _ chair _ ||| dine restaurant people',
# 			'table:restaurant:0.201 restaurant:dine:0.055 chair:people:0.025', 0, 0)
# print(s)

# align_input = '../data/VGNSL_split/traindevtest.frame.cap-frame.split_noverb'
# align_output = '../data/VGNSL_split/traindevtest.frame.cap-frame.split_noverb.out.no-lemmatization-frame'
# with open(align_input, 'r') as align_in, open(align_output, 'r') as align_out:
# 	ctvb = ctnvb = 0
# 	for ai, ao in zip(align_in, align_out):
# 		ai = ai.strip()
# 		ao = ao.strip()
# 		if (ai != '') and (ao != ''):
# 			_, ctvb, ctnvb = couple(ai, ao, ctvb, ctnvb)
# 	print(f'num of sents with vb aligned: {ctvb} \n num of sents with no vb: {ctnvb}')



