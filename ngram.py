#!/bin/python

import math
import re
import sys
import string
from decimal import Decimal
from corpus import Corpus
from collections import Counter
from functools import reduce


class NGram:    
    @staticmethod
    def create(degree=1, delta=0.5, name="", vocabulary=26):
        if degree == 1:
            return Unigram(delta, name, vocabulary)
        else:
            return Bigram(delta, name, vocabulary)


class Unigram:

    def __init__(self, delta, name, vocabulary):
        self.delta = delta
        self.name = name
        self.vocabulary = vocabulary
        self.corpus = [] # train corpus
        self.tokenized = [] # tokenized corpus
        self.count = [] # Counter
        self.unigram = []
    
    def train(self, training_corpus):
        self.corpus = Corpus(training_corpus)
        self.tokenized = self.corpus.clean_and_tokenize()
        self.count = Counter([(self.tokenized[i]) for i in range(0,len(self.tokenized)-1)])
        self.print_model(self.count)

    # def predict(self, test_corpus):
    #     test = Corpus(test_corpus).cleans()


    def print_model(self, ngram):
        outfile = open("output/{}.txt".format(self.name), "w")
        for letter in string.ascii_lowercase:
            letter_frequency = ngram.get(letter)
            if letter_frequency is not None:
                letter_frequency += letter_frequency + self.delta
            else:
                letter_frequency = self.delta
            total_characters = len(self.tokenized) + self.delta * self.vocabulary
            outfile.write("P({}) = {:.4e}\n".format(letter, Decimal(letter_frequency/total_characters)))
        outfile.close()


class Bigram:

    def __init__(self, delta, name, vocabulary):
        self.delta = delta
        self.name = name
        self.vocabulary = vocabulary
        self.corpus = [] # train corpus
        self.tokenized = [] # tokenized corpus
        self.count = [] # Counter
        self.test_set = []
    
    def train(self, training_corpus):
        self.corpus = Corpus(training_corpus)
        self.tokenized = self.corpus.clean_and_tokenize()
        self.unigram = Counter([(self.tokenized[i]) for i in range(0,len(self.tokenized)-1)])
        self.count = Counter([(self.tokenized[i],self.tokenized[i+1]) for i in range(0,len(self.tokenized)-1)])
        self.print_model(self.count)

    # def predict(self, test_corpus):
    #     test = Corpus(test_corpus).cleans()


    def print_model(self, ngram):
        character_count = dict({el:0 for el in string.ascii_lowercase})
        for c in character_count:
            letter_frequency = self.unigram.get(c)
            if letter_frequency is not None:
                character_count[c] = letter_frequency + self.vocabulary * self.delta
            else:
                character_count[c] = self.vocabulary
        pairs = [(a,b) for a in string.ascii_lowercase for b in string.ascii_lowercase]
        outfile = open("output/{}.txt".format(self.name), "w")
        for pair in pairs:
            pair_frequency = ngram.get(pair)
            if pair_frequency is not None:
                pair_frequency += pair_frequency + self.delta
            else:
                pair_frequency = self.delta
            outfile.write("P({}|{}) = {:.4e}\n".format(pair[0], pair[1], Decimal(pair_frequency/character_count[pair[0]])))
        outfile.close()


bigram = NGram.create(degree=2,name="bigramEN", delta=0.5)
bigram.train("corpora/fr-vingt-mille-lieues-sous-les-mers.txt")

# test = Corpus('corpora/first10TestSentences.txt').cleans()
# count = 1
# for line in test:
#     print(line)
#     outfile = open("output/out{}.txt".format(count), "w+")
#     count += 1
#     tokens = []
#     french = 1
#     english = 1
#     spanish = 0
#     outfile.write(' '.join(line)+'\n\n')
#     outfile.write('UNIGRAM MODEL:\n\n')
#     tokens.append(tokenize(line))
#     for line in tokens:
#         for c in line:
#             outfile.write('UNIGRAM: {}\n'.format(c))
#             f = Decimal(fr.get(c)/len(tokensFR))
#             e = Decimal(en.get(c)/len(tokensEN))
#             french += math.log10(f)
#             english += math.log10(e)
#             outfile.write('FRENCH: P({}) = {:.4e} ==> log prob of sequence so far: {:.4e}\n'.format(c, f, french))
#             outfile.write('ENGLISH: P({}) = {:.4e} ==> log prob of sequence so far: {:.4e}\n\n'.format(c, e, english))
#     if (-french > -english) and (-french > -spanish):
#         outfile.write('According to the unigram model, the sentence is in French')
#     elif (-english > -french) and (-english > -spanish):
#         outfile.write('According to the unigram model, the sentence is in English')
#     else:
#         outfile.write('According to the unigram model, the sentence is in Spanish')
#     outfile.close()
