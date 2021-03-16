# Multimodal Grammar Induction

This repo adds visual priors to the lexicalized-pcfg, which can be found in here https://github.com/neulab/neural-lpcfg.

# Preprocess

## Baseline
```python preprocess.py --vocabsize 100000 --replace_num 1 --dep --outputfile {OUTPUT_PATH}```

## Coupling method
*requires the input file for dice alignment, and the output file contains the alignment pairs with scores*

```python preprocess.py --vocabsize 100000 --replace_num 1 --dep --outputfile {OUTPUT_PATH} --align_input {PATH_TO_ALIGN_INPUT_FILE} --align_output {PATH_TO_ALIGN_OUTPUT_FILE}```

## Concreteness
*requires the original file for each English word with it's corresponding concreteness scores*

```python preprocess.py --vocabsize 100000 --replace_num 1 --dep --outputfile {OUTPUT_PATH} --concrete_file {PATH_TO_CONCRETE_FILE}```
