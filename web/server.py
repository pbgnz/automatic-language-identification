import json
import math
import pickle
from flask import Flask, render_template, request
from corpus import Corpus
from ngram import NGram


app = Flask(__name__)
with open('web/model/web.pkl', 'rb') as f:
    models = pickle.load(f)


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/predict', methods=['POST'])
def predict():
    retJson = {"unigram": "sentence too long", "bigram": "sentence too long"}
    sentence = request.form['sentence']
    if len(sentence) < 4000:
        unigram, bigram = handleSentence(sentence)
        retJson["unigram"] = unigram
        retJson["bigram"] = bigram
        return json.dumps(retJson)
    else:
        return json.dumps(retJson)


def handleSentence(sentence):
    tokens = [Corpus.tokenize(sentence)]
    unigram = ""
    bigram = ""
    for line in tokens:
        logTotal = {"english": 0, "french": 0, "spanish": 0}
        for c in line:
            for gram in models:
                f = gram[0].get_model()[c]
                lang = ""
                if "EN" in gram[0].name:
                    lang = "english"
                elif "FR" in gram[0].name:
                    lang = "french"
                else:
                    lang = "spanish"
                logTotal[lang] += math.log10(f)
        unigram = get_language(logTotal)
        logTotal["english"] = 0
        logTotal["french"] = 0
        logTotal["spanish"] = 0
        tmp = tokens[0]
        pairs = [a + b for a, b in zip(tmp, tmp[1:])]
        for p in pairs:
            for gram in models:
                f = gram[1].get_model()[(p[0], p[1])]
                lang = ""
                if "EN" in gram[0].name:
                    lang = "english"
                elif "FR" in gram[0].name:
                    lang = "french"
                else:
                    lang = "spanish"
                logTotal[lang] += math.log10(f)
        bigram = get_language(logTotal)
        return unigram, bigram


def get_language(logTotal):
    if (logTotal["french"] > logTotal["english"]) and (logTotal["french"] > logTotal["spanish"]):
        return "French"
    elif (logTotal["english"] > logTotal["french"]) and (logTotal["english"] > logTotal["spanish"]):
        return "English"
    else:
        return "Spanish"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
