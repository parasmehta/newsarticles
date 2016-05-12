# coding=utf-8
                                                                                                                        # IMPORTS
import csv

                                                                                                                        # LISTS
list_london_roads       = []
list_london_adminlevels = []
list_london_articles    = []

                                                                                                                        # FUNCTIONS
def main():

    num_not_tagged = 0                                                                                                  # initial value
    num_tagged = 0                                                                                                      # initial value

    print("Preparing needed lists...\n")

                                                                                                                        # ROADS

    f_roads_london = open('london_roads.csv', 'rb')                                                                     # open file
    for tmp in csv.reader(f_roads_london, delimiter=';'):                                                               # save content to list
        list_entry = [tmp[0], tmp[1]]                                                                                   # |
        list_london_roads.append(list_entry)                                                                            # |
    f_roads_london.close()                                                                                              # close file
    print("Filling list with roads = done...\n")

                                                                                                                        # ADMIN LEVELS
    f_admin_london = open('london_admin.csv', 'rb')                                                                     # open file
    for row in csv.reader(f_admin_london):                                                                              # save content to list
        tmp = str(row).split(";")                                                                                       # |
        list_entry = [tmp[0].replace('"',''), tmp[1], tmp[2]]                                                           # |
        list_london_adminlevels.append(list_entry)                                                                      # |
    f_admin_london.close()                                                                                              # close file
    print("Filling lists with admin levels = done...\n")

                                                                                                                        # ARTICLES

    f_articles_london = open('london_articles.csv', 'rb')                                                               # open file
    for tmp in csv.reader(f_articles_london, delimiter='|'):                                                            # save content to dictionary
        list_entry = [tmp[0], tmp[1], tmp[2]]                                                                           # |
        list_london_articles.append(list_entry)                                                                         # |
    f_articles_london.close()                                                                                           # close file
    print("Filling lists with articles = done...\n\n")

    print("Start tagging articles ...\n")

    output = open('london_articles_tagged.txt', 'wb')
    writer = csv.writer(output)

    isTagged = [False] * len(list_london_articles)

    for road in list_london_roads:
        for id in range(0, len(list_london_articles),1):
            article = list_london_articles[id]

            if ((road[0] in article[0]) or (road[0] in article[2])):                                                    # check if road name is in title or content of article
                article.append(road[1])                                                                                 # tag article with a position (road)
                writer.writerow(article)                                                                                # write article to file
                isTagged[id] = True                                                                                     # set flag
                num_tagged += 1

    print("Roads have been tagged ...\n")

    for admlvl in list_london_adminlevels:
        for id in range(0, len(list_london_articles), 1):
            article = list_london_articles[id]                                                                          # just a helper

            if not isTagged[id]:                                                                                        # if article was not already tagged
                if ((admlvl[0] in article[0] or admlvl[0] in article[2])):                                              # contains the article an administrative level name?
                    article.append(admlvl[2])                                                                           # tag article with a position (admin level)
                    writer.writerow(article)                                                                            # write article to file
                    isTagged[id] = True                                                                                 # set flag
                    num_tagged += 1

    print("Administration levels have been tagged ...\n")

    output.close()                                                                                                      # close the file london_articles_tagged.txt

    for id in range(0,len(isTagged),1):
        if (not isTagged[id]):
            print("WARNING: NOT TAGGED --> " + list_london_articles[id][0])                                             # print title of articles that have not been tagged
            num_not_tagged += 1

                                                                                                                        # TIME TAGGING ?
                                                                                                                        # - done by using the second attribute "time" of the extracted articles

    print("Number of tagged articles: "+str(num_tagged)+" | Number of NOT tagged articles "+str(num_not_tagged)+" .\n")
    print("TAGGING COMPLETED!\n")


# start with main()
if __name__ == '__main__':
    main()