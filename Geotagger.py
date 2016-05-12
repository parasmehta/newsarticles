# imports

# !!! OUT OF ORDER !!! --> use Tagger.py instead!

import csv

# empty dictionaries
dict_streets_london     = {}
dict_streets_roma       = {}
dict_streets_sofia      = {}
dict_adminlevel_london  = {}
dict_adminlevel_roma    = {}
dict_adminlevel_sofia   = {}
dict_articles_london    = {}
dict_articles_roma      = {}
dict_articles_sofia     = {}

# functions

# file-io
def load_data():

    # fill dictionaries

    # streets
    f_roads_london = open('roads_london.txt', 'rb')             # open file
    for row in csv.reader(f_roads_london):                      # save content to dictionary
        tmp = row.split()
        dict_entry = {tmp[3],tmp[10]}
        dict_streets_london.update(dict_entry)
    f_roads_london.close()                                      # close file

    # f_roads_roma = open('roads_roma.txt', 'rb')                 # open file
    # for row in csv.reader(f_roads_roma):                        # save content to dictionary
    #     tmp = row.split()
    #     dict_entry = {tmp[3],tmp[10]}
    #     dict_streets_roma.update(dict_entry)
    # f_roads_roma.close()                                        # close file
    #
    # f_roads_sofia = open('roads_sofia.txt', 'rb')               # open file
    # for row in csv.reader(f_roads_sofia):                       # save content to dictionary
    #     tmp = row.split()
    #     dict_entry = {tmp[3],tmp[10]}
    #     dict_streets_sofia.update(dict_entry)
    # f_roads_sofia.close()                                       # close file

    # admin levels
    f_admin_london = open('admin_london.txt', 'rb')             # open file
    for row in csv.reader(f_admin_london):                      # save content to dictionary
        tmp = row.split()
        dict_entry = {tmp[2],tmp[4]}
        dict_adminlevel_london.update(dict_entry)
    f_admin_london.close()                                      # close file

    # f_admin_roma = open('admin_roma.txt', 'rb')                 # open file
    # for row in csv.reader(f_admin_roma):                        # save content to dictionary
    #     tmp = row.split()
    #     dict_entry = {tmp[2],tmp[4]}
    #     dict_adminlevel_roma.update(dict_entry)
    # f_admin_roma.close()                                        # close file
    #
    # f_admin_sofia = open('admin_sofia.txt', 'rb')               # open file
    # for row in csv.reader(f_admin_sofia):                       # save content to dictionary
    #     tmp = row.split()
    #     dict_entry = {tmp[2],tmp[4]}
    #     dict_adminlevel_sofia.update(dict_entry)
    # f_admin_sofia.close()                                       # close file

    # load articles
    f_articles_london = open('londonarticles.csv', 'rb')          # open file
    line = 0
    for row in csv.reader(f_articles_london):                     # save content to dictionary
        tmp = row.split("|")
        dict_entry = {line, tmp}
        dict_articles_london.update(dict_entry)
    f_articles_london.close()                                     # close file

    # f_articles_roma = open('articles_roma.txt', 'rb')           # open file
    # for row in csv.reader(f_articles_roma):                     # save content to dictionary
    #     tmp = row.split()
    #     dict_entry = {tmp[2],tmp[4]}
    #     dict_articles_london.update(dict_entry)
    # f_articles_roma.close()                                     # close file
    #
    # f_articles_sofia = open('articles_sofia.txt', 'rb')         # open file
    # for row in csv.reader(f_articles_sofia):                    # save content to dictionary
    #     tmp = row.split()
    #     dict_entry = {tmp[2],tmp[4]}
    #     dict_articles_london.update(dict_entry)
    # f_articles_sofia.close()                                    # close file

    data = [                                                                           # data matrix
            [dict_articles_london],   #,dict_articles_roma, dict_articles_sofia],      # 1st row: articles     (data[1])
            [dict_streets_london],    #, dict_streets_roma, dict_streets_sofia],       # 2nd row: streets      (data[2])
            [dict_adminlevel_london]  #, dict_adminlevel_roma, dict_adminlevel_sofia]  # 3rd row: admin levels (data[3])
           ]

    return data

def geotagging_streets(articles,roads):

    tagged = False

    for road in roads:
        if (road in articles[3]):                                                       # articles[3] = article content
            # TODO tag
            tagged = True

    return tagged

def geotagging_adminlevels(articles, adminlvls):

    tagged = False
    for adminlvl in adminlvls:
        if (adminlvl in articles[3]):                                                   # articles[3] = article content
            # TODO tag
            tagged = True

    return tagged


def timetagging(article, time):

    tagged = False
    if ("hallo" in articles[3]):                                                        # articles[3] = article content
        # TODO tag
        tagged = True

    return tagged

# helper functions
def getTopic(articles):
    return articles[1]

# program
def main():

    print("\nSTARTING GEOTAGGING!\n")

    data = load_data();

    for i in range(1,len(data[1])+1,1):

        isGeotagged  = 0                                        # initial value
        isTimetagged = 0                                        # initial value

        #GEO############################################################################################################

        # GEOTAGGING
        if (not isGeotagged):
            isGeotagged = geotagging_streets(data[1][i], data[2][i])             # find streets mentioned in article
        if (not isGeotagged):
            isGeotagged = geotagging_adminlevels(data[1][i], data[3][i])         # find admin level mentioned in article

        if (not isGeotagged):                                                    # JUST LOGGING...
            print("WARNING: Article: " + getTopic(data[1][i]) + " could not be geotagged!\n")

        #TIME###########################################################################################################

        # TIMETAGGING
        if (not isTimetagged):
            isTimetagged = timetagging(article)                 # find time mentioned in article

        if (not isTimetagged):                                  # JUST LOGGING...
            print("WARNING: Article: " + getTopic(article) + " could not be timetagged!\n")

    print("\nGEOTAGGING COMPLETED!\n")

# start with main()
if __name__ == '__main__':
    main()