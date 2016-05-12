#as3:/usr/local/lib/python2.7/site-packages# cat sitecustomize.py
# encoding=utf8
from __future__ import print_function
import sys
import pandas as pd
import os  # for os.path.basename
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import MDS
from sklearn.externals import joblib

reload(sys)
sys.setdefaultencoding('utf8')

from sklearn.feature_extraction.text import TfidfVectorizer
import nltk, gensim, csv, re, mpld3
from stop_words import get_stop_words
from nltk.tokenize import word_tokenize, sent_tokenize
from gensim import corpora, models, utils
from sklearn.cluster import KMeans


#define custom toolbar location
class TopToolbar(mpld3.plugins.PluginBase):
    """Plugin for moving toolbar to top of figure"""

    JAVASCRIPT = """
    mpld3.register_plugin("toptoolbar", TopToolbar);
    TopToolbar.prototype = Object.create(mpld3.Plugin.prototype);
    TopToolbar.prototype.constructor = TopToolbar;
    function TopToolbar(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    TopToolbar.prototype.draw = function(){
      // the toolbar svg doesn't exist
      // yet, so first draw it
      this.fig.toolbar.draw();

      // then change the y position to be
      // at the top of the figure
      this.fig.toolbar.toolbar.attr("x", 150);
      this.fig.toolbar.toolbar.attr("y", 400);

      // then remove the draw function,
      // so that it is not called again
      this.fig.toolbar.draw = function() {}
    }
    """
    def __init__(self):
        self.dict_ = {"type": "toptoolbar"}


# gets the tokens from text by breaking it into sentences, then words and removing punctuation
def gettokens(text):
    text = text.lower()
    tokens = []

#    tokenizer = RegexpTokenizer(r'\w+')

    for sent in sent_tokenize(text):
        for word in utils.lemmatize(sent):
            tokens.append(word)

    # create English stop words list
    en_stop = get_stop_words('en')

    otherstopwords = ['ms', 'appear', 'time', 'give', 'month', 'ask', 'twitter', 'used', 'include', 'today', 'duggan',
                      'describe', 'dog', 'see', 'police', 'court', 'pm', 'anonymously', 'year', 'old', 'take', 'find',
                      'get', 'anyone', 'crimestopper', 'incident', 'person', 'information', 'contact', 'will', 'also',
                      'say', 'tell', 'told', 'man', 'call', '\'s', 'one', 'two', 'last', '0800', 'polouse', 'inform',
                      'london', 'be', 'have', 'mr', 'officer', 'go', 'make', 'british', 'image', 'charge', 'custody',
                      'investigation', 'suspicion', 'magistrate', 'arrest', 'spokesman', 'offence', 'address', 'quote',
                      'suspect', 'wear', 'know', 'guilty', 'victim', 'appeal', 'probe', 'met', 'jail', 'video', 'trial',
                      'attempted', 'crime', 'public', 'yard', 'scotland/NN yard', 'scotland', 'metropolitan',
                      'yesterday', 'follow', 'bailey']

    stopped_tokens = [i for i in tokens if i[:-3] not in en_stop and i[:-3] not in otherstopwords]

    # print stopped_tokens

    return stopped_tokens


def read_articles(filename):
    titles = []
    texts = []
    numarticles = 0

    with open(filename, 'rb') as csvfile:
        filer = csv.reader(csvfile, delimiter='|')

        next(filer, None) # skip header

        for row in filer:
            if len(row) != 3:
                print("row has ", len(row), " columns: ", row)
                sys.exit(-1)

            title = row[0].strip()

            if not title.endswith("."):
                title += ". "

            print(title)

            titles.append(title)

            numarticles += 1

            sent = title + row[2]     # text = title + body

            texts.append(sent.decode("utf-8"))


    print(numarticles, "articles read")

    return texts, titles


def clustertopwords(km, num_clusters, frame, terms):
    print("Top terms per cluster:")
    print()
    # sort cluster centers by proximity to centroid
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]

    clusternames = {}
    for i in range(num_clusters):
        print("Cluster %d words:" % i, end='')

        topwords = ""
        for ind in order_centroids[i, :6]:  # replace 6 with n words per cluster
            topwords = topwords + terms[ind].encode('utf-8', 'ignore')[:-3] + ", "
            print(' %s' % terms[ind].encode('utf-8', 'ignore'),
                  end=',')
        print()  # add whitespace
        print()  # add whitespace

        clusternames[i] = topwords[:-1]

        print("Cluster %d titles:" % i, end='')
        for title in frame.ix[i]['title'].values.tolist():
            print(' %s,' % title, end='')
        print()  # add whitespace
        print()  # add whitespace


    print()
    print()

    return clusternames

#### MAIN PROGRAM ####

