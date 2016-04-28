# -*- coding: utf-8 -*-

import nltk, gensim
from nltk.tokenize import WordPunctTokenizer
from nltk.tokenize import wordpunct_tokenize
from stop_words import get_stop_words
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models

def gettokens(text):
    text = text.lower()
    tokens = [word if word != "n't" else 'not' for sent in sent_tokenize(text) for word in word_tokenize(sent)]
    return filter(lambda word: word not in ',-.', tokens)


def process(doc):
    tokens = gettokens(doc)

    print tokens

    # create English stop words list
    en_stop = get_stop_words('en')

    stopped_tokens = [i for i in tokens if not i in en_stop]

    # print stopped_tokens

    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()

    # stem token
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

    # print(stemmed_tokens)

    return stemmed_tokens


def run():
    doc_a = "Escaped Rome prisoners caught. One prisoner gave himself up, the other arrested outside Rome.Two prisoners who escaped from Rome’s Rebibbia jail on 14 February are back in custody after one gave himself up on the afternoon of 17 February and the other was caught by police later that night.Both arrests were made in the Tivoli area north-east of Rome, ending a four-day manhunt that began after the prisoners sawed through window bars and scaled the prison walls using knotted sheets.One of the defendants, Catalin Ciobanu, handed himself in to Tivoli police station after realising he had “done something stupid”, according to his lawyer. Police discovered the other escapee, Mihai Florin Diaconescu, aboard a van in the Tivoli area. He was apprehended after a short chase by foot. Prosecutors in Rome have launched an investigation into the break-out from the city jail."
    doc_b = "Rome manhunt for escaped prisoners. Inmates remain at large after breaking out of Rome prison.A police manhunt is in operation in the greater Rome area for two prisoners who broke out of the city's Rebibbia jail during the evening of 14 February.The inmates, who include a convicted murderer and are described as \"very dangerous\", remain at large after evading capture for a second night.The pair escaped after sawing through window bars and scaling the prison wall using an improvised rope made from knotted sheets, before fleeing by foot on Via Tiburtina in the northeast Rebibbia suburb.They made their escape while attending a workshop at a new prison area, which was staffed by just two guards at the time and whose alarm system did not work, according to Italian news agency ANSA.Police are continuing with road blocks and bus checks around Rome in an attempt to catch the two who are named as Catalin Ciobanu and Mihai Florin Diaconescu, aged 33 and 28 respectively, from Romania."
    doc_c = u"One prisoner gave himself up, the other arrested outside Rome.Two prisoners who escaped from Rome’s Rebibbia jail on 14 February are back in custody after one gave himself up on the afternoon of 17 February and the other was caught by police later that night."
    doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
    doc_e = "Health professionals say that brocolli is good for your health."

    # compile sample documents into a list
    doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]

    # list for tokenized documents in loop
    texts = []

    # loop through document list
    for i in doc_set:
        stemmed_tokens = process(i)

        # add tokens to list
        texts.append(stemmed_tokens)


    dictionary = corpora.Dictionary(texts)

    corpus = [dictionary.doc2bow(text) for text in texts]

    print(corpus[0])

    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word=dictionary, passes=20)

    print(ldamodel.print_topics(num_topics=3, num_words=3))

#### MAIN PROGRAM ####

def main():

    run()



##### CALL MAIN PROGRAM #####

if __name__ == '__main__':
    main()
