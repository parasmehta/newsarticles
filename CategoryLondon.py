# -*- coding: utf-8 -*-

import nltk, gensim, csv, re
import matplotlib.pyplot as plt
from nltk.tokenize import WordPunctTokenizer
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models, utils
from wordcloud import WordCloud


# gets the tokens from text by breaking it into sentences, then words and removing punctuation
def gettokens(text):
    text = text.lower()
    tokens = []

#    tokenizer = RegexpTokenizer(r'\w+')

    for sent in sent_tokenize(text.decode('utf-8')):
        for word in utils.lemmatize(sent):
            tokens.append(word)

#    print "Lemmatized tokens", tokens

#         for word in word_tokenize(sent):
#             if word == "n't":
#                 word = 'not'
#
#                 # if €","–" in word:
#                 #   continue
#             #            if re.match(r'^\w+$', word):
#             #                tokens.append(word)
#
#             if word in ' :,-.\'':
#                 continue
#
# #            if word in ['will', 'also', 'said', 'told', 'man', 'call', '\'s']:
# #                continue
#
#            tokens.append(word)

    # return filter(lambda word: word not in ',-.', tokens)
    return tokens


# removes stop words and stems tokens
def processtokens(doc):
    tokens = gettokens(doc)

    # create English stop words list
    en_stop = get_stop_words('en')

    otherstopwords = ['appear', 'time', 'give', 'month', 'ask', 'twitter', 'used', 'include', 'today', 'duggan', 'describe', 'dog', 'see', 'police', 'court', 'pm', 'anonymously', 'year', 'old', 'take', 'find', 'get', 'anyone', 'crimestopper', 'incident', 'person', 'information', 'contact', 'will', 'also', 'say', 'tell', 'told', 'man', 'call', '\'s', 'one', 'two', 'last', '0800', 'polouse', 'inform', 'london', 'be', 'have', 'mr', 'officer', 'go', 'make']

    stopped_tokens = [i for i in tokens if i[:-3] not in en_stop and i[:-3] not in otherstopwords]

    # print stopped_tokens

    return stopped_tokens



    # Create p_stemmer of class PorterStemmer
    # p_stemmer = PorterStemmer()
    #
    # # stem token
    # stemmed_tokens = []
    # for i in stopped_tokens:
    #     stemmed_tokens.append(p_stemmer.stem(i))

#    print stemmed_tokens

#    return stemmed_tokens


# runs LDA on the processed tokens
def train_model(articletexts):
    # list for tokenized documents in loop
    texts = []

    # loop through document list
    for i in articletexts:
        stemmed_tokens = processtokens(i)

        # add tokens to list
        texts.append(stemmed_tokens)

    dictionary = corpora.Dictionary(texts)

    corpus = [dictionary.doc2bow(text) for text in texts]

#    print(corpus[0])

    numtopics = 4
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=numtopics, id2word=dictionary, passes=20)

    # print(ldamodel.print_topics(num_topics=6, num_words=4))

    print "Topics: "
    print(ldamodel.print_topics(num_topics=numtopics))

    createwc(ldamodel, numtopics)
    return ldamodel


def read_articles(filename):
    texts = []
    numarticles = 0

    with open(filename, 'rb') as csvfile:
        filer = csv.reader(csvfile, delimiter='|')

        next(filer, None) # skip header

        for row in filer:
            if len(row) > 0:

                title = row[0].strip()

                if not title.endswith("."):
                    title += ". "

                print title
                numarticles += 1

                sent = title + row[2]     # text = title + body

                texts.append(sent)
            else:
                print "row has 0 columns: " + row

    print numarticles, "articles read"

    return texts


def createwc(ldamodel, numtopics):
    # final_topics = open(os.path.join(MODELS_DIR, "final_topics.txt"), 'rb')
    final_topics = ldamodel.print_topics(num_topics=numtopics)
    curr_topic = 0
    for line1 in final_topics:
        line = line1[1]
        #line = line.strip()[line.rindex(":") + 2:]
        scores = [float(x.split("*")[0]) for x in line.split(" + ")]
        words = [x.split("*")[1].split('/')[0] for x in line.split(" + ")]
        freqs = []
        for word, score in zip(words, scores):
            freqs.append((word, score))

        wc = WordCloud().generate_from_frequencies(freqs)
        plt.imshow(wc)
        plt.axis("off")
        curr_topic += 1
        plt.show()




#def classify_articles(ldamodel, texts):

#### MAIN PROGRAM ####

def main():
    # build LDA Model
    texts = read_articles("londonarticles_small_train.csv")
    ldamodel = train_model(texts)

    ldamodel.save('londonmodel')

    # # classify new documents using the model
    # texts = read_articles("londonarticles_small_test.csv")
    # classify_articles(ldamodel, texts)

##### CALL MAIN PROGRAM #####

if __name__ == '__main__':
    main()
