import os
import pickle
import sys
from corpus import Corpus
from ngram import NGram

if __name__ == '__main__':

    """
    train the models using the corpora in the data folder.
    make sure that the files follow the convention;
    the english file must contain "en", the french file "fr", 
    and spanish file "sp"
    """
    ngrams = []
    corpora = ["data/en.txt", "data/sp.txt", "data/fr.txt"]

    for corpus in corpora:
        _, tail = os.path.split(corpus)
        name = tail.split(".")[0]
        if "en" in name:
            name = "EN"
        elif "fr" in name:
            name = "FR"
        else:
            name = "SP"
        unigram = NGram.create(degree=1,delta=0.5, name="unigram"+name)
        unigram.train(corpus)
        bigram = NGram.create(degree=2,delta=0.5, name="bigram"+name)
        bigram.train(corpus)
        ngrams.append((unigram, bigram))

    # pickle the ngrams
    with open('web/model/web.pkl', 'wb') as f:
        pickle.dump(ngrams, f)
