#!/bin/python

import argparse
import os
from ngram import NGram


def demo(verbose, corpora, test):
    ngrams = []
    for corpus in corpora:
        _, tail = os.path.split(corpus[0])
        name = tail.split(".")[0]
        print(name)
        if "en" in name:
            name = "EN"
        elif "fr" in name:
            name = "FR"
        else:
            name = "SP"
        unigram = NGram.create(degree=1,delta=0.5, name="unigram"+name)
        unigram.train(corpus[0])
        unigram.predict(test)
        bigram = NGram.create(degree=2,delta=0.5, name="bigram"+name)
        bigram.train(corpus[0])
        bigram.predict(test)
        ngrams.append((unigram, bigram))



parser = argparse.ArgumentParser(description='ali is a probabilistic language identification system that identifies the langue of a sentence.')

parser.add_argument("-v",
                    help="Prints debugging messages.",
                    action='store_true',)
parser.add_argument("-c",
                    help="Specifies the training text(s) for the language.",
                    action='append', nargs='+',
                    metavar='corpus_text_file')
parser.add_argument("-t",
                    help="Specifies the test set for the model.",
                    metavar='test_set_file')

args = parser.parse_args()
verbose = args.v
corpora = args.c
test_file = args.t

demo(verbose, corpora, test_file)
