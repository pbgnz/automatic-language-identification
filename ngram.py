#!/bin/python

import math
import re
import string
from decimal import Decimal
from corpus import Corpus
from collections import Counter
from functools import reduce


class NGram:
    """
    NGram is similar to an abstract factory.
    It is used to create Unigrams and Bigrams
    """
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
        self.model = dict({el:0 for el in string.ascii_lowercase})
        self.test = [] # the results of the perdictions
    
    def train(self, training_corpus):
        self.corpus = Corpus(training_corpus)
        self.tokenized = self.corpus.clean_and_tokenize()
        self.count = Counter([(self.tokenized[i]) for i in range(0,len(self.tokenized)-1)])
        self.print_model(self.count)

    def predict(self, test_corpus):
        test = Corpus(test_corpus).sanitize()
        count = 1
        for line in test:
            outfile = open("output/debug/{}-{}-{}.txt".format(count,self.name,self.corpus.name), "w+")
            count += 1
            tokens = []
            logTotal = 0
            outfile.write(' '.join(line)+'\n\n')
            outfile.write('UNIGRAM MODEL trained on: {}\n\n'.format(self.corpus.name))
            tokens.append(Corpus.tokenize(line))
            line_result = []
            for line in tokens:
                for c in line:
                    outfile.write('UNIGRAM: {}\n'.format(c))
                    f = self.model[c]
                    logTotal += math.log10(f)
                    line_result.append((c, f,logTotal))
                    outfile.write('MODEL PROBABILITY: P({}) = {:.4e} ==> log prob of sequence so far: {:.4e}\n'.format(c, f, logTotal))
            self.test.append(line_result)
            outfile.close()

    def print_model(self, ngram):
        outfile = open("output/{}.txt".format(self.name), "w")
        for letter in string.ascii_lowercase:
            letter_frequency = ngram.get(letter)
            if letter_frequency is not None:
                letter_frequency += letter_frequency + self.delta
            else:
                letter_frequency = self.delta
            total_characters = len(self.tokenized) + self.delta * self.vocabulary
            self.model[letter] = Decimal(letter_frequency/total_characters)
            outfile.write("P({}) = {:.4e}\n".format(letter, self.model[letter]))
        outfile.close()

    def get_model(self):
        return self.model

    def get_predictions(self):
        return self.test


class Bigram:

    def __init__(self, delta, name, vocabulary):
        self.delta = delta
        self.name = name
        self.vocabulary = vocabulary
        self.corpus = [] # train corpus
        self.tokenized = [] # tokenized corpus
        self.count = [] # Counter
        self.pairs = [(a,b) for a in string.ascii_lowercase for b in string.ascii_lowercase]
        self.model = dict({el:0 for el in self.pairs})
    
    def train(self, training_corpus):
        self.corpus = Corpus(training_corpus)
        self.tokenized = self.corpus.clean_and_tokenize()
        self.unigram = Counter([(self.tokenized[i]) for i in range(0,len(self.tokenized)-1)])
        self.count = Counter([(self.tokenized[i],self.tokenized[i+1]) for i in range(0,len(self.tokenized)-1)])
        self.print_model(self.count)

    def predict(self, test_corpus):
        test = Corpus(test_corpus).sanitize()
        count = 1
        for line in test:
            outfile = open("output/debug/{}-{}-{}.txt".format(count,self.name,self.corpus.name), "w+")
            tokens = []
            logTotal = 0
            outfile.write(' '.join(line)+'\n\n')
            outfile.write('BIGRAM MODEL:  trained on: {}\n\n'.format(self.corpus.name))
            tokens.append(Corpus.tokenize(line))
            tmp = tokens[0]
            count += 1
            if len(tmp) % 2 != 0:
                tmp = tmp[:-1]
            pairs = [tmp[i]+tmp[i+1] for i in range(0,len(tmp),2)]
            for p in pairs:
                outfile.write('BIGRAM: {}{}\n'.format(p[0],p[1]))
                f = self.model[(p[0],p[1])]
                logTotal += math.log10(f)
                outfile.write('MODEL PROBABILITY: P({}|{}) = {:.4e} ==> log prob of sequence so far: {:.4e}\n'.format(p[1], p[0], f, logTotal))
            outfile.close()

    def print_model(self, ngram):
        character_count = dict({el:0 for el in string.ascii_lowercase})
        for c in character_count:
            letter_frequency = self.unigram.get(c)
            if letter_frequency is not None:
                character_count[c] = letter_frequency + self.vocabulary * self.delta
            else:
                character_count[c] = self.vocabulary
        outfile = open("output/{}.txt".format(self.name), "w")
        for pair in self.pairs:
            pair_frequency = ngram.get(pair)
            if pair_frequency is not None:
                pair_frequency += pair_frequency + self.delta
            else:
                pair_frequency = self.delta
            self.model[pair] = Decimal(pair_frequency/character_count[pair[0]])
            outfile.write("P({}|{}) = {:.4e}\n".format(pair[1], pair[0], self.model[pair]))
        outfile.close()

    def get_model(self):
        return self.model
