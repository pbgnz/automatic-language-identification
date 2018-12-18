# Automatic-Language-Identification
A probabilistic language identification system that identifies the language of a sentence 

## Requirements
1. Python 2.7.15
2. Python 3.7.0
3. Pip

### Installation
``` bash
pip install -r requirements.txt
```

## Detailed Usage

### General

``` bash
ali is a probabilistic language identification system that identifies the langue of a sentence.

usage: ali [-v] (-c TRAIN-CORPUS)* [-t TEST-FILE]
    -v Prints debugging messages.
    -c Specifies the training text(s) for the language.
    -t Specifies the test set for the model.
```

### Examples

generate an unigram and a bigram for each corpus and predict the training sentences using the later.
``` bash
python ali.py -c "corpora/en-moby-dick.txt" -c "corpora/es-don-quijote.txt" -c "corpora/fr-vingt-mille-lieues-sous-les-mers.txt" -t "corpora/first10TestSentences.txt"
```
outputs: see `output/output.md`