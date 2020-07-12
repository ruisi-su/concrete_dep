import spacy
import sys
nlp = spacy.load("en_core_web_md")

threshold = 0.5

with open(sys.argv[1], 'r') as alignment_file:
  for aline in alignment_file:
    alignments = aline.strip().split(' ')
    if len(alignments) == 1:
        print('')
        continue
    # filter by similarity
    aitems_filt = []
    for alignment in alignments:
      align_list = alignment.split(':')
      if len(align_list) == 4:
          cap = align_list[:2]
          frame = align_list[2]
          score = align_list[3]
      else:
          cap, frame, score = align_list
      cap_doc = nlp(cap)
      frame_doc = nlp(frame)
      if cap_doc.similarity(frame_doc) > threshold:
        aitems_filt.append(alignment)
    aline_filt = ' '.join(aitems_filt)
    print(aline_filt)
