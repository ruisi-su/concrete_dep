This folder contains the input files and the alignments (`.output` files) with four different ways to split the words in the frames.

fast_align was used for the alignments with the intersect heuristic for merging forward and reverse alignments.

Example:

`caption`: A restaurant has modern wooden tables and chairs .

`frames`: dining_place_dining-room	dining_agent_people


`none`: dining_place_dining-room	dining_agent_people

`split_verb`: dining place_dining-room agent_people

`split_noverb`: dining dining-room people

`split_all`: dining place dining-room agent people