def main():
    # define vectorizer parameters
    texts, titles = read_articles("londonarticles.csv")

    tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000, min_df=0.1, stop_words='english',
                                       use_idf=True, tokenizer=gettokens, ngram_range=(1, 3))


    tfidf_matrix = tfidf_vectorizer.fit_transform(texts)  # fit the vectorizer to synopses

    print(tfidf_matrix.shape)

    terms = tfidf_vectorizer.get_feature_names()



    num_clusters = 5

    km = KMeans(n_clusters=num_clusters)

    km.fit(tfidf_matrix)

    clusters = km.labels_.tolist()

    # uncomment the below to save your model
    # since I've already run my model I am loading from the pickle

    # joblib.dump(km,  'doc_cluster.pkl')
    #
    # km = joblib.load('doc_cluster.pkl')
    # clusters = km.labels_.tolist()


    articles = { 'title': titles, 'texts': texts, 'cluster': clusters }

    frame = pd.DataFrame(articles, index=[clusters], columns=['title', 'cluster'])

    frame['cluster'].value_counts()  # number of films per cluster (clusters from 0 to 4)

    clusternames = clustertopwords(km,num_clusters,frame,terms)

    dist = 1 - cosine_similarity(tfidf_matrix)

    MDS()

    # convert two components as we're plotting points in a two-dimensional plane
    # "precomputed" because we provide a distance matrix
    # we will also specify `random_state` so the plot is reproducible.
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)

    pos = mds.fit_transform(dist)  # shape (n_components, n_samples)

    xs, ys = pos[:, 0], pos[:, 1]
    print()
    print()

    #set up colors per clusters using a dict
    cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e', 5: '#a9a9a9'}

    print("Names", clusternames)

    # create data frame that has the result of the MDS plus the cluster numbers and titles
    df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=titles))

    # group by cluster
    groups = df.groupby('label')

    # define custom css to format the font and to remove the axis labeling
    css = """
    text.mpld3-text, div.mpld3-tooltip {
      font-family:Arial, Helvetica, sans-serif;
    }

    g.mpld3-xaxis, g.mpld3-yaxis {
    display: none; }

    svg.mpld3-figure {
    margin-left: -200px;}
    """

    # Plot
    fig, ax = plt.subplots(figsize=(14, 6))  # set plot size
    ax.margins(0.03)  # Optional, just adds 5% padding to the autoscaling

    # iterate through groups to layer the plot
    # note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
    for name, group in groups:
        points = ax.plot(group.x, group.y, marker='o', linestyle='', ms=8,
                         label=clusternames[name], mec='none',
                         color=cluster_colors[name])
        ax.set_aspect('auto')
        labels = [i for i in group.title]

        # set tooltip using points, labels and the already defined 'css'
        tooltip = mpld3.plugins.PointHTMLTooltip(points[0], labels,
                                                 voffset=10, hoffset=10, css=css)
        # connect tooltip to fig
        mpld3.plugins.connect(fig, tooltip, TopToolbar())

        # set tick marks as blank
        ax.axes.get_xaxis().set_ticks([])
        ax.axes.get_yaxis().set_ticks([])

        # set axis as blank
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)

    ax.legend(numpoints=1, loc=1, fontsize=7)  # show legend with only one dot

    mpld3.display()  # show the plot

    # uncomment the below to export to html
    html = mpld3.fig_to_html(fig)
    f1 = open('clusters1.html', 'w+')
    f1.write(html)

    # # create data frame that has the result of the MDS plus the cluster numbers and titles
    # df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=titles))
    #
    # # group by cluster
    # groups = df.groupby('label')
    #
    # # set up plot
    # fig, ax = plt.subplots(figsize=(17, 9))  # set size
    # ax.margins(0.05)  # Optional, just adds 5% padding to the autoscaling
    #
    # # iterate through groups to layer the plot
    # # note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
    # for name, group in groups:
    #     ax.plot(group.x, group.y, marker='o', linestyle='', ms=12,
    #             label=clusternames[name], color=cluster_colors[name],
    #             mec='none')
    #     ax.set_aspect('auto')
    #     ax.tick_params( \
    #         axis='x',  # changes apply to the x-axis
    #         which='both',  # both major and minor ticks are affected
    #         bottom='off',  # ticks along the bottom edge are off
    #         top='off',  # ticks along the top edge are off
    #         labelbottom='off')
    #     ax.tick_params( \
    #         axis='y',  # changes apply to the y-axis
    #         which='both',  # both major and minor ticks are affected
    #         left='off',  # ticks along the bottom edge are off
    #         top='off',  # ticks along the top edge are off
    #         labelleft='off')
    #
    # ax.legend(numpoints=1)  # show legend with only 1 point
    #
    # #add label in x,y position with the label as the film title
    # # for i in range(len(df)):
    # #     ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['title'], size=8)
    #
    # plt.show() #show the plot
    #
    # # uncomment the below to save the plot if need be
    # plt.savefig('clusters_small_noaxes.png', dpi=200)

##### CALL MAIN PROGRAM #####

if __name__ == '__main__':
    main()