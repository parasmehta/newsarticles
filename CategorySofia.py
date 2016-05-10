# -*- coding: utf-8 -*-

import nltk, gensim, csv, re
from nltk.tokenize import WordPunctTokenizer
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models


def gettokens(text):
    text = text.lower()
    tokens = []

    tokenizer = RegexpTokenizer(r'\w+')

    for sent in sent_tokenize(text.decode('utf-8')):
        for word in word_tokenize(sent):
            if word == "n't":
                word = 'not'

                # if €","–" in word:
                #   continue
            #            if re.match(r'^\w+$', word):
            #                tokens.append(word)

            if word in ' ,-.\'':
                continue

            if word in ['will', 'also', 'said', '\'s']:
                continue

            tokens.append(word)

    # return filter(lambda word: word not in ',-.', tokens)
    return tokens


def process(doc):
    tokens = gettokens(doc)

    # create English stop words list
    en_stop = get_stop_words('en')

    stopped_tokens = [i for i in tokens if not i in en_stop]

    # print stopped_tokens

    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()

    # stem token
    stemmed_tokens = []
    for i in stopped_tokens:
        stemmed_tokens.append(p_stemmer.stem(i))

    print stemmed_tokens

    return stemmed_tokens


def read_articles(filename):
    texts = []
    numarticles = 0

    with open(filename, 'rb') as csvfile:
        filer = csv.reader(csvfile, delimiter='|')

        next(filer, None)  # skip header

        for row in filer:
            if len(row) > 0:

                title = row[0].strip()

                if not title.endswith("."):
                    title += ". "

                print title
                numarticles += 1

                sent = title + row[2]

                texts.append(sent)
            else:
                print "row has 0 columns: " + row

    print numarticles, "articles processed"

    return texts


def process_articles(articletexts):
    # doc_a = u"Escaped Rome prisoners caught. One prisoner gave himself up, the other arrested outside Rome.Two prisoners who escaped from Rome’s Rebibbia jail on 14 February are back in custody after one gave himself up on the afternoon of 17 February and the other was caught by police later that night.Both arrests were made in the Tivoli area north-east of Rome, ending a four-day manhunt that began after the prisoners sawed through window bars and scaled the prison walls using knotted sheets.One of the defendants, Catalin Ciobanu, handed himself in to Tivoli police station after realising he had “done something stupid”, according to his lawyer. Police discovered the other escapee, Mihai Florin Diaconescu, aboard a van in the Tivoli area. He was apprehended after a short chase by foot. Prosecutors in Rome have launched an investigation into the break-out from the city jail."
    # doc_b = u"Rome manhunt for escaped prisoners. Inmates remain at large after breaking out of Rome prison.A police manhunt is in operation in the greater Rome area for two prisoners who broke out of the city's Rebibbia jail during the evening of 14 February.The inmates, who include a convicted murderer and are described as \"very dangerous\", remain at large after evading capture for a second night.The pair escaped after sawing through window bars and scaling the prison wall using an improvised rope made from knotted sheets, before fleeing by foot on Via Tiburtina in the northeast Rebibbia suburb.They made their escape while attending a workshop at a new prison area, which was staffed by just two guards at the time and whose alarm system did not work, according to Italian news agency ANSA.Police are continuing with road blocks and bus checks around Rome in an attempt to catch the two who are named as Catalin Ciobanu and Mihai Florin Diaconescu, aged 33 and 28 respectively, from Romania."
    # doc_c = u"Rome opposes violence against women. A total of 152 women were murdered in Italy in 2014, with 94 per cent of the deaths attributed to men, according to a report into femicide released on 24 November. Of the 152 murdered women, 117 were killed within a family context. However the findings by European research institute EURES reveal that the overall number of femicides in 2014 was down just over 15 per cent compared to 2013.Marking the UN-backed International Day for the Elimination of Violence against Women on 25 November, volunteers from the multi-lingual women’s helpline Telefona Rosa are organising an event at the Auditorium della Conciliazione from 09.30-13.00, featuring experts speaking on the theme “women uniting diverse worlds and cultures”.The Teatro Sistina stages X=Y, a play opposing violence against women, aimed at a young audience, on 25 and 26 November at 10.30 on both days.A “tango session with red shoes” takes place at Porta S. Paolo from 19.00-21.30 on 25 November. Organisers say the initiative, performed and overseen by Argentinian dancers, will use tango as a “beautiful metaphor for the harmony that is possible between men and women.” The Casa Internazionale delle Donne on Via della Lungara 19, in Trastevere, is holding a talk entitled Le donne di fronte al terrorismo on 25 November at 17.30. All events in Italian.Proceeds from the sale of prints at the Chiostro del Bramante between now and 29 November will go towards Donne in Rete contro la violenza (D.iRe), the national association of independent women’s centres and shelters against violence.Each pair of red shoes in the photo symbolises a murdered woman."
    # doc_d = u"Mafia Capitale prosecutors indict ex-mayor Alemanno. Rome’s ex right-wing mayor Gianni Alemanno accused of corruption.Prosecutors in Rome have sought an indictment for the city’s former mayor Gianni Alemanno on accusations of corruption, in connection with the so-called Mafia Capitale trial which opened on 5 November. The indictment does not contain charges of association with the mafia.The Mafia Capitale trial is the result of a major investigation into a mafia-style syndicate accused of infiltrating city hall, involving politicians, public officials and business people who allegedly helped mobsters to win lucrative city contracts in sectors such as immigrant housing, camps for Roma people, waste management, recycling and parks maintenance.Prosecutors suspect Alemanno, the capital’s right-wing mayor from 2008 to 2013, of receiving €125,000 in illicit funds between 2012 and 2014. They allege the money was funnelled to him in separate tranches by three of the highest-profile defendants in the Mafia Capitale trial.Prosecutors believe Alemanno received €75,000 in financing for electoral dinners, €40,000 for his foundation, and about €10,000 in cash, the last of which he allegedly received in October 2014, two months before the first wave of Mafia Capitale arrests.Prosecutors allege that Alemanno received the illicit funds via his Nuova Italia foundation in exchange for “acts running counter to his duties in office”. On 11 December the trial’s judge Nicola Di Grazia will rule whether or not Alemanno should stand trial. The ex-mayor maintains his “complete innocence.”The Mafia Capitale trial is currently based at the criminal courts in Prati’s Piazzale Clodio but on 10 November is scheduled to relocate to the high security court at the Rebibbia prison in the eastern outskirts of Rome, which is better equipped for handling large groups of defendants."
    # doc_e = "Health professionals say that brocolli is good for your health."
    # compile sample documents into a list
    # doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]

    # list for tokenized documents in loop
    texts = []

    # loop through document list
    for i in articletexts:
        stemmed_tokens = process(i)

        # add tokens to list
        texts.append(stemmed_tokens)

    dictionary = corpora.Dictionary(texts)

    corpus = [dictionary.doc2bow(text) for text in texts]

    print(corpus[0])

    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=12, id2word=dictionary, passes=20)

    # print(ldamodel.print_topics(num_topics=6, num_words=4))

    print "Topics: "
    print(ldamodel.print_topics(num_topics=12))


#### MAIN PROGRAM ####

def main():
    texts = read_articles("romearticles_clean.csv")
    process_articles(texts)


##### CALL MAIN PROGRAM #####

if __name__ == '__main__':
    main()
