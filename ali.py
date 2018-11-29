#!/bin/python

import argparse
import math
import os
from corpus import Corpus
from ngram import NGram


def demo(verbose, corpora, test):
    ngrams = []
    if verbose:
        print("Creating the unigrams and bigrams for the corpora")
    for corpus in corpora:
        _, tail = os.path.split(corpus[0])
        name = tail.split(".")[0]
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

    if verbose:
        print("Generating output files.")
    count = 1
    test = Corpus(test).sanitize()
    for line in test:
        outfile = open("output/out{}.txt".format(count), "w+")
        count += 1
        tokens = []
        outfile.write(' '.join(line)+'\n\n')
        outfile.write('UNIGRAM MODEL:\n')
        tokens.append(Corpus.tokenize(line))
        for line in tokens:
            logTotal = {"english":0, "french":0, "spanish": 0}
            for c in line:
                outfile.write('\nUNIGRAM: {}\n'.format(c))
                for gram in ngrams:
                    f = gram[0].get_model()[c]
                    lang = ""
                    if "EN" in gram[0].name:
                        lang = "english"
                    elif "FR" in gram[0].name:
                        lang = "french"
                    else:
                        lang = "spanish"
                    logTotal[lang] += math.log10(f)
                    outfile.write('{}: P({}) = {:.4e} ==> log prob of sequence so far: {:.4e}\n'.format(gram[0].name, c, f, logTotal[lang]))
            if (logTotal["french"] > logTotal["english"]) and (logTotal["french"] > logTotal["spanish"]):
                outfile.write('\nAccording to the unigram model, the sentence is in French\n')
            elif (logTotal["english"] > logTotal["french"]) and (logTotal["english"] > logTotal["spanish"]):
                outfile.write('\nAccording to the unigram model, the sentence is in English\n')
            else:
                outfile.write('\nAccording to the unigram model, the sentence is in Spanish\n')
        outfile.write('----------------\nBIGRAM MODEL:\n\n')
        logTotal["english"] = 0
        logTotal["french"] = 0
        logTotal["spanish"] = 0
        tmp = tokens[0]
        if len(tmp) % 2 != 0:
            tmp = tmp[:-1]
        pairs = [tmp[i]+tmp[i+1] for i in range(0,len(tmp),2)]
        for p in pairs:
            outfile.write('\nBIGRAM: {}{}\n'.format(p[0],p[1]))
            for gram in ngrams:
                f = gram[1].get_model()[(p[0],p[1])]
                lang = ""
                if "EN" in gram[0].name:
                    lang = "english"
                elif "FR" in gram[0].name:
                    lang = "french"
                else:
                    lang = "spanish"
                logTotal[lang] += math.log10(f)
                outfile.write('{}: P({}|{}) = {:.4e} ==> log prob of sequence so far: {:.4e}\n'.format(gram[1].name, p[1], p[0], f, logTotal[lang]))
        if (logTotal["french"] > logTotal["english"]) and (logTotal["french"] > logTotal["spanish"]):
            outfile.write('\nAccording to the unigram model, the sentence is in French\n')
        elif (logTotal["english"] > logTotal["french"]) and (logTotal["english"] > logTotal["spanish"]):
            outfile.write('\nAccording to the unigram model, the sentence is in English\n')
        else:
            outfile.write('\nAccording to the unigram model, the sentence is in Spanish\n')
    outfile.close()




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
