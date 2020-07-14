# Automatic-Language-Identification
A probabilistic language identification system that identifies the language of a sentence 

[Visit demo website. Takes couple of seconds to launch the app](https://automatic-language-detection.herokuapp.com/)

## Requirements
1. Python 2.7.15
2. Python 3.7.0
3. Pip

## Installation
``` bash
pip install -r requirements.txt
```

## Detailed Usage

#### CLI

``` bash
ali is a probabilistic language identification system that identifies the langue of a sentence.

usage: ali [-v] (-c TRAIN-CORPUS)* [-t TEST-FILE]
    -v Prints debugging messages.
    -c Specifies the training text(s) for the language.
    -t Specifies the test set for the model.
```

**Examples**

generate an unigram and a bigram for each corpus and predict the training sentences using the later.
``` bash
python ali.py -c "data/en.txt" -c "data/sp.txt" -c "data/fr.txt" -t "data/first10TestSentences.txt"
```
outputs: see `output/output.md`

#### Web App

Train the models
``` bash
python train.py
```

Run the server
``` bash
python server.py
# or
gunicorn server:app
```