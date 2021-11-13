# Lexicalized Compound Probabilistic Context-Free Grammars (L-PCFG)
The base code of the L-PCFG model is adapted from the paper 
[The Return of Lexical Dependencies: Neural Lexicalized PCFGs](about:blank)  

## Dependencies
The code was tested in `python 3.6` and `pytorch 1.4`. We also require the `nltk` package if creating
the processed data from the raw PTB dataset.

## Training
To illustrate the training command, we provide a toy script which could be used on normal machines or on slurm clusters:

Running on normal machine:
```
chmod +x script/toy.sbatch
CUDA_VISIBLE_DEVICES=[gpu_id] bash script/toy.sbatch
```

Deploy on clusters:
```
sbatch script/toy.sbatch
```

## Testing
Change `mode` from `train` to `test` and provide the test data. Use
```
python train.py --help
```
for usage. 

## Acknowledgements
My implementation is largely based on [CompPCFG](https://github.com/harvardnlp/compound-pcfg)

## License
MIT
