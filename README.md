# Concrete Dependency Induction

This is the implementation for the paper _Dependency Induction Through the Lens of Visual Perception_. We implemented based on the lpcfg [Lexicalized-PCFG](https://github.com/neulab/neural-lpcfg).

## Preprocess-Alignment

To generate the alignment, concatinate all caption and label pairs for all splits, and use the `make_input` argument in `align.py` under `data/proc_data` directory

We provided the alignment input and output in the `data/proc_data` folder. Periods are stripped.

## Preprocess-Dice scores
To get the dice alignment scores:

```
python dice_alignment.py {alignment_file} > {file_prefix.out}
```
The dependencies (`.conllx` files) for MSCOCO are generated using [this repo](https://github.com/hankcs/TreebankPreprocessing)

Dependencies folders should be placed in the `lpcfg/data` with the folder name `dep` to use during `preprocess.py`

## Train

Sample training scripts are provided in `lpcfg/scripts` folder. They can be executed `sh scripts/{script_you_want_to_run}.sh` in the `lpcfg` directory. Evaluation requires setting the argument `--mode test` when calling `train.py`

## Baseline
```python preprocess.py --vocabsize 100000 --replace_num 1 --dep --outputfile {OUTPUT_PATH}```

## Coupling method
*requires the input file for dice alignment, and the output file contains the alignment pairs with scores*

```
python preprocess.py --vocabsize 100000 --replace_num 1 --dep --outputfile {OUTPUT_PATH} --align_input {PATH_TO_ALIGN_INPUT_FILE} --align_output {PATH_TO_ALIGN_OUTPUT_FILE}
```

## Concreteness
*requires the original file for each English word with it's corresponding concreteness scores*

```
python preprocess.py --vocabsize 100000 --replace_num 1 --dep --outputfile {OUTPUT_PATH} --concrete_file {PATH_TO_CONCRETE_FILE}
```
