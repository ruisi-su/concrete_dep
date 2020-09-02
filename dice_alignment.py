import argparse
import math
import numpy as np
from tqdm import tqdm
from collections import defaultdict

# A Dice-coefficient based aligner, roughly based on:
# https://www.aclweb.org/anthology/P97-1063.pdf
# I Dan Melamud. "A Word-to-Word Model of Translational Equivalence". ACL 1997

parser = argparse.ArgumentParser(description="Parse arguments")
parser.add_argument("srctrg_file", help="Source file")
parser.add_argument("--thresh", default=-1.0e5, help="The threshold")
parser.add_argument("--eqn", default="dice", help="What type of equation to use (dice/pmi)")
args = parser.parse_args()

srctrg_cnt = defaultdict(lambda: 0)
src_cnt = defaultdict(lambda: 0)
trg_cnt = defaultdict(lambda: 0)
tot_cnt = 0

with open(args.srctrg_file, 'r') as fsrctrg:
  for lsrctrg in tqdm(fsrctrg):
    lsrctrg = lsrctrg.strip()
    if not lsrctrg:
      continue
    tot_cnt += 1.0
    print(lsrctrg)
    if len(lsrctrg.split(' ||| ') == 1:
      continue
    lsrc, ltrg = lsrctrg.split(' ||| ')
    wsrc = set(lsrc.lower().strip().split())
    wtrg = set(ltrg.lower().strip().split())
    for s in wsrc:
      src_cnt[s] += 1.0
      for t in wtrg:
        srctrg_cnt[s,t] += 1.0
    for t in wtrg:
      trg_cnt[t] += 1.0

if args.eqn == 'dice':
  srctrg_score = {(s,t): 2*v/(src_cnt[s]+trg_cnt[t]) for ((s,t), v) in tqdm(srctrg_cnt.items())}
elif args.eqn == 'pmi':
  srctrg_score = {(s,t): math.log(v*tot_cnt/src_cnt[s]/trg_cnt[t]) for ((s,t), v) in tqdm(srctrg_cnt.items())}
else:
  raise ValueError(f'Illegal equation {args.eqn}')


with open(args.srctrg_file, 'r') as fsrctrg:
  for lsrctrg in tqdm(fsrctrg):
    lsrctrg = lsrctrg.strip()
    if not lsrctrg:
      print()
      continue
    #print(lsrctrg)
    lsrc, ltrg = lsrctrg.split(' ||| ')
    wsrc = list(set(lsrc.lower().strip().split()))
    wtrg = list(set(ltrg.lower().strip().split()))
    dsrctrg = np.zeros( (len(wsrc), len(wtrg)) )
    for i, s in enumerate(wsrc):
      for j, t in enumerate(wtrg):
        dsrctrg[i,j] = srctrg_score[s,t]
    # print(wsrc)
    # print(wtrg)
    # print(dsrctrg)
    idsrc, idtrg = np.unravel_index(np.argmax(dsrctrg), dsrctrg.shape)
    aligns = []
    while dsrctrg[idsrc,idtrg] > args.thresh:
      aligns.append(f'{wsrc[idsrc]}:{wtrg[idtrg]}:{dsrctrg[idsrc,idtrg]:.3f}')
      dsrctrg[idsrc,:] = args.thresh
      dsrctrg[:,idtrg] = args.thresh
      idsrc, idtrg = np.unravel_index(np.argmax(dsrctrg), dsrctrg.shape)
    print(' '.join(aligns))
