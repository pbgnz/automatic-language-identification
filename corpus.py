import os
import re
import string


class Corpus:
    """
    Corpus is used for handling text files.
    """

    def __init__(self, file_path):
        file = open(file_path)
        self.corpus = file.readlines()
        file.close()
        _, tail = os.path.split(file_path)
        self.name = tail

    @staticmethod
    def clean(corpus):
        """
        Separates each line of the corpus by words and removes punctuation.

        >>> clean('first10TestSentences.txt')
        [['What', 'will', 'the', 'Japanese', 'economy', 'be', 'like', 'next', 'year'], 
        ['She', 'asked', 'him', 'if', 'he', 'was', 'a', 'student', 'at', 'this', 'school'], 
        ['Im', 'OK'], ['Birds', 'build', 'nests'], ['I', 'hate', 'AI'], ['Loiseau', 'vole'], 
        ['Woody', 'Allen', 'parle'], ['Estce', 'que', 'larbitre', 'est', 'la'],
        ['Cette', 'phrase', 'est', 'en', 'anglais'], ['Jaime', 'lIA']]

        :param string corpus: String path of the corpus text file
        :return list: List of lists.
        """
        # seperate the corpus by words
        words_split = []
        for line in corpus:
            words_split.append(line.split())

        # Remove punctuation
        regex = re.compile('[%s]' % re.escape(string.punctuation))

        no_punctuation = []
        for review in words_split:
            new_review = []
            for token in review: 
                new_token = regex.sub(u'', token)
                if not new_token == u'':
                    new_review.append(new_token)
            no_punctuation.append(new_review)
        # remove empty lists
        return [x for x in no_punctuation if x != []]

    @staticmethod
    def tokenize(cleaned_text):
        """
        Flattens a list of lists and splits all the words into characters.

        >>> tokenize([['the', 'Japanese', 'economy'],['next','year']])
        ['t', 'h', 'e', 'j', 'a', 'p', 'a', 'n', 'e', 's', 'e', 'e', 'c', 
        'o', 'n', 'o', 'm', 'y', 'n', 'e', 'x', 't', 'y', 'e', 'a', 'r']

        :param list cleaned_text: List of lists.
        :return list: List of characters.
        """
        # flatten the list
        flattened = [val for sublist in cleaned_text for val in sublist]

        # Seperate by character
        tokens = []
        for word in flattened:
            l = list(word)
            # only add ascii letters
            for c in l:
                if c in string.ascii_uppercase:
                    tokens.extend(c.lower())
                elif c in string.ascii_lowercase:
                    tokens.extend(c)
        return tokens

    def clean_and_tokenize(self):
        return Corpus.tokenize(Corpus.clean(self.corpus))

    def sanitize(self):
        return Corpus.clean(self.corpus)
